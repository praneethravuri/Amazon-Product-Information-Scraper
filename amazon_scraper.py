import os
import time
from datetime import date
import csv
from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException

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
        self.category_name = None
        self.formatted_category_name = None

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

        # Wait till the page has been loaded
        time.sleep(3)

    def get_category_url(self):

        self.category_name = input("\n>> Enter the product/category to be searched: ")

        self.formatted_category_name = self.category_name.replace(" ", "+")

        # This is the product url format for all products
        category_url = "https://www.amazon.in/s?k={}&ref=nb_sb_noss"

        category_url = category_url.format(self.formatted_category_name)

        print(">> Category URL: ", category_url)

        # Go to the product webpage
        self.driver.get(category_url)
        # To be used later while navigating to different pages
        return category_url

    def extract_webpage_information(self):
        # Parsing through the webpage
        soup = BeautifulSoup(self.driver.page_source, 'html.parser')
        # List of all the html information related to the product
        page_results = soup.find_all('div', {'data-component-type': 's-search-result'})

        return page_results

    @staticmethod
    def extract_product_information(page_results):
        temp_record = []
        for i in range(len(page_results)):
            item = page_results[i]

            # Find the 'a' tag of the item
            a_tag_item = item.h2.a

            # Name of the item
            description = a_tag_item.text.strip()

            # Get the url of the item
            category_url = "https://www.amazon.in/" + a_tag_item.get('href')

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
            product_information = (description, product_price[1:], product_review, review_number, category_url)

            # Store the information in a temporary record
            temp_record.append(product_information)

        return temp_record

    def navigate_to_other_pages(self, category_url):
        # Contains the list of all the product's information
        records = []

        print("\n>> Page 1 - webpage information extracted")

        try:

            max_number_of_pages = "//span[@class='s-pagination-item s-pagination-disabled']"

            number_of_pages = self.driver.find_element_by_xpath(max_number_of_pages)
            print("Maximum Pages: ", number_of_pages.text)
        except NoSuchElementException:
            max_number_of_pages = "//li[@class='a-normal'][last()]"
            number_of_pages = self.driver.find_element_by_xpath(max_number_of_pages)

        for i in range(2, int(number_of_pages.text) + 1):
            # Goes to next page
            next_page_url = category_url + "&page=" + str(i)
            self.driver.get(next_page_url)

            # Webpage information is stored in page_results
            page_results = self.extract_webpage_information()
            temp_record = self.extract_product_information(page_results)

            extraction_information = ">> Page {} - webpage information extracted"
            print(extraction_information.format(i))

            for j in temp_record:
                records.append(j)

        self.driver.close()

        print("\n>> Creating an excel sheet and entering the details...")

        return records

    def product_information_spreadsheet(self, records):

        today = date.today().strftime("%d-%m-%Y")

        for _ in records:
            file_name = "{}_{}.csv".format(self.category_name, today)
            f = open(file_name, "w", newline='', encoding='utf-8')
            writer = csv.writer(f)
            writer.writerow(['Description', 'Price', 'Rating', 'Review Count', 'Product URL'])
            writer.writerows(records)
            f.close()

        message = f">> Information about the product '{self.category_name}' is stored in {file_name}\n"

        print(message)

        os.startfile(file_name)


if __name__ == "__main__":
    my_amazon_bot = AmazonProductScraper()

    my_amazon_bot.open_browser()

    category_details = my_amazon_bot.get_category_url()

    my_amazon_bot.extract_product_information(my_amazon_bot.extract_webpage_information())

    navigation = my_amazon_bot.navigate_to_other_pages(category_details)

    my_amazon_bot.product_information_spreadsheet(navigation)
