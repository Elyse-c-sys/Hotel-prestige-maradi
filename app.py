from flask import Flask, render_template, request, redirect, url_for
import csv
import os
from datetime import datetime
from fpdf import FPDF

app = Flask(__name__)

DOSSIER_PDF = 'fiches_pdf'
if not os.path.exists(DOSSIER_PDF):
    os.makedirs(DOSSIER_PDF)

@app.route('/')
def accueil():
    return render_template('accueil.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return redirect(url_for('fiche'))
    return render_template('login.html')

@app.route('/fiche', methods=['GET', 'POST'])
def fiche():
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

        with open('clients.csv', mode='a', newline='', encoding='utf-8') as f:
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

        return render_template('fiche.html', pdf_url=None)

    return render_template('fiche.html', pdf_url=None)

if __name__ == "__main__":
    app.run()

