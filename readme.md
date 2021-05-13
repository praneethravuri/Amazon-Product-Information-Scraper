# **Amazon Product Information Scraper**

## **Libraries Required**:
* **time**
* **csv**
* **bs4**
* **selenium**
* **requests**
* **webdriver_manager**

 This script asks for a product to be searched and scrapes through all the available pages and enters the _**product name/description**_, _**price**_, _**ratings**_, _**number of reviews**_ and _**product url**_.

 A new _**CSV**_ file is created for each product. Some of the products may not have the reviews, price or number of ratings and are denoted as _**N/A**_ in the _**CSV**_ file.

 Amazon has a maximum number of _**20**_ pages for each product and the script goes through all the pages. Sometimes, the number of pages might be less than _**20**_ but the script will continue to run. It won't affect the performance of the program. I will try to add a function to detect the maximum number of pages.

 The second script _**main_v1.1.py**_ has a bit more functionality like calculating the _**time**_ it took to extract and printing messages.

![Example Image](sample.png)

**Disclaimer**: The script sometimes will show products that are not related to your search preferences because they might be sponsered posts and the rating counts of all the products scraped might be **N/A**. Close the editor and try again and it will work. The reason for this unknown to me. I will try to add a function to detect the maximum number of pages for the product searched later.

[Github - Praneeth Ravuri](https://github.com/praneethravuri)

[Amazon Product Scraper V1.0](https://github.com/praneethravuri/Amazon-Product-Info-Scraper/blob/main/main_v1.0.py)

[Amazon Product Scraper V1.1](https://github.com/praneethravuri/Amazon-Product-Info-Scraper/blob/main/main_v1.1.py)