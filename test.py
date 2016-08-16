import pyodbc
from newsItem import *


def insertRow(newsItem):
	#try:
		conn = pyodbc.connect('DRIVER={SQL Server};SERVER=kapydatabase.database.windows.net,1433', user='kapygroup', password='Kapykapy1234', database='kapymvc1')
		cursor=conn.cursor()

		# Prepare SQL query to INSERT a record into the database.
		sql ="INSERT INTO dbo.Source(sourceName) VALUES (?)"
		cursor.execute(sql,(newsItem.source_name))
		sql ="INSERT INTO dbo.News(uniqueTitle,newsTitle,newsDate, newsTime, sourceName, origUrl, newsContent,categoryName,author,picUrl) VALUES (?,?,?,?,?,?,?,?,?,?)"

		
			# Execute the  SQL command
			#print news.title
			#print news.date
			#print news.category
		cursor.execute(sql,(newsItem.title,newsItem.complete_title,newsItem.date,newsItem.time,newsItem.source_name,newsItem.origin_url,newsItem.description,newsItem.category,newsItem.author,newsItem.pic_url))
			# Commit your changes in the database
		conn.commit()
		print 'success insert data'
		#except:
			# Rollback in case there is any error
			#conn.rollback()
			#print "failed insert data"

		conn.close()
		#print 'insertion finish'

	#except:
		#print "connection failed2"

newsItem.title='test1test1test1'
newsItem.complete_title="gkldsald kddddddddddddd a;dljfkas;l  jkda;ldsjfk;lsadf"
newsItem.date='Aug 9 2018'
newsItem.time='13:45'
newsItem.source_name="fox"
newsItem.origin_url="http://www.foxnews/politics/kdkdkkaldjkflajdsf"
newsItem.description="dkjkkkkkkkkkkkkkkkkkkkkkkkkkkgasldddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddkl;;;;;;;;;;;;;;;;;;;;;;kdddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd"
newsItem.category="Politics"
newsItem.author='yyyyy'
newsItem.pic_url='kdkdkkdladjflksajdfjdd'
insertRow(newsItem)