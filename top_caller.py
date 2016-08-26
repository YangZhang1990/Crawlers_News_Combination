from dataconnet import *
import os
import datetime
import time
def sleeptime(hour,min,sec):
	return hour*3600 + min*60 + sec

second = sleeptime(0,0,20)
while 1==1:
	print 'start'
	print datetime.datetime.now()
	os.system('initial_fox.py')
	time.sleep(second)
	
