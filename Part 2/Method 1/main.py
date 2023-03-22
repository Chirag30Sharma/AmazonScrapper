import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

# Set up options for headless browsing
options = Options()
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome(options=options)

# Read the CSV file into a Pandas DataFrame
df = pd.read_csv('amazon_bags.csv')

# Create empty lists to store the scraped data
descriptions = []
asins = []
product_descriptions = []
manufacturers = []

# Loop through each URL in the DataFrame and scrape the required information
for url in df['URL']:
    # Load the URL
    driver.get(url)
    
    # Parse the HTML with BeautifulSoup
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    
    # Scrape the product information
    description_tag = soup.find('span', {'id': 'productTitle'})
    if description_tag:
        description = description_tag.text.strip()
    else:
        description = ''
    
    asin_tag = soup.find('div', {'data-asin': True})
    if asin_tag:
        asin = asin_tag['data-asin']
    else:
        asin = ''
    
    product_description_tag = soup.find('div', {'id': 'productDescription'})
    if product_description_tag:
        product_description = product_description_tag.text.strip()
    else:
        product_description = ''
    
    manufacturer_tag = soup.find('a', {'id': 'bylineInfo'})
    if manufacturer_tag:
        manufacturer = manufacturer_tag.text.strip()
    else:
        manufacturer = ''
    
    # Append the scraped data to the corresponding lists
    descriptions.append(description)
    asins.append(asin)
    product_descriptions.append(product_description)
    manufacturers.append(manufacturer)

# Close the Chrome driver
driver.quit()

# Add the scraped data to the original DataFrame
df['description'] = descriptions
df['asin'] = asins
df['product_description'] = product_descriptions
df['manufacturer'] = manufacturers

df.to_csv('product_bags.csv', index=False)

# Print the updated DataFrame
print(df)
