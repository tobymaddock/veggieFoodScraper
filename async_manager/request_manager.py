""" Handles asychronous requests for any input scraper """
import requests
from bs4 import BeautifulSoup
from tabulate import tabulate
import json
import re
from time import perf_counter
from scrapers._utils import extract_number_from_string
import asyncio
import aiohttp


class protein_fetcher:

    def __init__(self, scraper):
        self.scraper = scraper

    async def fetch(self, s, url):
        """ gathers protein from page using the 'await' keyword as to allow for this to be done
            asynchronously """

        async with s.get(url) as r:
            # wait for page text to become available
            page_to_examine = await r.text()
            res = self.scraper.scrape_protein(page_to_examine)
            return [res[0], url, res[1]]

    async def fetch_all(self, s, urls):
        """ based on the list of urls, this function asynchronously gathers protein data for each
            website """

        tasks = []
        for url in urls:
            task = asyncio.create_task(self.fetch(s, url))
            tasks.append(task)
        res = await asyncio.gather(*tasks)
        return res

    async def main(self, urls):
        """ calling this function creates a session """

        async with aiohttp.ClientSession() as session:
            htmls = await self.fetch_all(session, urls)

        recipes_data = sorted(htmls, key=lambda x: x[2], reverse=True)
        table = tabulate(recipes_data, headers=["Recipe", "Link", "Protein content/g"], tablefmt="fancy_grid")
        print(table)

    def start_fetching_data(self):
        hyperlinks = self.scraper.return_websites()
        asyncio.run(self.main(hyperlinks))





