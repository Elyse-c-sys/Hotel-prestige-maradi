from flask import Flask, render_template, request, redirect, url_for, session, send_from_directory
from werkzeug.utils import secure_filename
import os
from datetime import datetime
from fpdf import FPDF
from collections import Counter

app = Flask(__name__)
app.secret_key = 'cle_super_secrete'

UPLOAD_FOLDER = os.path.join('static', 'pdfs')
<<<<<<< HEAD
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

=======
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
>>>>>>> 501dfef (Mise à jour du projet)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def accueil():
    return render_template('accueil.html')

@app.route('/gerant', methods=['GET', 'POST'])
def gerant():
    if request.method == 'POST':
<<<<<<< HEAD
        nom = request.form['nom']
        prenom = request.form['prenom']
        mot_de_passe = request.form['mot_de_passe']
=======
        nom = request.form.get('nom')
        prenom = request.form.get('prenom')
        mot_de_passe = request.form.get('mot_de_passe')
>>>>>>> 501dfef (Mise à jour du projet)
        if mot_de_passe == 'Pension@2025':
            session['logged_in'] = True
            session['nom_gerant'] = nom
            session['prenom_gerant'] = prenom
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', erreur='Mot de passe incorrect.')
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if not session.get('logged_in'):
        return redirect(url_for('gerant'))
    return render_template('dashboard.html')
<<<<<<< HEAD

@app.route('/fiche', methods=['GET', 'POST'])
def fiche():
    if not session.get('logged_in'):
        return redirect(url_for('gerant'))
    if request.method == 'POST':
        data = request.form.to_dict()
        now = datetime.now()
        timestamp = now.strftime("%Y%m%d%H%M%S")
        nom_fichier_pdf = f"{secure_filename(data['nom'])}_{timestamp}.pdf"
        chemin_pdf = os.path.join(app.config['UPLOAD_FOLDER'], nom_fichier_pdf)

        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        pdf.cell(200, 10, txt="FICHE DE RENSEIGNEMENT CLIENT", ln=True, align='C')
        pdf.ln(10)
        pdf.set_font("Arial", 'B', 14)
        pdf.cell(200, 10, txt="HOTEL LE PRESTIGE MARADI", ln=True, align='C')
        pdf.set_font("Arial", '', 12)
        pdf.cell(200, 10, txt="Tel : 96970571 / 94250556", ln=True, align='C')
        pdf.ln(5)
        pdf.set_font("Arial", 'B', 13)
        pdf.cell(200, 10, txt="FICHE DE RENSEIGNEMENT CLIENT", ln=True, align='C')
        pdf.ln(10)

        for key, value in data.items():
            pdf.cell(200, 10, txt=f"{key.replace('_',' ').capitalize()} : {value}", ln=True)

        pdf.output(chemin_pdf)
 
        return render_template('fiche.html', message='✅ Client enregistré avec succès.')
    return render_template('fiche.html')



@app.route('/pdfs')
def pdfs():
    if not session.get('logged_in'):
        return redirect(url_for('gerant'))
    fichiers = sorted(os.listdir(app.config['UPLOAD_FOLDER']), reverse=True)
    return render_template('pdfs.html', fichiers=fichiers)

@app.route('/telecharger/<nom_fichier>')
def telecharger(nom_fichier):
    return send_from_directory(app.config['UPLOAD_FOLDER'], nom_fichier)

=======

@app.route('/fiche', methods=['GET', 'POST'])
def fiche():
    if not session.get('logged_in'):
        return redirect(url_for('gerant'))
    if request.method == 'POST':
        data = request.form.to_dict()
        now = datetime.now()
        timestamp = now.strftime("%Y%m%d%H%M%S")
        nom_fichier_pdf = f"{secure_filename(data.get('nom','client'))}_{timestamp}.pdf"
        chemin_pdf = os.path.join(app.config['UPLOAD_FOLDER'], nom_fichier_pdf)

        pdf = FPDF('P', 'mm', 'A4')
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()
        pdf.set_margins(15, 15, 15)

        pdf.set_font("Arial", 'B', 14)
        pdf.cell(0, 7, txt="FICHE DE RENSEIGNEMENT CLIENT", ln=True, align='L')
        pdf.ln(2)
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(0, 7, txt="HOTEL LE PRESTIGE MARADI", ln=True, align='L')
        pdf.set_font("Arial", '', 10)
        pdf.multi_cell(pdf.w - 30, 6, txt="Tel : 96970571 / 94250556", align='L')
        pdf.ln(2)
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(0, 7, txt="FICHE DE RENSEIGNEMENT CLIENT", ln=True, align='L')
        pdf.ln(2)

        pdf.set_font("Arial", '', 10)
        for key, value in data.items():
            text = f"{key.replace('_',' ').capitalize()} : {value}"
            text = text.replace('’', "'")
            pdf.multi_cell(pdf.w - 30, 6, txt=text, align='L')
            pdf.ln(0.5)

        pdf.ln(10)
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(0, 6, txt="Signature du Client :", ln=True, align='L')
        pdf.set_font("Arial", '', 10)
        pdf.cell(0, 6, txt=f"Nom : {data.get('nom','')} {data.get('prenom','')}", ln=True, align='L')
        
        pdf.ln(15)  # espace plus large entre les deux signatures
        
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(0, 6, txt="Signature du Gérant :", ln=True, align='L')
        nom_gerant = session.get('nom_gerant', '') + " " + session.get('prenom_gerant', '')
        pdf.set_font("Arial", '', 10)
        pdf.cell(0, 6, txt=f"Nom : {nom_gerant}", ln=True, align='L')

        pdf.output(chemin_pdf)
        return render_template('fiche.html', message='✅ Client enregistré avec succès.')
    return render_template('fiche.html')

@app.route('/pdfs')
def pdfs():
    if not session.get('logged_in'):
        return redirect(url_for('gerant'))
    fichiers = sorted(os.listdir(app.config['UPLOAD_FOLDER']), reverse=True)
    return render_template('pdfs.html', fichiers=fichiers)

@app.route('/telecharger/<nom_fichier>')
def telecharger(nom_fichier):
    if not session.get('logged_in'):
        return redirect(url_for('gerant'))
    return send_from_directory(app.config['UPLOAD_FOLDER'], nom_fichier)

>>>>>>> 501dfef (Mise à jour du projet)
@app.route('/stats')
def stats():
    if not session.get('logged_in'):
        return redirect(url_for('gerant'))
    fichiers = os.listdir(app.config['UPLOAD_FOLDER'])
    dates = [f.split('_')[-1].replace('.pdf', '')[:8] for f in fichiers]
    par_jour = Counter(dates)
    return render_template('stats.html', par_jour=par_jour)

if __name__ == "__main__":
    app.run(debug=True)
