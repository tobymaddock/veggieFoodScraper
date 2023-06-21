""" scraper to extract *veggie* recipes by highest amount of protein using asynchronous requests """

from async_manager.request_manager import protein_fetcher
from scrapers.bbc_good_food import bbc_good_food_scraper

scraper = bbc_good_food_scraper()
newManager = protein_fetcher(scraper)
newManager.start_fetching_data()
