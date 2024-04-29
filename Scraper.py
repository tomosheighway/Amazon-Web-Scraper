import requests
from bs4 import BeautifulSoup

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
            price_symbol = soup.find('span', {'class': 'a-price-symbol'})
            #before_discount = soup.find('span', {'class': 'a-offscreen'})
            #print(before_discount.get_text().strip())
            price = price_symbol.get_text().strip() +price_whole_element.get_text().strip() + price_fraction_element.get_text().strip()
            
            #Not working 
            regular_price_element = soup.find("span", class_="a-price")
            regular_price = regular_price_element.find("span", class_="a-offscreen").text.strip()
            print(regular_price)

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


url = "https://www.amazon.com/dp/B0CCRP85TR/ref=sspa_dk_detail_2?psc=1&pd_rd_i=B0CCRP85TR&pd_rd_w=8J0l0&content-id=amzn1.sym.eb7c1ac5-7c51-4df5-ba34-ca810f1f119a&pf_rd_p=eb7c1ac5-7c51-4df5-ba34-ca810f1f119a&pf_rd_r=89CXFAHKPEGJG5G6F0T8&pd_rd_wg=GLH2h&pd_rd_r=8ec25787-3a4a-456f-adc9-3b1e83b0c96e&s=pc&sp_csd=d2lkZ2V0TmFtZT1zcF9kZXRhaWw"
#url = "https://www.amazon.com/Raspberry-Pi-MS-014-1-8GHz-64-bit-Quad-Core/dp/B07TD42S27/"
product_info = get_amazon_product_info(url)
if product_info:
    print("Product Title:", product_info['title'])
    print("Price:", product_info['price'])
    print("Rating:", product_info['rating'])
    print("Number of Reviews:", product_info['num_reviews'])
