from abc import ABC
from bs4 import BeautifulSoup
import requests
import json
from scrapers._utils import extract_number_from_string

class abstract_scraper(ABC):
    """ This abstract class forms the basis for subsequent scrapers to be used"""

    def return_websites(self):
        """scraper specific method to ensure websites are scraped"""
        pass

    def scrape_protein(self):
        """scraper specific method to ensure protein is appropriately scraped"""
        pass

class base_scraper(abstract_scraper):
    """ This class forms the basis for subsequent scrapers to be used"""


