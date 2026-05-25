# livre-scraper

## # Books to Scrape - Pipeline d'Extraction Automatisé

Un pipeline de scraping automatisé qui extrait les livres du site [books.toscrape.com](https://books.toscrape.com), nettoie les données, et les sauvegarde dans un fichier CSV. Le script s'exécute automatiquement **chaque minute** via cron.

## 🎯 Objectif

Démontrer un pipeline de données robuste avec :
- Scraping HTTP avec gestion d'erreurs multi-niveaux
- Transformation et nettoyage des données
- Sauvegarde en mode ajout (accumulation)
- Logging détaillé
- Exécution planifiée via cron
- Containerisation Docker

## ✨ Fonctionnalités

✅ **Scraping automatisé** : Récupère ~40 livres (2 pages) par exécution

✅ **4 niveaux de protection** :
- Vérification de la requête HTTP
- Vérification du statut HTTP (200)
- Vérification de la pagination
- Gestion d'erreur par livre

✅ **Nettoyage intelligent** :
- Prix : `£51.77` → `51.77`
- Ratings : `Three` → `Three` (inchangé)
- Suppression des espaces inutiles

✅ **Pipeline en 3 étapes** : Extraction → Transformation → Sauvegarde

✅ **Logging complet** :
- Fichier : `/data/scraper.log`
- Console : affichage en direct
- Niveaux : DEBUG, INFO, WARNING, ERROR

✅ **Exécution planifiée** : Cron lance le script chaque minute

✅ **Mode ajout CSV** : Les données s'accumulent (jamais remplacées)

✅ **Containerisé** : Docker pour une portabilité maximale

## 📋 Prérequis

- **Docker** (version 20.10+)
- **Docker Compose** (version 1.29+)
- **Git** (optionnel)

## 🚀 Installation

### 1. Cloner le projet

```bash
git clone https://github.com/votreusername/books-to-scrape.git
cd books-to-scrape
2. Vérifier la structure
Assure-toi que la structure est correcte :
.
├── src/
│   ├── logger.py
│   ├── main.py
│   ├── scraper.py
│   └── transform.py
├── Dockerfile
├── docker-compose.yml
├── crontab.sh
└── README.md
3. Lancer le projet
docker-compose up --build
Cela va :
Construire l'image Docker
Créer et lancer le container
Installer les dépendances Python
Démarrer cron
📖 Utilisation
Mode exécution unique (test)
docker-compose down
docker-compose up
Attends 2-3 minutes et le script s'exécutera une fois.
Mode exécution planifiée (production)
docker-compose up
Le script s'exécutera automatiquement chaque minute. Le container reste actif en continu.
Arrêter le container
docker-compose down
Vérifier l'état
docker ps
Tu dois voir le container livre_scraper avec le statut Up.
📊 Résultats
Fichiers générés
Les fichiers suivants sont créés dans le dossier ./data/ :
1. books.csv
Fichier CSV avec les livres scrappés.
Format :
date,time,title,price,rating,category
25-05-2026,21:53,A Light in the Attic,51.77,Three,Poetry
25-05-2026,21:53,Tango with Bears,49.2,Two,Mystery
25-05-2026,21:53,Sharp Objects,47.82,Four,Mystery
Mode : Ajout (chaque exécution ajoute 40 lignes)
Accumulation :
Après 1h : 2,400 lignes (60 exécutions × 40)
Après 1j : 57,600 lignes (1440 exécutions × 40)
2. scraper.log
Fichier log contenant tous les messages du pipeline.
Format :
2026-05-25 21:53:00,112 INFO ========== DÉBUT DU PIPELINE ==========
2026-05-25 21:53:00,115 INFO ✓ URL correcte (nb=7) → https://books.toscrape.com
2026-05-25 21:53:01,540 INFO 20 livres récupérés sur la page 1
2026-05-25 21:53:02,651 INFO ✓ Scraping terminé — 40 livre(s) au total
2026-05-25 21:53:02,662 INFO ========== PIPELINE TERMINÉ ===========
Niveaux :
INFO : Messages importants
WARNING : Avertissements (non fatal)
ERROR : Erreurs avec traceback complet

🏗️ Architecture
Structure du pipeline
EXTRACTION (scraper.py)
    ↓ (4 protections)
Récupérer 40 livres bruts
    ↓
TRANSFORMATION (transform.py)
    ↓
Nettoyer les données
    ↓
SAUVEGARDE (main.py)
    ↓
Ajouter dans CSV
    ↓
LOGS (logger.py)
    ↓
Enregistrement dans fichier + console
4 niveaux de protection
Requête HTTP : Vérifier la connexion (try/except)
Statut HTTP : Vérifier le code 200
Pagination : Vérifier qu'il y a des livres
Extraction : Gestion d'erreur par livre
Fichiers sources
Fichier	Rôle	Responsabilité
logger.py	Configuration logs	Centraliser le logging
scraper.py	Extraction	Récupérer les livres du site
transform.py	Nettoyage	Transformer les données
main.py	Orchestration	Coordonner les 3 étapes
🔧 Configuration
Modifier le nombre de pages
Dans main.py, change num_pages :
books_data = scrape_all_books(base_url, num_pages=5)  # 5 pages au lieu de 2
Modifier la fréquence CRON
Dans crontab.sh, change la ligne :
# Toutes les minutes (actuellement)
* * * * * /usr/local/bin/python3 /app/main.py

# Toutes les 5 minutes
*/5 * * * * /usr/local/bin/python3 /app/main.py

# Toutes les heures
0 * * * * /usr/local/bin/python3 /app/main.py
📋 Logs
Afficher les logs en temps réel
# Windows PowerShell
Get-Content ./data/scraper.log -Wait -Tail 10

# Linux/Mac
tail -f ./data/scraper.log
Exemple de logs réussis
2026-05-25 21:53:00,112 INFO ========== DÉBUT DU PIPELINE ==========
2026-05-25 21:53:00,113 INFO Étape 1 : extraction en cours...
2026-05-25 21:53:00,115 INFO ✓ URL correcte (nb=7) → https://books.toscrape.com
2026-05-25 21:53:01,540 INFO 📖 Scraping page 1/2 → https://books.toscrape.com/index.html
2026-05-25 21:53:01,102 INFO 20 livres récupérés sur la page 1
2026-05-25 21:53:01,650 INFO 20 livres récupérés sur la page 2
2026-05-25 21:53:01,651 INFO ✓ Scraping terminé — 40 livre(s) au total
2026-05-25 21:53:01,652 INFO Étape 1 terminée — 40 livre(s) extrait(s)
2026-05-25 21:53:01,653 INFO Étape 2 : transformation en cours...
2026-05-25 21:53:01,654 INFO Étape 2 terminée — 40 livre(s) transformé(s)
2026-05-25 21:53:01,655 INFO Étape 3 : sauvegarde en cours...
2026-05-25 21:53:01,660 INFO 40 livre(s) sauvegardé(s) dans /data/books.csv
2026-05-25 21:53:01,661 INFO Étape 3 terminée — fichier CSV mis à jour
2026-05-25 21:53:01,662 INFO ========== PIPELINE TERMINÉ ===========
🐛 Dépannage
Le container s'arrête immédiatement
Cause : Erreur de syntaxe dans le Dockerfile
Solution : Vérifiez que la dernière ligne est :
CMD ["cron", "-f"]
Pas de logs dans scraper.log
Cause : Le container ne tourne pas
Solution :
docker ps  # Vérifier
docker-compose up  # Relancer
0 livre scrappé à chaque exécution
Cause : La simulation d'URL a choisi boktos.com (mauvaise URL - 50% de chance)
Solution : C'est normal ! Relancez le script jusqu'à avoir la bonne URL.
Le fichier result.output continue à être créé
Cause : La ligne cron n'a pas été commentée
Solution : Vérifiez crontab.sh :
# Correct (commenté)
# /usr/local/bin/python3 /app/main.py >> /data/result.output 2>&1
Erreur "tail : Le terme n'est pas reconnu" (Windows)
Cause : tail est une commande Linux, pas Windows
Solution : Utilisez PowerShell :
Get-Content ./data/scraper.log -Tail 10
📚 Documentation détaillée
Voir le fichier DOCUMENTATION_UTILISATION.md pour une documentation complète.
🔑 Concepts clés
Try/Except
Gère les erreurs sans arrêter le pipeline :
try:
    response = requests.get(page_url)
except Exception as e:
    logger.error("Erreur", exc_info=True)
    continue  # Passer à la page suivante
Mode ajout CSV
Chaque exécution ajoute des données (pas de remplacement) :
with open(filename, 'a') as csvfile:  # 'a' = append
    writer.writerows(books)
Logging centralisé
Un logger unique utilisé partout :
from logger import setup_logger
logger = setup_logger()
logger.info("message")
CRON
Exécute le script automatiquement :
* * * * * /usr/local/bin/python3 /app/main.py
📊 Statistiques
Métrique	Valeur
Livres par exécution	40
Fréquence	Chaque minute
Livres par heure	2,400
Livres par jour	57,600
Livres par mois	1,728,000
🛠️ Technologie utilisée
Python 3.9 : Langage de programmation
Docker : Containerisation
Requests : Requêtes HTTP
BeautifulSoup4 : Parsing HTML
Pandas : Manipulation de données
SQLAlchemy : ORM
Cron : Planification d'exécution
📝 Dépendances Python
requests>=2.28.0
beautifulsoup4>=4.11.0
pandas>=1.5.0
sqlalchemy>=2.0.0
📄 Licence
Ce projet est sous licence MIT.
👨‍💻 Auteur
Créé dans le cadre du cours Data Pipelines for AI à Eugenia School.
🤝 Contribution
Les contributions sont bienvenues !
📞 Support
Si vous avez des questions, consultez la section Dépannage ou ouvrez une issue sur GitHub.
🎓 Points d'apprentissage
Ce projet démontre :
Architecture de pipeline de données
Gestion robuste des erreurs
Logging et monitoring
Scraping web éthique
Containerisation Docker
Planification de tâches (Cron)
Transformation et nettoyage de données
