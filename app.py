from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
import os
import locale
import calendar
from datetime import datetime
from fpdf import FPDF
import cloudinary
import cloudinary.uploader
from sqlalchemy import extract
from dotenv import load_dotenv

# ================= CONFIGURATION =================
try:
    locale.setlocale(locale.LC_TIME, "fr_FR.UTF-8")
except:
    try:
        locale.setlocale(locale.LC_TIME, "fra_FRA")
    except:
        pass 

load_dotenv()
app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "prime_business_secure_key")

# DB Config
DATABASE_URL = os.environ.get("DATABASE_URL")
if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Cloudinary Config
cloudinary.config(
    cloud_name=os.environ.get("CLOUD_NAME"),
    api_key=os.environ.get("CLOUD_API_KEY"),
    api_secret=os.environ.get("CLOUD_API_SECRET"),
    secure=True
)

class FicheClient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    prenom = db.Column(db.String(100))
    nationalite = db.Column(db.String(50))
    provenance = db.Column(db.String(100))
    date_arrivee = db.Column(db.Date)
    date_depart = db.Column(db.Date)
    pdf_url = db.Column(db.String(255))
    cloudinary_id = db.Column(db.String(150))
    date_creation = db.Column(db.DateTime, default=datetime.utcnow)

with app.app_context():
    db.create_all()

def format_date_fr(date_str):
    if not date_str: return "Non renseigné"
    try:
        dt = datetime.strptime(date_str, '%Y-%m-%d')
        return dt.strftime('%d/%m/%Y')
    except:
        return date_str

# ================= ROUTES =================

@app.route('/')
def accueil(): return render_template('accueil.html')

@app.route('/gerant', methods=['GET', 'POST'])
def gerant():
    if request.method == 'POST':
        if request.form.get('mot_de_passe') == os.environ.get("ADMIN_PASSWORD"):
            session['logged_in'] = True
            session['nom_gerant'] = request.form.get('nom')
            session['prenom_gerant'] = request.form.get('prenom')
            return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if not session.get('logged_in'): return redirect(url_for('gerant'))
    return render_template('dashboard.html')

@app.route('/fiche', methods=['GET', 'POST'])
def fiche():
    if not session.get('logged_in'): return redirect(url_for('gerant'))

    if request.method == 'POST':
        data = request.form.to_dict()
        
        # Vérification des champs requis
        champs_requis = [
            'nom', 'prenom', 'date_naissance', 'lieu_naissance', 'nationalite',
            'profession', 'domicile', 'provenance', 'destination', 'transport',
            'telephone', 'motif', 'type_piece', 'numero_piece', 'date_delivrance',
            'lieu_delivrance', 'date_arrivee', 'date_depart'
        ]
        for c in champs_requis:
            if not data.get(c):
                return render_template('fiche.html', erreur=f"Le champ {c} est vide.")

        nom_client = data.get('nom', '').upper()
        
        # --- GÉNÉRATION PDF (TOUT À GAUCHE) ---
        pdf = FPDF()
        pdf.add_page()
        pdf.set_left_margin(20) # Marge de gauche propre

        # Titres alignés à gauche
        pdf.set_font("Arial", 'B', 16)
        pdf.cell(0, 10, "HOTEL LE PRESTIGE MARADI", ln=True, align='L')
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(0, 10, "FICHE DE RENSEIGNEMENT CLIENT", ln=True, align='L')
        pdf.ln(5)

        # Liste plate de toutes les infos
        pdf.set_font("Arial", '', 11)
        
        infos = [
            f"Nom : {nom_client}",
            f"Prénom : {data.get('prenom')}",
            f"Date de naissance : {format_date_fr(data.get('date_naissance'))}",
            f"Lieu de naissance : {data.get('lieu_naissance')}",
            f"Nationalité : {data.get('nationalite')}",
            f"Profession : {data.get('profession')}",
            f"Organisme : {data.get('organisme', 'N/A')}",
            f"Domicile : {data.get('domicile')}",
            f"Provenance : {data.get('provenance')}",
            f"Destination : {data.get('destination')}",
            f"Moyen de transport : {data.get('transport')}",
            f"Téléphone : {data.get('telephone')}",
            f"Motif du voyage : {data.get('motif')}",
            f"Type de pièce : {data.get('type_piece')}",
            f"Numéro de pièce : {data.get('numero_piece')}",
            f"Délivrée le : {format_date_fr(data.get('date_delivrance'))}",
            f"Lieu de délivrance : {data.get('lieu_delivrance')}",
            f"Date d'arrivée : {format_date_fr(data.get('date_arrivee'))}",
            f"Date de départ prévue : {format_date_fr(data.get('date_depart'))}"
        ]

        for info in infos:
            pdf.cell(0, 8, info, ln=True, align='L')

        pdf.ln(10)
        pdf.set_font("Arial", 'I', 10)
        pdf.cell(0, 6, f"Signé par l'agent : {session.get('prenom_gerant')} {session.get('nom_gerant')}", ln=True, align='L')
        pdf.cell(0, 6, f"Fait le : {datetime.now().strftime('%d/%m/%Y à %H:%M')}", ln=True, align='L')

        temp_pdf = f"temp_{secure_filename(nom_client)}.pdf"
        pdf.output(temp_pdf)

        # Upload & DB
        upload_res = cloudinary.uploader.upload(temp_pdf, resource_type="raw", public_id=f"fiches/{nom_client}_{int(datetime.now().timestamp())}")
        os.remove(temp_pdf)

        d_arr = datetime.strptime(data.get('date_arrivee'), '%Y-%m-%d').date()
        d_dep = datetime.strptime(data.get('date_depart'), '%Y-%m-%d').date()

        nouvelle_fiche = FicheClient(
            nom=nom_client, prenom=data.get('prenom'), nationalite=data.get('nationalite'),
            provenance=data.get('provenance'), date_arrivee=d_arr, date_depart=d_dep,
            pdf_url=upload_res['secure_url'], cloudinary_id=upload_res['public_id']
        )
        db.session.add(nouvelle_fiche)
        db.session.commit()

        return render_template('fiche.html', success=True)
    return render_template('fiche.html')

@app.route('/pdfs')
def pdfs():
    if not session.get('logged_in'): return redirect(url_for('gerant'))
    clients = FicheClient.query.order_by(FicheClient.date_creation.desc()).all()
    return render_template('pdfs.html', clients=clients)

@app.route('/supprimer_pdf/<int:id>')
def supprimer_pdf(id):
    if not session.get('logged_in'): return redirect(url_for('gerant'))
    fiche = FicheClient.query.get_or_404(id)
    if fiche.cloudinary_id:
        try: cloudinary.uploader.destroy(fiche.cloudinary_id, resource_type="raw")
        except: pass
    db.session.delete(fiche)
    db.session.commit()
    return redirect(url_for('pdfs'))

@app.route('/stats')
def stats():
    if not session.get('logged_in'): return redirect(url_for('gerant'))
    now = datetime.now()
    mois = int(request.args.get('mois', now.month))
    annee = int(request.args.get('annee', now.year))
    fiches = FicheClient.query.filter(extract('month', FicheClient.date_arrivee) == mois, extract('year', FicheClient.date_arrivee) == annee).all()
    
    total_nuitees, debut_mois, fin_mois = 0, 0, 0
    nationalites, provenances = {}, {}
    for f in fiches:
        if f.date_depart and f.date_arrivee:
            nuitees = max((f.date_depart - f.date_arrivee).days, 1)
            total_nuitees += nuitees
            if f.date_arrivee.day <= 20: debut_mois += nuitees
            else: fin_mois += nuitees
        if f.nationalite: nationalites[f.nationalite] = nationalites.get(f.nationalite, 0) + 1
        if f.provenance: provenances[f.provenance] = provenances.get(f.provenance, 0) + 1

    _, nb_jours = calendar.monthrange(annee, mois)
    stats_data = {
        "total": len(fiches), "total_nuitees": total_nuitees, "debut_mois": debut_mois,
        "fin_mois": fin_mois, "chiffre_affaires": total_nuitees * 17500,
        "taux_occupation": round((total_nuitees * 100) / (9 * nb_jours), 2) if nb_jours else 0,
        "nationalites": nationalites, "provenances": provenances,
        "mois_num": mois, "mois_nom": calendar.month_name[mois].capitalize(),
        "annee": annee, "nb_jours_mois": nb_jours
    }
    return render_template("stats.html", stats=stats_data, datetime_now=now.strftime("%d/%m/%Y %H:%M"))

if __name__ == "__main__":
    app.run(debug=True)