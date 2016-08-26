import threading
from Queue import Queue
from urlSpider import urlSpider
from general import *
import time

NUMBER_OF_THREADS = 1

project_name1 = 'fox'
homepage1 = 'http://www.foxnews.com/'
domain_name1 = get_domain_name(homepage1)
#queue_file1 = project_name1+ '/'+project_name1+'_queue.txt'
urlSpider1= urlSpider(project_name1,homepage1,domain_name1)

queue= Queue(maxsize=0)
#create workder threads(will die when main exits)
def create_workers(urlSpider):
	for _ in range(NUMBER_OF_THREADS):
		t = threading.Thread(target= work, args=(urlSpider,))
		t.daemon= True
		t.start()

#do the next job in the queue
def work(urlSpider):
	while True:
		url= queue.get()
		urlSpider.crawl_page_urls(threading.current_thread().name,url)
		queue.task_done()

#each queued link is a new job
def create_jobs(urlSpider):
	for link in file_to_set(urlSpider.queue_file):
		queue.put(link)
	queue.join()
	crawl(urlSpider)

#check if there are items in the queue, if so crawl them
def crawl(urlSpider):
	queued_links = set()
	queued_links = file_to_set(urlSpider.queue_file)
	if len(queued_links)>0:
		print(str(len(queued_links))+' links in the queue')
		create_jobs(urlSpider)


create_workers(urlSpider1)
crawl(urlSpider1)

