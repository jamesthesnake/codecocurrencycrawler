import requests
from bs4 import BeautifulSoup
import time
import concurrent.futures

MAX_WORKERS = 10

def get_story_urls():
    BASE_URL = "https://news.ycombinator.com/"

    r = requests.get(BASE_URL)
    soup = BeautifulSoup(r.content, "html.parser")

    story_links = soup.find_all("a", attrs={"class": "storylink"})
    urls = [x["href"] for x in story_links]

    return urls


def scrape_story_url(url):
    r = requests.get(url)


if __name__ == "__main__":
    story_urls = get_story_urls()

    t0 = time.time()
    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = list()
        for story_url in story_urls:
            futures.append(executor.submit(scrape_story_url, url=story_url))

        results = list()
        for future in concurrent.futures.as_completed(futures):
            results.append(future.result())            

    t1 = time.time()

    print(f"{t1-t0} seconds to download {len(story_urls)} urls")
