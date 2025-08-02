# 🏨 Hôtel Prestige Maradi

Bienvenue dans l'application web **Hôtel Prestige Maradi** — une solution élégante et simple pour gérer les informations des clients d’un hôtel ou pension locale.

---

## ✨ Présentation

Cette application a été créée avec **Flask (Python)** dans le but de :

- 🎯 Enregistrer les informations détaillées des clients
- 🧑‍💼 Sécuriser l’accès par un mot de passe gérant
- 📄 Générer et sauvegarder automatiquement les fiches client (CSV + Google Sheets)
- 🌐 Offrir une interface conviviale, accessible en ligne via [Render](https://hotel-prestige-maradi-1.onrender.com)

---

## ⚙️ Fonctionnalités principales

✅ Interface d’accueil personnalisée avec logo  
✅ Authentification gérant avec mot de passe  
✅ Formulaire de fiche de renseignement complet pour les clients  
✅ Enregistrement automatique dans un fichier `.csv` + sauvegarde vers **Google Sheets**  
✅ Notification douce après enregistrement  
✅ Design élégant et professionnel (vert foncé + animations)  
✅ Application hébergée gratuitement sur Render  
✅ Architecture prête à évoluer (export PDF, notifications WhatsApp, statistiques…)

---

## 🛠️ Technologies utilisées

- Python 3.11+
- Flask
- HTML / CSS (classique et animé)
- Gunicorn (déploiement)
- Google Sheets API (sauvegarde cloud)
- CSV standard
- Render (hébergement)

---

## 🚀 Installation locale (développement)

> Assurez-vous d’avoir **Python** et **Git** installés sur votre machine.

```bash
# 1. Cloner le projet
git clone https://github.com/Elyse-c-sys/Hotel-prestige-maradi.git
cd Hotel-prestige-maradi

# 2. Créer un environnement virtuel
python -m venv venv
source venv/bin/activate  # ou venv\Scripts\activate sous Windows

# 3. Installer les dépendances
pip install -r requirements.txt

# 4. Lancer l'application localement
python app.py
