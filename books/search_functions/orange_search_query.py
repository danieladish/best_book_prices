import requests
from bs4 import BeautifulSoup
from ..models import Book

def transcribe_orange(promt):
    
    return promt.replace(' ', '+')

def search_orange(title_promt, autor_promt):
    search_results = []

    # Define the URL of the bookstore to scrape
    bookstore_url = f'https://www.orangecenter.bg/catalogsearch/result/?q={transcribe_orange(title_promt)}'

    response = requests.get(bookstore_url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        # Extract relevant information from the HTML page using BeautifulSoup
        
        search_results = soup.find_all('a', class_='product-item-info')
        
        product_info = {}

        for result in search_results:
            # Extract title
            title_element = result.find('strong', class_='product-item-name')
            title = title_element.span.text.strip()

            # Extract author
            author_element = result.find('span', class_='product-item-subname')
            author = author_element.text.strip() if author_element else ""
            
            # Validate author and title
            if (autor_promt.lower() != author.lower()) or (title_promt.lower() not in title.lower()):
                continue
           
            # Extract price
            price_element = result.find('span', class_='price-wrapper')
            price = price_element['data-price-amount']
            
            # Extrcat link
            link = result['href']
        
            product_info['title'] = title
            product_info['author'] = author
            product_info['price'] = price
            product_info['link'] = link
            break
    
    # Check if the book already exists in the local database using the link
    if product_info:
        existing_book = Book.objects.filter(link=product_info['link']).first()

        if not existing_book:
            # Create a new instance of the Book model and save it to the database
            new_book = Book(
                title=product_info['title'],
                author=product_info['author'],
                price=product_info['price'],
                link=product_info['link']
            )
            new_book.save()

    return product_info

