import pyodbc
import datetime
from newsItem import *


def insertRow(newsItem):
	try:
		conn = pyodbc.connect('DRIVER={SQL Server};SERVER=kapydatabase.database.windows.net,1433', user='kapygroup', password='Kapykapy1234', database='kapymvc1')
		cursor=conn.cursor()


		sql ="INSERT INTO dbo.News1(uniqueTitle,newsTitle,newsDate, newsTime,sourceId, origUrl, newsContent,categoryId,author,picUrl,crawlTime) VALUES (?,?,?,?,?,?,?,?,?,?,?)"

		try:
			# Execute the  SQL command
			#print news.title
			#print news.date
			#print news.sourceId
			#print news.categoryId
			cursor.execute(sql,(newsItem.title,newsItem.complete_title,newsItem.date,newsItem.time,newsItem.sourceId,newsItem.origin_url,newsItem.description,newsItem.categoryId,newsItem.author,newsItem.pic_url,datetime.datetime.now()))
			# Commit your changes in the database
			conn.commit()
			print 'success insert data'
		except:
			#Rollback in case there is any error
			conn.rollback()
			print "failed insert data"

		conn.close()
		#print 'insertion finish'

	except:
		print "connection failed2"
#news = newsItem("title","complete_title","14:22","2016-08-12",13,"description","origin_url",2,"author","pic_url")

#insertRow(news)

def deleteDupicatetRows():
	try:
		conn = pyodbc.connect('DRIVER={SQL Server};SERVER=kapydatabase.database.windows.net,1433', user='kapygroup', password='Kapykapy1234', database='kapymvc1')
		cursor=conn.cursor()
		sql1 ="DELETE FROM dbo.News1 WHERE newsId NOT IN(SELECT MIN(newsId) FROM dbo.News1 GROUP BY uniqueTitle)"
		try:
			cursor.execute(sql1)
			conn.commit()
			print 'success delete duplicate data'
		except:
			conn.rollback()
			print "failed delete duplicate data"
		sql2 ="DELETE FROM dbo.News1 WHERE newsDate ='1900-01-01'"
		try:
			cursor.execute(sql2)
			conn.commit()
			print 'success delete inproper date'
		except:
			conn.rollback()
			print "failed delete inproper data"
		conn.close()
	except:
		print "connection failed2"


'''
DELETE FROM [dbo].[News1]
      WHERE newsDate ='1900-01-01';
GO
'''
#delete duplicate rows
'''
USE [kapymvc1]
GO


DELETE
FROM [dbo].[News1]
WHERE newsId NOT IN
(
SELECT MAX(newsId)
FROM [dbo].[News1]
GROUP BY uniqueTitle)



'''


