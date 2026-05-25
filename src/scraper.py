import requests
from bs4 import BeautifulSoup
import time
import random
from datetime import datetime
from logger import setup_logger

# Initialiser le logger (disponible partout dans ce fichier)
logger = setup_logger()

# === SIMULATION D'URL ===
URL_REAL = 'https://books.toscrape.com'
URL_FAKE = 'https://boktos.com'  # URL invalide pour simuler les erreurs

def simulate_url():
    """
    Simule une erreur d'URL :
    - Tire un nombre aléatoire entre 1 et 10
    - Si le nombre est PAIR (2, 4, 6, 8, 10) = 5 chances sur 10 = 1 fois sur 2
      → retourne une mauvaise URL (boktos.com)
    - Si le nombre est IMPAIR (1, 3, 5, 7, 9) = 5 chances sur 10 = 1 fois sur 2
      → retourne la bonne URL (books.toscrape.com)
    """
    nb = random.randint(1, 10)
    logger.debug(f"Simulation URL — nb tiré : {nb}")
    
    if nb % 2 == 0:  # Nombre pair = mauvaise URL
        logger.warning(f"⚠️  URL simulée incorrecte (nb={nb}) → {URL_FAKE}")
        return URL_FAKE
    else:  # Nombre impair = bonne URL
        logger.info(f"✓ URL correcte (nb={nb}) → {URL_REAL}")
        return URL_REAL

def get_category(book_url):
    """
    Récupère la catégorie d'un livre en suivant le lien détail
    """
    clean_url = book_url.replace('../../../', '')
    
    # Déterminer l'URL de base selon l'URL simulée
    if 'boktos' in clean_url:
        category_url = clean_url
    else:
        category_url = f'{URL_REAL}/{clean_url}'
    
    try:
        response = requests.get(category_url, timeout=5)
        
        # === CONTRÔLE 2 : Vérifier le statut HTTP ===
        if response.status_code != 200:
            logger.warning(f"Statut HTTP {response.status_code} sur {category_url} — catégorie ignorée")
            return "Pas de catégorie"
        
        soup = BeautifulSoup(response.content, 'html.parser')
        category = soup.find('a', {'class': 'breadcrumb'})
        
        if category:
            return category.get_text(strip=True)
        else:
            return "Pas de catégorie"
    
    except Exception as e:
        # On log l'erreur mais on continue (ne pas s'arrêter sur une balise manquante)
        logger.debug(f"Erreur extraction catégorie sur {category_url} : {str(e)}")
        return "Pas de catégorie"

def scrape_all_books(base_url, num_pages=2):
    """
    Scrape les livres sur les pages 1 à num_pages
    
    Structure :
    1. Requête HTTP vers chaque page
    2. Extraction HTML avec BeautifulSoup
    3. Extraction des données (titre, prix, rating, catégorie)
    """
    
    logger.info(f"🚀 Début du scraping — {num_pages} page(s) — base URL : {base_url}")
    
    all_books = []
    
    for page_num in range(1, num_pages + 1):
        # Construire l'URL de la page
        if page_num == 1:
            page_url = f'{base_url}/index.html'
        else:
            page_url = f'{base_url}/catalogue/page-{page_num}.html'
        
        logger.info(f"📖 Scraping page {page_num}/{num_pages} → {page_url}")
        
        try:
            # === CONTRÔLE 1 : Requête HTTP ===
            # Si l'URL est invalide ou le serveur ne répond pas, ça lève une exception
            response = requests.get(page_url, timeout=10)
        
        except Exception as e:
            # Log l'erreur COMPLÈTE avec la pile (exc_info=True)
            # Cela affiche aussi le traceback (File "...", line X, in ...)
            logger.error(f"❌ [Page {page_num}] Connexion impossible : {page_url}", exc_info=True)
            # Continue vers la page suivante (ne pas s'arrêter ici)
            continue
        
        # === CONTRÔLE 2 : Vérifier le statut HTTP ===
        if response.status_code != 200:
            logger.warning(f"⚠️  [Page {page_num}] Statut HTTP {response.status_code} reçu — page ignorée")
            continue  # Passer à la page suivante
        
        # Parser la page HTML
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Trouver tous les livres (balise <article class='product_pod'>)
        books = soup.find_all('article', {'class': 'product_pod'})
        
        # === CONTRÔLE 3 : Vérifier la pagination ===
        if not books:
            logger.warning(f"⚠️  [Page {page_num}] Aucun livre trouvé — pagination terminée")
            break  # Arrêter le scraping (plus de pages)
        
        logger.info(f"   ✓ {len(books)} livre(s) détecté(s) sur la page {page_num}")
        
        # === CONTRÔLE 4 : Extraction de chaque livre ===
        for book in books:
            try:
                # Extraire le titre
                title = book.find('h3').find('a')['title']
                
                # Extraire le prix (avec symbole £ que le convertir en nombre)
                price_text = book.find('p', {'class': 'price_color'}).get_text(strip=True)
                price = price_text.replace('£', '')
                
                # Extraire le rating (Five, Four, Three, Two, One)
                rating_class = book.find('p', {'class': 'star-rating'})['class'][1]
                
                # Extraire la catégorie (via le lien détail)
                book_link = book.find('h3').find('a')['href']
                category = get_category(book_link)
                
                # Ajouter le livre à la liste
                all_books.append({
                    'date': datetime.now().strftime('%d-%m-%Y'),
                    'time': datetime.now().strftime('%H:%M'),
                    'title': title,
                    'price': price,
                    'rating': rating_class,
                    'category': category
                })
            
            except Exception as e:
                # Un livre a une structure HTML invalide : on le saute et on continue
                logger.error(f"❌ Erreur extraction livre sur page {page_num}", exc_info=True)
                continue  # Passer au livre suivant
        
        time.sleep(1)  # Pause pour ne pas surcharger le serveur
    
    logger.info(f"✓ Scraping terminé — {len(all_books)} livre(s) au total")
    return all_books