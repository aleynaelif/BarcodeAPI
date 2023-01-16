import json
import logging
import pandas as pd

from time import sleep

from bs4 import BeautifulSoup
from translate import Translator

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.remote.remote_connection import LOGGER

from utils import regex_description



class Scraper:

    def __init__(self, delay = 2):

        options = webdriver.ChromeOptions()
        options.add_argument("--no-sandbox")
        options.add_argument("--headless")
        options.add_argument("--single-process")
        options.add_argument("--ignore-certificate-errors")
        options.add_argument("--incognito")
        self.driver = webdriver.Chrome(service = Service(ChromeDriverManager().install()), 
                                  options=options)

        self.translator = Translator(to_lang = 'tr')

        self.delay = delay



    def get_soup(self, link):
        try:
            self.driver.get(link)
            sleep(self.delay)
            soup = BeautifulSoup(self.driver.page_source, "html.parser")
            logging.info("GET: {}".format(link))
            return soup
        except WebDriverException as we:
            logging.error("Unexpected Error: {}".format(we.stacktrace))
            return None



    def find_barcode(self, barcode):
        link = "https://barcode-list.com/barcode/EN/Search.htm?barcode={}".format(barcode)
        soup = self.get_soup(link)

        table_soup = soup.find_all("table", {"class": "randomBarcodes"})

        try:
            table = str(table_soup[0])
            data = pd.read_html(table)[0]
            keywords = data['Product Name'].values
            logging.info("The Product is {}".format(keywords[0]))
            logging.info("All Products: {}".format(keywords))
            return keywords[0]
        except Exception as e:
            logging.error("Couldn't find any product. {}".format(e))
            return None



    def product_info(self, keyword):

        # Search Product
        link = 'https://www.migros.com.tr/arama?q={}'.format(keyword)
        soup = self.get_soup(link)
        
        try:
            products_soup = soup.find_all("fe-product-image")
            product = products_soup[0].a.get('href')
        except Exception as e:
            logging.error("{}, {}".format(link, e))
            product = None
        
        # Product Page
        link = "https://www.migros.com.tr/{}".format(product)
        soup = self.get_soup(link)

        try:
            script_soup = soup.find_all("script", {"type" : "application/ld+json"})[0]
            json_data = json.loads(script_soup.string)
        except Exception as e:
            logging.error("{}, {}".format(link, e))
            json_data = None

        return json_data



    def run(self, barcode):
        keyword    = self.find_barcode(barcode)
        keyword_tr = self.translator.translate(keyword)
        data       = self.product_info(keyword_tr)
        info       = regex_description(keyword_tr, data)
        return info


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--barcode')
    opt = parser.parse_args()

    sc = Scraper(delay = 1)
    info = sc.run(opt.barcode)
    print(info)