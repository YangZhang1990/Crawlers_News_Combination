import threading
import time
from Queue import Queue
from urlSpider import urlSpider
from general import *

NUMBER_OF_THREADS = 6



project_name2 = 'bbc'
homepage2 = 'http://www.bbc.com/news/world'
domain_name2 = 'bbc.com/news'
#queue_file1 = project_name1+ '/'+project_name1+'_queue.txt'
urlSpider2= urlSpider(project_name2,homepage2,domain_name2)

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
		
def sleeptime(hour,min,sec):
	return hour*3600 + min*60 + sec

second = sleeptime(0,0,10)
while 1==1:
	time.sleep(second)
	print '================Start Crawling================='
	create_workers(urlSpider2)
	crawl(urlSpider2)
