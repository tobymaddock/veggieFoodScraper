from abc import ABC
from bs4 import BeautifulSoup
import requests
import json
from scrapers._utils import extract_number_from_string
from scrapers.abstract_scraper import base_scraper
class bbc_good_food_scraper(base_scraper):

    URLs = ["https://www.bbcgoodfood.com/recipes/collection/high-protein-vegan-recipes?page=1",
            "https://www.bbcgoodfood.com/recipes/collection/high-protein-vegan-recipes?page=2",
            "https://www.bbcgoodfood.com/recipes/collection/high-protein-vegan-recipes?page=3"]

    def return_websites(self):
        base_url = "https://www.bbcgoodfood.com"
        job_hyperlinks = []

        for URL in self.URLs:
            page = requests.get(URL)
            soup = BeautifulSoup(page.content, "html.parser")
            list_of_links = soup.find(class_="dynamic-list__list list")
            a_tags = list_of_links.find_all("a", class_="link d-block", href=True)
            for a in a_tags:
                job_hyperlinks.append(base_url + a['href'])

        return job_hyperlinks

    def scrape_protein(self, page_to_examine):
        new_soup = BeautifulSoup(page_to_examine, "html.parser")
        new_soup = new_soup.find(class_="js-site-main site-main body-background fluid-container")
        page_dict = json.loads("".join(new_soup.find("script", {"type": "application/ld+json"}).contents))
        protein_content = page_dict["nutrition"]["proteinContent"]
        protein_content = extract_number_from_string(protein_content)

        return [page_dict["headline"], protein_content]
