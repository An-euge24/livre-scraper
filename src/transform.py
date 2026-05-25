from datetime import datetime

def transform_books(books_data):
    """
    Transforme et nettoie les données des livres scrapés
    """
    
    # Mapping des ratings textuels vers des valeurs numériques
    ratings = {
        'One': '1',
        'Two': '2',
        'Three': '3',
        'Four': '4',
        'Five': '5'
    }
    
    # Transformer chaque livre
    for book in books_data:
        
        if 'price' in book and isinstance(book['price'], str):
            book['price'] = book['price'].replace('£', '').strip()
        
        if 'title' in book:
            book['title'] = book['title'].strip()
        
        if 'category' in book:
            book['category'] = book['category'].strip()
    
    return books_data