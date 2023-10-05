import requests
from bs4 import BeautifulSoup
from ..models import Book


def transcribe_ciela(promt):
    
    return promt.replace(' ', '+')

def search_ciela(title_promt, autor_promt):
    search_results = []

    # Define the URL of the bookstore to scrape
    bookstore_url = f'https://www.ciela.com/catalogsearch/result/index/?q={transcribe_ciela(title_promt)}'

    response = requests.get(bookstore_url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        # Extract relevant information from the HTML page using BeautifulSoup
        
        products_ol = soup.find('ol', class_='products list items product-items row')
        search_results = products_ol.find_all('li', class_='item product product-item')

        product_info = {}
        for result in search_results:
        	# Extract product name and link
            product_name_element = result.find('strong', class_='product name product-item-name')
            title = product_name_element.a.text.strip()
            link = product_name_element.a['href']

            # Extract author info
            author_info_element = result.find('div', class_='author-info')
            if author_info_element.a:
                author = author_info_element.a.text.strip()
            else:
                author = ''

            # Validate author and title
            if (autor_promt.lower() != author.lower()) or (title_promt.lower() not in title.lower()):
                continue

            product_info['title'] = title
            product_info['author'] = author
            
            # Extract publisher info
            publisher_info_element = result.find('div', class_='publisher-info')
            if publisher_info_element.a:
                product_info['publisher'] = publisher_info_element.a.text.strip()
            else:
                product_info['publisher'] = ''

            # Extract price
            product_info['price'] = result.select_one('span.price-wrapper')['data-price-amount']
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
