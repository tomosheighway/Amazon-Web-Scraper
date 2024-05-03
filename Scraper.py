import requests
from bs4 import BeautifulSoup
import csv

def get_amazon_product_info(url):
    try:
        response = requests.get(url)
        
        # Check if successful code 
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            
            #title
            title_element = soup.find('span', {'id': 'productTitle'})
            title = title_element.get_text().strip() if title_element else "Title not found"
            
            #price
            price_whole_element = soup.find('span', {'class': 'a-price-whole'})
            price_fraction_element = soup.find('span', {'class': 'a-price-fraction'})
            price_symbol_element = soup.find('span', {'class': 'a-price-symbol'})
            price = price_symbol_element.get_text().strip() + price_whole_element.get_text().strip() + price_fraction_element.get_text().strip()
        
            #rating
            rating_element = soup.find('span', {'class': 'a-icon-alt'})
            rating = rating_element.get_text().strip() if rating_element else "Rating not available"
            
            #number reviews 
            num_reviews_element = soup.find('span', {'id': 'acrCustomerReviewText'})
            num_reviews = num_reviews_element.get_text().strip() if num_reviews_element else "Number of reviews not available"
            
            return {
                'title': title,
                'price': price,
                'rating': rating,
                'num_reviews': num_reviews
            }
        else:
            #error code for reason of fail
            print("Failed to retrieve the page. Status code:", response.status_code)
            return None
        
    except Exception as e:
        print("An error occurred:", str(e))
        return None

# Add product info to CSV 
def write_to_csv(filename, product_info):
    fields = ['title', 'price', 'rating', 'num_reviews']
    with open(filename, 'a', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fields)
        if csvfile.tell() == 0:
            writer.writeheader()
        writer.writerow(product_info)

# checks if product title already in the csv 
def product_exists_in_csv(filename, product_title):         
    try:
        with open(filename, 'r', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if row['title'] == product_title:
                    return True
            return False
    except FileNotFoundError:
        return False

#Updates the product info with newest details from most recent scrape        
def update_csv(filename, product_info):
    updated = False
    rows = []
    with open(filename, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['title'] == product_info['title']:
                row['price'] = product_info['price']
                row['rating'] = product_info['rating']
                row['num_reviews'] = product_info['num_reviews']
                updated = True
            rows.append(row)
    
    if updated:
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=reader.fieldnames)
            writer.writeheader()
            writer.writerows(rows)

product_urls = [
    "https://www.amazon.com/dp/B0CCRP85TR/ref=sspa_dk_detail_2?psc=1&pd_rd_i=B0CCRP85TR&pd_rd_w=8J0l0&content-id=amzn1.sym.eb7c1ac5-7c51-4df5-ba34-ca810f1f119a&pf_rd_p=eb7c1ac5-7c51-4df5-ba34-ca810f1f119a&pf_rd_r=89CXFAHKPEGJG5G6F0T8&pd_rd_wg=GLH2h&pd_rd_r=8ec25787-3a4a-456f-adc9-3b1e83b0c96e&s=pc&sp_csd=d2lkZ2V0TmFtZT1zcF9kZXRhaWw",
    "https://www.amazon.com/Raspberry-Pi-MS-014-1-8GHz-64-bit-Quad-Core/dp/B07TD42S27/",
    "https://www.amazon.com/dp/B09S11Q684/ref=sspa_dk_detail_2?psc=1&pd_rd_i=B09S11Q684&pd_rd_w=uvOsA&content-id=amzn1.sym.bea09237-ea55-4178-b48e-12d729325a93&pf_rd_p=bea09237-ea55-4178-b48e-12d729325a93&pf_rd_r=Y8NFMZY70GBMEJYYGYFN&pd_rd_wg=4stFS&pd_rd_r=4bf965d9-4248-4bfc-9964-c6560244e96e&s=pc&sp_csd=d2lkZ2V0TmFtZT1zcF9kZXRhaWxfdGhlbWF0aWM",
]

for url in product_urls:
    product_info = get_amazon_product_info(url)
    if product_info:
        filename = 'product_info.csv'

        #check if product already in CSV file then update or add it to CSV 
        if product_exists_in_csv(filename, product_info['title']):
            update_csv(filename, product_info)
            print(f"Product '{product_info['title']}' info updated in CSV.")
        else:
            write_to_csv(filename, product_info)
            print(f"Product '{product_info['title']}' added to CSV.")
    else:
        print("Failed to get product information.")