from dataconnet import *
import os
import datetime
import time
def sleeptime(hour,min,sec):
	return hour*3600 + min*60 + sec

second = sleeptime(1,0,0)
while 1==1:
	print 'start'
	print datetime.datetime.now()
	print 'start crawl fox'
	os.system('initial_fox.py')
	print 'start crawl bbc'
	os.system('initial_bbc.py')
	time.sleep(second)
	
