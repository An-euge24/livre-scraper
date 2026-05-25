import logging
import os

def setup_logger():
    """
    Configure le système de logs unique pour tout le projet
    - Sortie fichier: /data/scraper.log (tous les logs)
    - Sortie console: seulement les INFO et plus (pas les DEBUG)
    """
    
    # Créer le dossier /data s'il n'existe pas
    os.makedirs('/data', exist_ok=True)
    
    # Récupérer le logger nommé 'scraper' (le même partout dans le projet)
    # Cela évite les doublons si on appelle setup_logger() plusieurs fois
    logger = logging.getLogger('scraper')
    
    # Si le logger a déjà des handlers, ne rien faire (éviter les doublons)
    if logger.handlers:
        return logger
    
    # Définir le niveau minimum à DEBUG (on veut capturer TOUT)
    logger.setLevel(logging.DEBUG)
    
    # === SORTIE 1 : FICHIER ===
    # Créer un handler pour écrire dans /data/scraper.log
    file_handler = logging.FileHandler('/data/scraper.log', mode='a', encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)  # Écrire tous les niveaux dans le fichier
    
    # === SORTIE 2 : CONSOLE ===
    # Créer un handler pour afficher dans la console (stdout)
    #console_handler = logging.StreamHandler()
    #console_handler.setLevel(logging.INFO)  # Afficher seulement INFO et plus (pas DEBUG)
    
    # === FORMAT DES LOGS ===
    # Format : "2026-05-19 14:32:01,432 INFO message"
    # - %(asctime)s : date/heure avec millisecondes
    # - %(levelname)s : INFO, WARNING, ERROR, etc.
    # - %(message)s : le message du log
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    
    # Appliquer le format aux deux handlers
    file_handler.setFormatter(formatter)
    #console_handler.setFormatter(formatter)
    
    # Ajouter les handlers au logger
    logger.addHandler(file_handler)
    #logger.addHandler(console_handler)
    
    return logger