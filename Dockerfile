FROM python:3.9-slim

WORKDIR /app

# Mettre à jour les paquets et installer cron
RUN apt-get update && apt-get install -y cron

# Créer le dossier /data pour les logs et le CSV
# Le flag -p crée les dossiers parent s'ils n'existent pas
RUN mkdir -p /data

# Installer les dépendances Python
RUN pip install --no-cache-dir requests beautifulsoup4 pandas sqlalchemy

# Copier le code source (dossier src/) vers /app
COPY src/ /app/

# Donner les permissions d'exécution aux scripts Python
RUN chmod +x *.py

# Copier la config cron (optionnel, si tu en as besoin)
COPY crontab.sh /etc/cron.d/scraper-cron
RUN chmod 0644 /etc/cron.d/scraper-cron

# Lancer le pipeline Python au démarrage du container
# CMD ["python","main.py"] #exécute juste une fois, alors que nous voulons que cron tourne en continu
CMD ["cron", "-f"]