import urllib
import urllib2
import os
from general import *
import requests
from bs4 import BeautifulSoup
from urlparse import urljoin
from dataconnet import *
from newsItem import *


class urlSpider:
	# Class variables shared among all instances
	#project_name =''
	project_name=''
	base_url= ''
	domain_name = ''
	queue_file =''
	crawled_file =''
	crawled_item_file=''
	queue = set()
	crawled_url = set()
	crawled_item = set()

	def __init__(self,project_name,base_url,domain_name):
		urlSpider.project_name= project_name
		urlSpider.base_url= base_url
		urlSpider.domain_name = domain_name
		urlSpider.queue_file = urlSpider.project_name + '/'+urlSpider.project_name + '_queue.txt'
		urlSpider.crawled_file = urlSpider.project_name+'/'+urlSpider.project_name + '_crawled.txt'
		urlSpider.crawled_item_file = urlSpider.project_name+'/'+urlSpider.project_name + '_crawledItems.txt'
		self.boot()
		self.crawl_page_urls('First Spider',urlSpider.base_url)

	@staticmethod
	def boot():
		create_project_dir(urlSpider.project_name)
		create_data_files(urlSpider.project_name,urlSpider.base_url)
		urlSpider.queue = file_to_set(urlSpider.queue_file)
		urlSpider.crawled_url = file_to_set(urlSpider.crawled_file)
		urlSpider.crawled_item = file_to_set(urlSpider.crawled_item_file)

	@staticmethod
	def crawl_page_urls(thread_name, page_url):
		
			if page_url not in urlSpider.crawled_url:
				#print(thread_name+ ' now crawling '+page_url)
				print('Queue: '+ str(len(urlSpider.queue)) + '| Crawled :'+str(len(urlSpider.crawled_item)))
				if len(urlSpider.crawled_item)<=500:
                                        if urlSpider.project_name =='bbc':
                                                urlSpider.add_links_to_queue_BBC(urlSpider.find_links(page_url))
                                        elif urlSpider.project_name=='fox':
                                                urlSpider.add_links_to_queue_fox(urlSpider.find_links(page_url))
					urlSpider.queue.remove(page_url)
					urlSpider.crawled_url.add(page_url)
					if urlSpider.project_name=='bbc':
					   news = urlSpider.find_PageItem_BBC(page_url)
					elif urlSpider.project_name=='fox':
                                                news = urlSpider.find_PageItem_Fox(page_url)  
					if news != None:
						urlSpider.crawled_item.add(page_url)
					else:
						print page_url
					urlSpider.update_files()
				else:
					deleteDupicatetRows()
					deleteFolder(urlSpider.project_name)
					print 'finished__'+urlSpider.project_name
					os._exit(-1)

	@staticmethod
	def find_links(base_url):
		try:
			r= requests.get(base_url)
			soup = BeautifulSoup(r.content,"lxml")
			original_links = soup.find_all('a')
			links=set()
			for link in original_links:
				full_url = urljoin(base_url,link.get('href'))
				#print full_url
				links.add(full_url)
		except:
			print('Error: can not crawl page')
			return set()
		return links
	@staticmethod
	def update_files():
		set_to_file(urlSpider.queue,urlSpider.queue_file)
		set_to_file(urlSpider.crawled_url,urlSpider.crawled_file)
		set_to_file(urlSpider.crawled_item,urlSpider.crawled_item_file)

	@staticmethod
	def add_links_to_queue_BBC(links):
		for url in links:
			#print url
			if url in urlSpider.queue:
				continue
			if url in urlSpider.crawled_url:
				continue
			if urlSpider.domain_name not in url:
				continue
			if '?intcmp=trending' in url:
                                continue
			if 'bbc.com/autos' in url:
				#print url
				continue
			if 'bbc.com/iplayer' in url:
				#print url
				continue
			if 'bbc.com/aboutthebbc' in url:
				#print url
				continue
			if 'bbc.com/blogs' in url:
				#print url
				continue
			if 'bbc.com/accessibility' in url:
				#print url
				continue
			if 'bbc.com/capital' in url:
				#print url
				continue
			if 'bbc.com/cbbc' in url:
				#print url
				continue
			if 'bbc.com/cbeebies' in url:
				#print url
				continue
			if 'bbc.com/contact' in url:
				#print url
				continue
			if 'bbc.com/culture/story' in url:
				#print url
				continue
			if 'bbc.com/cymrufyw' in url:
				#print url
				continue
			if 'bbc.com/education/subjects' in url:
				#print url
				continue
			if 'bbc.com/education/topics' in url:
				#print url
				continue
			if 'bbc.com/food' in url:
				#print url
				continue
			if 'bbc.com/future' in url:
				#print url
				continue
			if 'bbc.com/help' in url:
				#print url
				continue
			if 'bbc.com/news/help' in url:
                                #print url
                                continue
			if 'bbc.com/id' in url:
				#print url
				continue			
			if 'bbc.com/japanese' in url:
				#print url
				continue
			if 'bbc.com/learning' in url:
				#print url
				continue
			if 'bbc.com/mediacentre' in url:
				#print url
				continue	
			if 'bbc.com/modules' in url:
				#print url
				continue

			if 'bbc.com/news/world-radio-and-tv' in url:
                                continue
                        if 'bbc.com/news/video_and_audio' in url:
                                #print url
                                continue

			urlSpider.queue.add(url)
	
	@staticmethod	
	def find_PageItem_BBC(page_url):
                r= requests.get(page_url)
                soup = BeautifulSoup(r.content,'lxml')
                #<h1 class="story-headline gel-trafalgar-bold ">Rio 2016: Andy Murray leads Team GB out in opening ceremony</h1>
                complete_title=''
                try:
                    complete_title = soup.find('h1',{'class':'story-body__h1'}).next
                
                except:
                    pass
                try:
                    complete_title = soup.find('h1',{'class':'story-headline gel-trafalgar-bold '}).next
                except:
                    pass
                title= complete_title.replace(' ','').replace("'","").replace('!','').replace(':','')[:49]
                #print 'title:   '
                #print title
                date=''
                time=''
                try:
                    timestampdiv= soup.find('li',{'class':'mini-info-list__item'})
                    timeseconds=timestampdiv.find('div',{'class':'date date--v2'})['data-seconds']
                    timestamp =Time2ISOString(timeseconds)
                    date = timestamp[:10]
                    time = timestamp[11:]
                except:
                    pass
                try:
                    timestampdiv= soup.find('div',{'id':'media-asset-page-text'})
                    #print timestampdiv
                    timeseconds=timestampdiv.find('p',{'class':'date date--v1'})['data-seconds']
                    #print timeseconds
                    timestamp =Time2ISOString(timeseconds)
                    date = timestamp[:10]
                    time = timestamp[11:]
                except:
                    pass
                #print date
                #print time
                author=''
                try:
                    author=soup.find('div',{'class':'byline'}).find('span',{'class':'byline__name'}).next[3:]
                except:
                    pass
                #print 'author:'
                #print author
                source_name='BBC News'
                sourceId = 1007
                '''
                try:
                    source_name= soup.find('div',{'itemprop':'sourceOrganization'}).find('a').next
                    sourceId = find_source_id(source_name)
                except:
                    pass
                '''
                #print source_name
                origin_url=page_url
                pic_url=''
                try:
                    image=soup.find('img',{'class':'js-image-replace'})
                    pic_url=image['src']
                    #pic_info=soup.find('figcaption',{'class':'media-caption'})
                except:
                    pass
                try:
                    image=soup.find('img',{'class':'player-with-placeholder__image'})
                    pic_url=image['src']
                    #pic_info=soup.find('figcaption',{'class':'media-caption'})
                except:
                    pass
                try:
                    image=soup.find('div',{'class':'sp-media-asset__image gel-responsive-image'}).find('img')
                    pic_url=image['src']
                    #pic_info=soup.find('figcaption',{'class':'media-caption'})
                except:
                    pass
                try:
                    image=soup.find('figure',{'class':'media-landscape has-caption full-width'}).find('div',{'class':'js-delayed-image-load'})
                    pic_url=image['data-src']
                except:
                    pass                
                #print image  
                #print 'Pic url:'
                #print pic_url
                category_div=''
                category=''
                categoryId=12
                try:
                    category_div=soup.find('div',{'class':'secondary-navigation secondary-navigation--wide'})
                except:
                    pass
                try:
                    category_div= soup.find('a',{'class':'secondary-nav__link'})
                except:
                    pass
                try:
                    category_div=soup.find('div',{'class':'secondary-navigation secondary-navigation--wide'})
                except:
                    pass
                #print 'Category_div:'
                #print category_div
                try:            
                    category=category_div.find('a',{'class':'secondary-navigation__title navigation-wide-list__link '}).find('span').next
                except:
                    pass
                try:            
                    category=category_div.find('a',{'class':'secondary-navigation__title navigation-wide-list__link selected'}).find('span').next
                except:
                    pass
                try:            
                    category=category_div.find('span',{'class':'secondary-nav__link-text'}).next
                except:
                    pass
                if category =='':
                    try:            
                        category=soup.find('span',{'class':'index-title__container'}).find('a').next
                    except:
                        pass
                if category=='World':
                    categoryId=1
                if category =='':
                    if 'sport' in page_url:
                        category='Sport'
                        categoryId = 5
                if 'England' in category:
                    category='World'
                    categoryId = 1
                if 'Scotland' in category:
                    category='World'
                    categoryId = 1
                if 'UK' in category:
                    category='World'
                    categoryId = 1
                if 'Asia' in category:
                    category='World'
                    categoryId = 1
                if 'Wales' in category:
                    category='World'
                    categoryId = 1
                if 'Guernsey' in category:
                    category='World'
                    categoryId = 1
                if 'Science & Environment' in category:
                    category='Tech & Science'
                    categoryId = 4
                if 'Technology' in category:
                    category='Tech & Science'
                    categoryId = 4
                if 'politics' in category:
                    category='Politics'
                    categoryId = 2
                if 'EU Referendum' in category:
                    category='Politics'
                    categoryId = 2
                if 'Disability' in category:
                    category='Others'
                    categoryId = 12
                if 'The Reporters' in category:
                    category='Others'
                    categoryId = 12
                if 'Magazine' in category:
                    category='Entertainment & Arts'
                    categoryId = 7
                if 'Business' in category:
                    categoryId = 8
                if 'Education & Family' in category:
                    categoryId = 13
                #if category=='Rio 2016':
                #   category='sports'
                #print 'Category:'
                #print category
                #print categoryId
                #second_category = category_div.find('a',{'class':'navigation-wide-list__link navigation-wide-list__link--first navigation-wide-list__link--last"'}).find('span').next
                #print second_category
                
                description=''
                try:

                    article_contents= soup.find('div',{'class':'story-body__inner'}).find_all('p')
                    description=''
                    for paragraph in article_contents:
                        if paragraph.text !='Share this with' and paragraph.text!='Email' and paragraph.text!='Twitter' and paragraph.text!='Pinterest' and paragraph.text!='WhatsApp' and paragraph.text!='Facebook' and paragraph.text!='Linkedin' and paragraph.text!='Copy this link':
                            description=description+paragraph.text.replace("'",'')+'\n'
                except:
                    pass
                try:
                    article_contents= soup.find('div',{'class':'map-body'}).find_all('p')
                    description=''
                    for paragraph in article_contents:
                        if paragraph.text !='Share this with' and paragraph.text!='Email' and paragraph.text!='Twitter' and paragraph.text!='Pinterest' and paragraph.text!='WhatsApp' and paragraph.text!='Facebook' and paragraph.text!='Linkedin' and paragraph.text!='Copy this link':
                            description=description+paragraph.text.replace("'",'')+'\n'
                except:
                    pass
                try:
                    article_contents= soup.find('div',{'class':'story-body'}).find_all('p')
                    #print article_contents
                    description=''
                    for paragraph in article_contents:
                        if paragraph.text !='Share this with' and paragraph.text!='Email' and paragraph.text!='Twitter' and paragraph.text!='Pinterest' and paragraph.text!='WhatsApp' and paragraph.text!='Facebook' and\
                        paragraph.text!='Linkedin' and paragraph.text!='Copy this link'\
                        and 'Media playback is not supported on this device' not in paragraph.text:
                            description=description+paragraph.text.replace("'",'')+'\n'
                except:
                    pass
                #print 'Description: '
                #print description
                if title != "":
                    news = newsItem(title,complete_title,time,date,sourceId,description,origin_url,categoryId,author,pic_url)
                    insertRow(news)
                else:
                    return None

                return news
        
        @staticmethod
        def add_links_to_queue_fox(links):
            for url in links:
                if url in urlSpider.queue:
                        #print url
                        continue
                if url in urlSpider.crawled_url:
                        #print url
                        continue
                if urlSpider.domain_name not in url:
                        #print url
                        continue
                if 'shop.foxnews' in url:
                        #print url
                        continue
                if 'live.foxnews' in url:
                        #print url
                        continue
                if 'careers.foxnews' in url:
                        #print url
                        continue
                if 'radio.foxnews' in url:
                        #print url
                        continue
                if 'help' in url:
                        #print url
                        continue
                if 'video.foxnews' in url:
                        #print url
                        continue
                if 'video.latino' in url:
                        #print url
                        continue
                if 'latino.foxnews' in url:
                        #print url
                        continue
                if 'nation.foxnews' in url:
                        #print url
                        continue
                if 'com/on-air' in url:
                        #print url
                        continue
                if 'print' in url:
                        #print url
                        continue
                if '?intcmp=trending' in url:
                        continue
                urlSpider.queue.add(url)

        @staticmethod
        def find_PageItem_Fox(page_url):
                try:
                        r= requests.get(page_url)
                        soup = BeautifulSoup(r.content,'lxml')
                        complete_title = soup.find('h1',{'itemprop':'headline'}).next
                        title= complete_title.replace(' ','').replace("'","").replace('!','').replace(':','')[:49]
                        #print title
                        timestamp=soup.find('time')
                        if timestamp.has_attr('datetime'):
                                date= timestamp['datetime'][:10]
                                #print date
                                time= timestamp['datetime'][11:19]
                                #print time
                        dateString=soup.find('time',{'itemprop':'datePublished'}).next.replace('\n','').replace(' ','')[9:]
                        #print dateString
                        source_name='Foxnews'
                        sourceId =12
                        '''
                        try:
                                source_name= soup.find('div',{'itemprop':'sourceOrganization'}).find('a').next
                                sourceId = find_source_id(source_name)
                        except:
                                pass
                        '''
                        #print source_name
                        author=''
                        try:
                                author=soup.find('div',{'class':'article-info'}).find('span',{'itemprop':'name'}).next.replace('\n','').lstrip().rstrip()
                        except:
                                pass
                        #print author
                        origin_url=page_url
                        #print origin_url
                        pic_url=''
                        try:
                                image=soup.find('div',{'class':'m'}).find('img')
                                pic_url=image['src']
                                #pic_info=soup.find('div',{'class':'m'}).find('p').next.replace('\n','').lstrip()
                        except:
                                pass
                        #print pic_url
                        #print pic_info
                        #crawl category
                        categoryId = 12
                        if 'foxnews.com/politics' in origin_url:
                                category = 'Politics'
                                categoryId = 2
                        elif 'foxnews.com/us' in origin_url:
                                category = 'US & Canada'
                                categoryId = 3
                        elif 'foxnews.com/opinion' in origin_url:
                                category='Opinion'
                                categoryId = 6
                        elif 'foxnews.com/entertainment' in origin_url:
                                category = 'Entertainment & Arts'
                                categoryId = 7
                        elif 'foxnews.com/tech' in origin_url:
                                category='Tech & Science'
                                categoryId = 4
                        elif 'foxnews.com/science' in origin_url:
                                category = 'Tech & Science'
                                categoryId = 4
                        elif 'foxnews.com/health' in origin_url:
                                category='Health'
                                categoryId = 9
                        elif 'foxnews.com/travel' in origin_url:
                                category ='LifeStyle'
                                categoryId = 10
                        elif 'foxnews.com/world' in origin_url:
                                category='World'
                                categoryId = 1
                        elif 'foxnews.com/sports' in origin_url:
                                category='Sport'
                                categoryId = 5
                        elif 'foxnews.com/leisure' in origin_url:
                                category='Lifestyle'
                                categoryId = 10
                        elif 'foxnews.com/weather' in origin_url:
                                category='Weather'
                                categoryId = 11
                        else:
                                category='Others'
                                categoryId = 12
                        #print category
                        article_contents= soup.find('div',{'class':'article-text'}).find_all('p')
                        description=''
                        for paragraph in article_contents:
                                description=description+paragraph.text.replace("'",'')+'\n'
                        #print description
                        news = newsItem(title,complete_title,time,date,sourceId,description,origin_url,categoryId,author,pic_url)
                        
                        insertRow(news)
                        return news
                except:
                        #pass
                        #print page_url
                        print('skip this page')
                        return None


#urlSpider.find_PageItem_BBC('http://www.bbc.com/news/business-35667911')

