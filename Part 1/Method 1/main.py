from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

# set up Selenium
options = Options()
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--headless') # run in headless mode
driver = webdriver.Chrome(options=options)

# define function to scrape product info
def scrape_product_info(url):
    # load page
    driver.get(url)
    time.sleep(3) # wait for page to load
    
    # scrape data
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    products = soup.find_all('div', {'data-component-type': 's-search-result'})
    
    data = []
    for product in products:
        # product url
        url = 'https://www.amazon.in' + product.find('a', {'class': 'a-link-normal'})['href']
        
        # product name
        name = product.find('h2', {'class': 'a-size-mini'}).text.strip()
        
        # product price
        price = product.find('span', {'class': 'a-price-whole'})
        if price is not None:
            price = price.text.replace(',', '')
        else:
            price = ''
        
        # product rating
        rating = product.find('span', {'class': 'a-icon-alt'})
        if rating is not None:
            rating = rating.text.split()[0]
        else:
            rating = ''
        
        # number of reviews
        num_reviews = product.find('span', {'class': 'a-size-base s-underline-text'})
        if num_reviews is not None:
            num_reviews = num_reviews.text.split()[0]
        else:
            num_reviews = ''
        
        # add data to list
        data.append([url, name, price, rating, num_reviews])
    
    return data

# set up DataFrame to store data
columns = ['URL', 'Name', 'Price', 'Rating', 'NumReviews']
df = pd.DataFrame(columns=columns)

# scrape 20 pages of product listings
for i in range(1, 21):
    url = f'https://www.amazon.in/s?k=bags&page={i}'
    data = scrape_product_info(url)
    df = df.append(pd.DataFrame(data, columns=columns))

# output data to CSV file
df.to_csv('amazon_bags.csv', index=False)

# quit Selenium
driver.quit()
