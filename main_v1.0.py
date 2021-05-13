import time
import csv
from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.firefox import GeckoDriverManager as gdm
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException, WebDriverException

"""
    Step1: Open the brower
    Step2: Search for the product 
    Step3: Extract the html content of all the products
    Step4: Extract the product description, price, ratings, reviews count and URL
    Step5: Record the product information in a product record list
    Step6: Repeat for all the pages
    Step7: Close the browser
    Step8: Write all the product's information in the product record list in the spreadsheet
"""



"""Step 1"""
def open_browser():
    #Install geckodriver for firefox
    global driver
    driver = webdriver.Firefox(executable_path=gdm().install())
    # Website URL
    driver.get("https://www.amazon.in/")
    # Wait till the page has been loaded
    time.sleep(3)



"""Step 2"""
def get_product_url(driver, search_product_name):
    # This is the product url format for all products
    product_url = "https://www.amazon.in/s?k={}&ref=nb_sb_noss"
    # Replace the spaces with + signs to create a valid searchable url
    search_product_name = search_product_name.replace(" ", "+")
    product_url = product_url.format(search_product_name)
    # Go to the product webpage
    driver.get(product_url)
    # To be used later while navigating to different pages
    return product_url



"""Step 3"""
def extract_webpage_information():
    # Parsing through the webpage
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    # List of all the html information related to the product
    search_results = soup.find_all('div', {'data-component-type': 's-search-result'})
    return search_results



"""Step 4 and 5"""
def extract_product_information(search_results):
    temporary_record = []
    for i in range(len(search_results)):
        item = search_results[i]

        # Find the a tag of the item
        atag_item = item.h2.a

        # Name of the item
        description = atag_item.text.strip()

        # Get the url of the item
        product_url = "https://www.amazon.in/" + atag_item.get('href')

        
        # Get the price of the product
        try:
            product_price_location = item.find('span', 'a-price')
            product_price = product_price_location.find('span', 'a-offscreen').text
        except AttributeError:
            product_price = "N/A"

        # Get product reviews
        try:
            product_review = item.i.text.strip()
        except AttributeError:
            product_review = "N/A"

        # Get number of reviews
        try:
            review_number = item.find('span', {'class': 'a-size-base', 'dir':'auto'}).text
        except AttributeError:
            review_number = "N/A"

        product_information = (description,  product_price[1:], product_review, review_number, product_url)

        temporary_record.append(product_information)
    
    return temporary_record



"""Step 6 and 7"""
def navigate_to_other_pages(search_product_name):
    records = []
    for i in range(2,5):
        next_page_url = get_product_url(driver, search_product_name) + "&page=" + str(i)
        driver.get(next_page_url)
        search_results = extract_webpage_information()
        temporary_record = extract_product_information(search_results)
        for i in temporary_record:
            records.append(i)
    driver.close()
    return records



"""Step 8"""
def product_information_spreadsheet(records):
    for _ in records:
        with open("product_list.csv", "w", newline='', encoding='utf-8') as f:
                try:
                    writer = csv.writer(f)
                    writer.writerow(['Description', 'Price', 'Rating', 'Review Count', 'Product URL'])
                    writer.writerows(records)
                    
                except UnicodeEncodeError:
                    continue
        f.close()



def main():
    search_product_name = input("Enter the name of the product to be searched: ")
    search_product_name = search_product_name.replace(" ", "+")

    open_browser()

    get_product_url(driver,search_product_name)

    search_results = extract_webpage_information()

    extract_product_information(search_results)

    temp = navigate_to_other_pages(search_product_name)
    
    product_information_spreadsheet(temp)

    


if __name__ == "__main__":
    main()
