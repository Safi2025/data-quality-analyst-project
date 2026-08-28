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

# Au lieu de juste lancer tests.py, lancez un script d'exécution globale ou tests.py puis business_analytics.py
CMD ["python", "python/main.py"]