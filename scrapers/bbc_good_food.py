""" scraper to extract *veggie* recipes by highest amount of protein using asynchronous requests """

import requests
from bs4 import BeautifulSoup
from tabulate import tabulate
import json
import re
import asyncio
from time import perf_counter
import aiohttp
from scrapers._utils import extract_number_from_string

async def fetch(s, url):
    """ gathers protein from page using the 'await' keyword as to allow for this to be done
        asynchronously """

    async with s.get(url) as r:
        # wait for page text to become available
        page_to_examine = await r.text()
        new_soup = BeautifulSoup(page_to_examine, "html.parser")
        new_soup = new_soup.find(class_="js-site-main site-main body-background fluid-container")
        page_dict = json.loads("".join(new_soup.find("script", {"type": "application/ld+json"}).contents))
        protein_content = page_dict["nutrition"]["proteinContent"]
        protein_content = extract_number_from_string(protein_content)
        return [page_dict["headline"], url, protein_content]


async def fetch_all(s, urls):
    """ based on the list of urls, this function asynchronously gathers protein data for each
        website """

    tasks = []
    for url in urls:
        task = asyncio.create_task(fetch(s, url))
        tasks.append(task)
    res = await asyncio.gather(*tasks)
    return res


async def main(urls):
    """ calling this function creates a session """

    async with aiohttp.ClientSession() as session:
        htmls = await fetch_all(session, urls)

    recipes_data = sorted(htmls, key=lambda x: x[2], reverse=True)
    table = tabulate(recipes_data, headers=["Recipe", "Link", "Protein content/g"], tablefmt="fancy_grid")
    print(table)



if __name__ == '__main__':
    start = perf_counter()

    URLs = ["https://www.bbcgoodfood.com/recipes/collection/high-protein-vegan-recipes?page=1",
           "https://www.bbcgoodfood.com/recipes/collection/high-protein-vegan-recipes?page=2",
            "https://www.bbcgoodfood.com/recipes/collection/high-protein-vegan-recipes?page=3"]

    base_url = "https://www.bbcgoodfood.com"
    job_hyperlinks = []

    for URL in URLs:
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, "html.parser")
        list_of_links = soup.find(class_="dynamic-list__list list")
        a_tags = list_of_links.find_all("a", class_="link d-block", href=True)
        for a in a_tags:
            job_hyperlinks.append(base_url + a['href'])

    print(len(job_hyperlinks))

    # send request to main()
    asyncio.run(main(job_hyperlinks))

    stop = perf_counter()
    print("time taken:", stop - start)
