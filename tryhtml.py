import sys, threading, time, os, sys
from queue import Queue

from html.parser import HTMLParser
import urllib.request
from urllib.parse import urlparse, urlunparse, urljoin
import queue
import concurrent.futures 


dupcheck = set()  
dupcheck.add("https://www.openai.com")
q = Queue(100) 
q.put("https://www.openai.com") 
class HyperlinkParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.hyperlinks = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "a" and "href" in attrs:
            self.hyperlinks.append(attrs["href"])


def get_hyperlinks(url):
    """
    Takes in a URL and outputs all URLs clickable from it which are on the same domain
    """
    with urllib.request.urlopen(url) as response:
        if not response.info().get('Content-Type').startswith("text/html"):
            # Don't want to download zips, pdfs, etc.
            return []
        html = response.read().decode('utf-8')

    parser = HyperlinkParser()
    parser.feed(html)
    parsed = urlparse(url)
    results = []
    for link in parser.hyperlinks:
        parsed2 = urlparse(urljoin(url, link))
        if parsed2.netloc == parsed.netloc:
            results.append(urlunparse(parsed2))
    return results

"""
def queueURLs(links): 
    print(links,"adf")
    for link in links:
        print(link,len(links),links.index(link))
        if link in dupcheck:
            continue
        dupcheck.add(link)
        if len(dupcheck) > 99999: 
            dupcheck.clear()
        q.put(link) 
        q.task_done()

def getHTML(link): 
    print(link)
    try:
        links=get_hyperlinks(link)
        print(links)
        queueURLs(links) 
    except (KeyboardInterrupt, SystemExit): 
        raise
    except Exception:
        pass
while q:
    start=q.get()
    
    mythread=threading.Thread(target=getHTML,args=(str(start),))
    print("dumb")
    mythread.start()
    mythread.join()

    print(len(dupcheck))
    time.sleep(0.5)
    mythread.join()
print("hello")
"""
import concurrent.futures


def crawl(startUrl):
	s = set()
	s.add(startUrl)
	queue = [startUrl]
	while len(queue) > 0:
		queue2 = []
		with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
			l = list(executor.map(lambda url: get_hyperlinks(url), queue))
			for urls in l:
				for newUrl in urls:
					if newUrl in s:
						continue
					s.add(newUrl)
					print(len(s))
					queue2.append(newUrl)
			print(len(s))
		queue = queue2
	return list(s),len(s)
print(crawl("https://www.openai.com"))
