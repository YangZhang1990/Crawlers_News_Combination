import datetime
import time

'''
second = sleeptime(0,0,10)
while 1==1:
	time.sleep(second)
	print datetime.datetime.now()
'''
#!/usr/bin/env python
# -*- coding: cp936 -*-



def ISOString2Time( s ):
    ''' 
    convert a ISO format time to second
    from:2006-04-12 16:46:40 to:23123123

    '''
    d=datetime.datetime.strptime(s,"%Y-%m-%d %H:%M:%S")
    return time.mktime(d.timetuple())

def Time2ISOString( s ):
    ''' 
    convert second to a ISO format time
    from: 23123123 to: 2006-04-12 16:46:40

    '''
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime( float(s) ) ) 

'''
a="2016-08-25 16:58:00"
b=ISOString2Time(a)
print b
c=Time2ISOString(1472155212)
print c

'''
