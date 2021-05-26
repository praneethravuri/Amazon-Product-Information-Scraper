import os
import time
from datetime import date
import csv
from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

"""
    Step1: Open the browser
    Step2: Search for the product 
    Step3: Extract the html content of all the products
    Step4: Extract the product description, price, ratings, reviews count and URL
    Step5: Record the product information in a product record list
    Step6: Repeat for all the pages
    Step7: Close the browser
    Step8: Write all the product's information in the product record list in the spreadsheet
"""


class AmazonProductScraper:
    def __init__(self):
        self.driver = None

    def open_browser(self):
        
        opt = Options()

        opt.add_argument("--disable-infobars")
        opt.add_argument("--disable-extensions")
        opt.add_argument('--log-level=OFF')
        opt.add_experimental_option('excludeSwitches', ['enable-logging'])

        url = "https://www.amazon.in/"
        self.driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=opt)
        # Website URL
        self.driver.get(url)
        print("\n>> The browser is open")

        # Wait till the page has been loaded
        time.sleep(3)

    def get_product_url(self):

        search_product_name = input(">> Enter the product to be searched: ").replace(" ", "+")

        # This is the product url format for all products
        product_url = "https://www.amazon.in/s?k={}&ref=nb_sb_noss"

        product_url = product_url.format(search_product_name)

        print(">> Product URL: ", product_url)

        # Go to the product webpage
        self.driver.get(product_url)
        # To be used later while navigating to different pages
        return [product_url, search_product_name, search_product_name]

    def extract_webpage_information(self):
        # Parsing through the webpage
        soup = BeautifulSoup(self.driver.page_source, 'html.parser')
        # List of all the html information related to the product
        search_results = soup.find_all('div', {'data-component-type': 's-search-result'})

        return search_results

    @staticmethod
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
                review_number = item.find('span', {'class': 'a-size-base'}).text
            except AttributeError:
                review_number = "N/A"

            # Store the product information in a tuple
            product_information = (description,  product_price[1:], product_review, review_number, product_url)

            # Store the information in a temporary record
            temporary_record.append(product_information)
    
        return temporary_record

    def navigate_to_other_pages(self, product_details):
        # Contains the list of all the product's information
        records = []

        product_url = product_details[0]
        search_product_name = product_url[1]

        print("\n>> Page 1 - webpage information extracted")

        number_of_pages = self.driver.find_element_by_xpath("(//li[@class='a-disabled'])[3]")

        for i in range(2, int(number_of_pages.text)+1):
            # Goes to next page
            next_page_url = product_url+ "&page=" + str(i)
            self.driver.get(next_page_url)

            # Webpage information is stored in search_results
            search_results = self.extract_webpage_information()
            temporary_record = self.extract_product_information(search_results)

            extraction_information = ">> Page {} - webpage information extracted"
            print(extraction_information.format(i))

            for j in temporary_record:
                records.append(j)

        self.driver.close()

        return records

    @staticmethod
    def product_information_spreadsheet(records, product_details):

        today = date.today().strftime("%d-%m-%Y")

        for _ in records:

            searched_product = product_details[-1]

            file_name = "{}_{}.csv".format(searched_product, today)
            f = open(file_name, "w", newline='', encoding='utf-8')
            writer = csv.writer(f)
            writer.writerow(['Description', 'Price', 'Rating', 'Review Count', 'Product URL'])
            writer.writerows(records)
            f.close()

        message = ("\n>> Information about the product '{}' is stored in {}").format(searched_product, file_name)

        print(message)

        os.startfile(file_name)


if __name__ == "__main__":

    my_amazon_bot = AmazonProductScraper()

    my_amazon_bot.open_browser()

    product_details = my_amazon_bot.get_product_url()

    my_amazon_bot.extract_product_information(my_amazon_bot.extract_webpage_information())

    navigation = my_amazon_bot.navigate_to_other_pages(product_details)

    my_amazon_bot.product_information_spreadsheet(navigation, product_details)
