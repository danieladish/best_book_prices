from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from ..models import Book


def transcribe_ozone(promt):
    
    return promt.replace(' ', '%20')

def search_ozone(title_promt, autor_promt):
    product_info = {}

    # Set Chrome options for headless mode
    chrome_options = Options()
    chrome_options.add_argument("--headless")

    # Initialize the WebDriver with Chrome options
    driver = webdriver.Chrome(options=chrome_options)

    # Define the URL of the bookstore to scrape
    bookstore_url = f'https://www.ozone.bg/instantsearchplus/result/?q={transcribe_ozone(title_promt)}'

    driver.get(bookstore_url)

    # Find the list of <li> elements
    li_elements = driver.find_elements(By.CLASS_NAME, "isp_grid_product")

    for li in li_elements:
        # Extract title
        title_element = li.find_element(By.CLASS_NAME, "isp_product_title")
        title = title_element.text.strip()

        # Extract author
        try:
            author_element = li.find_element(By.CSS_SELECTOR, "span[style='color:#999;font-size: 14px;font-weight: normal;']")
            author = author_element.text.strip()
        except NoSuchElementException:
            author = ""

        # Remove the author information from the title and author heading\\
        title = title.replace(author, "").strip()
        if author.split(': ')[0] == "Издателство":
            author = ""
        elif author.split(': ')[0] == "Автор":
            author = author.split(': ')[1]

        # Validate author and title
        if (autor_promt.lower() != author.lower()) or (title_promt.lower() not in title.lower()):
            continue

        # Extract price
        price_element = li.find_element(By.CLASS_NAME, "isp_product_price")
        price = price_element.get_attribute("data-currency-bgn") 

        # Extract link
        link_element = li.find_element(By.CSS_SELECTOR, "a.isp_product_image_href")
        link = link_element.get_attribute("href")

        product_info['title'] = title
        product_info['author'] = author
        product_info['price'] = price
        product_info['link'] = link
        break

    driver.quit()

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
 

title_promt, author_promt = "Змей побратим", "Симона Панова"
expected_output = {'title': 'Змей побратим (Змей закрилник 2)', 'author': 'Симона Панова', 'price': '24.00', 'link': 'https://www.ozone.bg/product/zmey-pobratim-zmey-zakrilnik2'}
actual_output = search_ozone(title_promt, author_promt)
print(actual_output)