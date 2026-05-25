import csv
import os
from scraper import scrape_all_books, simulate_url
from transform import transform_books
from logger import setup_logger

# Initialiser le logger
logger = setup_logger()

def save_to_csv(books, filename='/data/books.csv'):
    """
    Sauvegarde les livres dans un fichier CSV en mode AJOUT (append)
    
    - Si le fichier n'existe pas : créer l'en-tête
    - Si le fichier existe : ajouter les nouvelles lignes sans re-écrire l'en-tête
    """
    
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    
    # Vérifier si le fichier existe
    file_exists = os.path.isfile(filename)
    
    # Ouvrir en mode ajout ('a' = append)
    with open(filename, 'a', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['date', 'time', 'title', 'price', 'rating', 'category']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        # Écrire l'en-tête SEULEMENT si le fichier est nouveau
        if not file_exists:
            writer.writeheader()
            logger.debug(f"En-tête CSV créé dans {filename}")
        
        # Écrire toutes les lignes des livres
        writer.writerows(books)
        
        logger.info(f"{len(books)} livre(s) sauvegardé(s) dans {filename}")

def main():
    """
    Pipeline complet :
    Étape 1 : Extraction (scraping)
    Étape 2 : Transformation (nettoyage)
    Étape 3 : Sauvegarde (CSV)
    """
    
    logger.info("========== DÉBUT DU PIPELINE ==========")
    
    # ===== ÉTAPE 1 : EXTRACTION =====
    logger.info("Étape 1 : extraction en cours...")
    
    # Simuler l'URL (1 fois sur 2 = mauvaise URL)
    base_url = simulate_url()
    
    try:
        # Scraper les livres (5 pages)
        books_data = scrape_all_books(base_url, num_pages=5)
        logger.info(f"Étape 1 terminée — {len(books_data)} livre(s) extrait(s)")
    
    except Exception as e:
        logger.error("Étape 1 : erreur fatale lors du scraping", exc_info=True)
        logger.warning("⚠️  Aucun livre extrait — pipeline interrompu")
        return
    
    # Vérifier qu'on a bien extrait des livres
    if not books_data:
        logger.warning("⚠️  Aucun livre extrait — pipeline interrompu sans sauvegarde")
        return
    
    # ===== ÉTAPE 2 : TRANSFORMATION =====
    logger.info("Étape 2 : transformation en cours...")
    
    try:
        # Nettoyer et valider les données
        books_transformed = transform_books(books_data)
        logger.info(f"Étape 2 terminée — {len(books_transformed)} livre(s) transformé(s)")
    
    except Exception as e:
        logger.error("Étape 2 : erreur fatale lors de la transformation", exc_info=True)
        logger.warning("⚠️  Les données n'ont pas pu être transformées — pipeline interrompu")
        return
    
    # ===== ÉTAPE 3 : SAUVEGARDE =====
    logger.info("Étape 3 : sauvegarde en cours...")
    
    try:
        # Sauvegarder dans le CSV (mode ajout)
        save_to_csv(books_transformed, filename='/data/books.csv')
        logger.info("Étape 3 terminée — fichier CSV mis à jour")
    
    except Exception as e:
        logger.error("Étape 3 : erreur fatale lors de la sauvegarde", exc_info=True)
        logger.warning("⚠️  Les données n'ont pas pu être sauvegardées")
        return
    
    logger.info("========== PIPELINE TERMINÉ ==========")

if __name__ == '__main__':
    main()