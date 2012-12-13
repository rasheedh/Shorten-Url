import webapp2
import random
import cgi
from google.appengine.ext import db

class Data(db.Model):
	longurl=db.StringProperty(multiline=True)
	shorturl=db.StringProperty()

class MainPage(webapp2.RequestHandler):
	def get(self):
		self.response.out.write("""
          	<html>
            	<body>
		<br/><br/><br/><br/><br/><br/><br/><br/>
		<center>
              	<form >
                <div><textarea name="content" rows="3" cols="60"></textarea></div>
                <div><input type="submit" value="ShortUrl"></div>
              	</form></center>""")
		longurl=self.request.get('content')
		l = len(longurl)
		val1=[]
		#val1.append("/")
		for i in range(0,l-1):
			#s=0
			#s = ord(longurl[i])
			#s = str(s)
			if i%10==0:
				val1.append(longurl[i])
				#val1.append("'")
		shorturl = ''.join(val1)
		if longurl != "":
			obj=Data(db.Key.from_path('URL',longurl))
			#self.response.out.write(store.longurl)
			obj.longurl=longurl
			obj.shorturl=shorturl
			#self.response.out.write(longurl)
			url=db.GqlQuery("SELECT * FROM Data WHERE ANCESTOR IS :c",c=db.Key.from_path('URL',longurl))
			count =0
			for i in url:
				count=count+1
			if count==0:
				obj.put()
			short=self.request.path[1:]
			url1=db.GqlQuery("SELECT * FROM Data WHERE ANCESTOR IS :c",c=db.Key.from_path('URL',longurl))
			
			for i in url1:
				self.response.out.write("<center><br/><br/>Shortened Url")
				self.response.out.write("<br/><br/><font size=5px color=red>huntersshort.appspot.com/")
				self.response.out.write(i.shorturl)
				self.response.out.write("""<br></font></center>""")
			self.response.out.write("""</body></html>""")
		if self.request.path[1:]!="":
			u=Data.all()
			res = u.filter("shorturl =",self.request.path[1:]).get()
			self.redirect(str(res.longurl))			

app=webapp2.WSGIApplication([('/.*',MainPage)],debug=True)		
