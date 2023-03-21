import requests
from bs4 import BeautifulSoup
import pandas as pd

base_url = 'https://www.amazon.in/s?k=bags&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_{}'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

all_products = []

for i in range(1, 21): # scraping 20 pages
    url = base_url.format(i)
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.content, 'lxml')
    
    products = soup.select('div[data-component-type="s-search-result"]')

    for product in products:
        try:
            product_url = 'https://www.amazon.in' + product.select_one('a.a-link-normal.s-no-outline')['href']
            product_name = product.select_one('span.a-size-medium.a-color-base.a-text-normal').text.strip()
            product_price = product.select_one('span.a-price-whole').text.strip()
            product_rating = product.select_one('span.a-icon-alt').text.strip().split()[0]
            product_reviews = product.select_one('span.a-size-base.s-underline-text').text.strip().split()[0]
            
            all_products.append({
                'url': product_url,
                'name': product_name,
                'price': product_price,
                'rating': product_rating,
                'reviews': product_reviews
            })
        except:
            pass
        
products = pd.DataFrame(all_products)
print(products)

products.to_csv('products.csv', index=False, encoding='utf-8')