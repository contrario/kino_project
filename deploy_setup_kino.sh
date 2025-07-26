#!/bin/bash

echo "🚀 Starting Kino Project Setup..."

# Δημιουργία εικονικού περιβάλλοντος
python -m venv venv

# Ενεργοποίηση εικονικού περιβάλλοντος
source venv/Scripts/activate

# Εγκατάσταση dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Πρώτη δοκιμή με Streamlit
streamlit run kino_overseer_web.py
