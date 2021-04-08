import sys, threading, time, os, sys
from queue import Queue

from html.parser import HTMLParser
import urllib.request
from urllib.parse import urlparse, urlunparse, urljoin
import queue
import concurrent.futures 
import json
import time
from multiprocessing import Process, Value, Array




import concurrent.futures
with open('data.json') as f:
	data = json.load(f)
start=0
first_edges=[]
for edges in data:
	print(edges)
	try:
		start=data[edges]['start']
		first_edges.extend(list(data[edges]['edges'].items()))
		print(first_edges,[('B',5),('C',7)])
	except Exception as e:
		if start:
			break
		else:
			print('not found yet')
def get_edges(edge,start_time_first):
	start_time = time.time()

	time.sleep(edge[1])
	print(edge[0],time.time()-start_time,time.time()-start_time_first)
	print(first_edges)
	first_edges.remove(edge)
	return edge[0]
	

def crawl(startUrl):
		print(edges)
		futures=[]
		start_time = time.time()

		with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
				#futures.append(executor.submit(get_edges,edges=first_edges))
				while first_edges:
					futures = list(map(lambda url: executor.submit(get_edges,url,start_time), first_edges))   
					for future in concurrent.futures.as_completed(futures):           
						first_edges.extend(list(data[future.result()]['edges'].items()))
					print(first_edges)
					
					#futures.append(l)
		print(time.time()-start_time,"blesseD")
		#	print(future)
		#	try:
		#		print(future[0].results())
		#	except:
		#		print('done')
"""
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
"""
print(crawl("https://www.openai.com"))
