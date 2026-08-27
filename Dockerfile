# Image Python légère officielle
FROM python:3.10-slim

# Repertoire de travail dans le conteneur
WORKDIR /app

# Copie des fichiers de configuration et dépendances
COPY requirements.txt .

# Installation des bibliothèques Python
RUN pip install --no-cache-dir -r requirements.txt

# Copie du reste du projet
COPY . .

# Commande par défaut : lance l'audit Data Quality
CMD ["python", "python/tests.py"]