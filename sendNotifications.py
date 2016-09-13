import pyodbc
from user import *
import smtplib
import datetime

def getUsers():
      try:
            conn = pyodbc.connect('DRIVER={SQL Server};SERVER=kapydatabase.database.windows.net,1433', user='kapygroup', password='Kapykapy1234', database='kapymvc1')
            cursor=conn.cursor()
            sql1 ="SELECT Id, Email FROM dbo.AspNetUsers WHERE emailConfirmed =1"
            try:
                  users=[]
                  cursor.execute(sql1)
                  for row in cursor.fetchall():
                        users.append(user(row[0],row[1]))
                        print row[0]
                        print row[1]
                  print 'success get users'
                  return users
            except:
                  conn.rollback()
                  print "failed get data"

      except:
            print "connection failed"      
def sendEmail(user):
      SUBJECT = "Everyday News From KAPY!"
      TEXT = "This is a test for notification\n\n"+getNewsForUser(user.user_id)
      message = 'Subject: %s\n\n%s' % (SUBJECT, TEXT)
      message=message.encode("utf-8")
      mail = smtplib.SMTP('smtp.gmail.com',587)
      mail.ehlo()
      mail.starttls()
      mail.login('kapynews@gmail.com','Kapyiscool1234')
      mail.sendmail('kapynews@gmail.com',user.user_email,message)
      print 'mail sent'
      mail.close()
def getNewsForUser(user_Id):
      try:          
            conn = pyodbc.connect('DRIVER={SQL Server};SERVER=kapydatabase.database.windows.net,1433', user='kapygroup', password='Kapykapy1234', database='kapymvc1')
            cursor=conn.cursor()
            try:
                  url = "https://kapynewstest1.azurewebsites.net/News1/Details/"
                  newscontent="Recommend News in "+str(datetime.date.today())+" to you\n\n"
                  cursor.execute("""
                        SELECT souceId FROM dbo.AspNetUser_Source WHERE UserId = ?
                        """,
                        user_Id)
                  ids=0
                  for row in cursor.fetchall():
                        ids=ids+row[0]            
                  if ids==0:
                        print "aaa"
                        cursor.execute("""SELECT top 10 newsTitle, newsId,newsTime FROM dbo.News1
                              WHERE categoryId in(SELECT categoryId FROM dbo.AspNetUser_Category WHERE userId = ?)
                              AND newsDate = ?
                              ORDER BY newsTime desc"""
                              ,user_Id,str(datetime.date.today()))
                  else:
                        cursor.execute("""SELECT top 10 newsTitle, newsId,newsTime,sourceId FROM dbo.News1
                              WHERE categoryId in(SELECT categoryId FROM dbo.AspNetUser_Category WHERE userId = ?)
                              AND sourceId in (SELECT souceId FROM dbo.AspNetUser_Source WHERE UserId = ?)
                              AND newsDate = ?
                              ORDER BY newsTime desc"""
                              ,user_Id,user_Id,str(datetime.date.today()))
                  newsList=""      
                  for row in cursor.fetchall():
                        newsList=newsList+row[0]
                        newscontent=newscontent+row[0]+"\n"+url+str(row[1])+"\n\n"
                        print row[0]
                        print row[1]
                        print row[2]
                  print 'success get news'
                  if newsList =="":
                        newscontent="Select news in categories and sources you're interested in and receive our notifications for you!\nhttps://kapynewstest1.azurewebsites.net"
                  else:
                        newscontent=newscontent
                  return newscontent
            except:
                  conn.rollback()
                  print "failed get news"
      except:
            print "connection failed" 


users = getUsers()
for user in users:
      sendEmail(user)


#getNewsForUser(101)
