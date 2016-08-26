import urllib
import urllib2
import sys
from general import *
import requests
from bs4 import BeautifulSoup
from urlparse import urljoin
from dataconnet import *
from newsItem import *
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
            
                #<p class="date date--v1" data-seconds="1470434601" data-timestamp-inserted="true"><strong>5 August 2016</strong> Last updated at 23:03 BST </p>
                #print 'timestampe:  '
                #print timestamp
                '''
                date=''
                try:
                    date=timestamp.find('p',{'class':'date date--v1'}).next              
                except:
                    pass
                try:
                    date=timestamp.find('p',{'class':'date date--v1'}).find('strong').next                  
                except:
                    pass
                try:
                    date=timestamp.find('div',{'class':'date date--v2'}).next               
                except:
                    pass
                try:
                    date=soup.find('time').find('abbr')['title']  
                except:
                    pass 
                try:
                    date=soup.find('p',{'class':'date date--v1'}).find('strong').next   
                except:
                    pass
                try:
                    date=soup.find('p',{'class':'date date--v1'}).find('strong').next   
                except:
                    pass
                '''
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
                print date
                print time
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

                #if category=='Rio 2016':
                #   category='sports'
                #print 'Category:'
                #print category
                
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
                    #insertRow(news)
                else:
                    return None

                return news

find_PageItem_BBC('http://www.bbc.com/news/world-europe-37188301')
