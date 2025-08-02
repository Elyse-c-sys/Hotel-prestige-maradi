from flask import Flask, render_template, request, redirect, url_for, session, flash
import csv
import os
from datetime import datetime
from fpdf import FPDF
from collections import Counter
import pandas as pd

app = Flask(__name__)
app.secret_key = 'prestige-secret-key'

DOSSIER_PDF = 'fiches_pdf'
if not os.path.exists(DOSSIER_PDF):
    os.makedirs(DOSSIER_PDF)

CSV_FILE = 'clients.csv'
PASSWORD = "Pension@2025"

# ----------- ROUTES -----------

@app.route('/')
def accueil():
    return render_template('accueil.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        mot_de_passe = request.form.get('password')
        if mot_de_passe == PASSWORD:
            session['gerant'] = True
            return redirect(url_for('fiche'))
        else:
            flash("Mot de passe incorrect", "error")
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('gerant', None)
    return redirect(url_for('login'))

@app.route('/fiche', methods=['GET', 'POST'])
def fiche():
    if 'gerant' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        data = {
            'nom': request.form['nom'],
            'prenom': request.form['prenom'],
            'date_naissance': request.form['date_naissance'],
            'lieu_naissance': request.form['lieu_naissance'],
            'nationalite': request.form['nationalite'],
            'profession': request.form['profession'],
            'organisme': request.form['organisme'],
            'domicile': request.form['domicile'],
            'provenance': request.form['provenance'],
            'destination': request.form['destination'],
            'transport': request.form['transport'],
            'telephone': request.form['telephone'],
            'piece_type': request.form['piece_type'],
            'piece_numero': request.form['piece_numero'],
            'delivre_date': request.form['delivre_date'],
            'delivre_lieu': request.form['delivre_lieu'],
            'arrivee': request.form['arrivee'],
            'depart': request.form['depart'],
            'motif': request.form['motif'],
            'renseignement': request.form['renseignement'],
        }

        with open(CSV_FILE, mode='a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(data.values())

        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt="HÔTEL LE PRESTIGE MARADI", ln=True, align='C')
        pdf.cell(200, 10, txt="Tel: 96970571 / 94250556", ln=True, align='C')
        pdf.ln(10)
        pdf.set_font("Arial", 'B', 14)
        pdf.cell(200, 10, txt="FICHE DE RENSEIGNEMENT CLIENT", ln=True, align='C')
        pdf.ln(10)
        pdf.set_font("Arial", size=12)

        for key, value in data.items():
            pdf.cell(0, 10, txt=f"{key.replace('_', ' ').capitalize()} : {value}", ln=True)

        filename = f"{data['nom']}_{data['prenom']}_{datetime.now().strftime('%Y%m%d%H%M%S')}.pdf"
        pdf_path = os.path.join(DOSSIER_PDF, filename)
        pdf.output(pdf_path)

        flash("✅ Client enregistré avec succès !", "success")
        return redirect(url_for('fiche'))

    return render_template('fiche.html')

@app.route('/clients')
def liste_clients():
    if 'gerant' not in session:
        return redirect(url_for('login'))

    clients = []
    if os.path.exists(CSV_FILE):
        with open(CSV_FILE, mode='r', encoding='utf-8') as f:
            reader = csv.reader(f)
            for row in reader:
                clients.append(row)
    return render_template('clients.html', clients=clients)

@app.route('/dashboard')
def dashboard():
    if 'gerant' not in session:
        return redirect(url_for('login'))

    if not os.path.exists(CSV_FILE):
        return render_template('dashboard.html', stats={})

    df = pd.read_csv(CSV_FILE, header=None)
    if df.empty:
        return render_template('dashboard.html', stats={})

    today = datetime.today().strftime('%Y-%m-%d')
    stats = {
        "clients_aujourdhui": df[df[16] == today].shape[0],
        "par_destination": dict(Counter(df[9])),
        "par_nationalite": dict(Counter(df[4]))
    }
    return render_template('dashboard.html', stats=stats)

import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)



