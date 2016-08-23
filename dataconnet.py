import pyodbc
from newsItem import *


def insertRow(newsItem):
	try:
		conn = pyodbc.connect('DRIVER={SQL Server};SERVER=kapydatabase.database.windows.net,1433', user='kapygroup', password='Kapykapy1234', database='kapymvc1')
		cursor=conn.cursor()


		sql ="INSERT INTO dbo.News1(uniqueTitle,newsTitle,newsDate, newsTime,sourceId, origUrl, newsContent,categoryId,author,picUrl) VALUES (?,?,?,?,?,?,?,?,?,?)"

		try:
			# Execute the  SQL command
			#print news.title
			#print news.date
			#print news.sourceId
			#print news.categoryId
			cursor.execute(sql,(newsItem.title,newsItem.complete_title,newsItem.date,newsItem.time,newsItem.sourceId,newsItem.origin_url,newsItem.description,newsItem.categoryId,newsItem.author,newsItem.pic_url))
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