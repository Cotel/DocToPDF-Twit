#!/usr/bin/env python
# author: Miguel Coleto

from mechanize import Browser
import sys, urllib, os, subprocess

# little parser for handling refresh html tag
from HTMLParser import HTMLParser
class MyHTMLParser(HTMLParser):
	fileid = None
	def handle_startendtag(self, tag, attrs):
		if tag == 'meta' and attrs[0] == ('http-equiv', 'refresh'):
			self.fileid = attrs[1][1].split('result.php')[-1]

def fileid(self):
	return self.fileid

def transformation(url):	
	# creates the url where the file should be downloaded for its later transformation
	file_name = url.split('/')[-1]
	urllib.urlretrieve(url,file_name)

	br = Browser()
	#br.set_handle_equiv(True)
	#br.set_handle_redirect(True)
	#br.set_handle_refresh(True)
	#br.set_handle_referer(True)
	br.set_handle_robots(False)
	#br.addheaders = [('User-Agent', 'Firefox')]

	# open converter site
	urlbase = "http://www.conv2pdf.com/"
	br.open(urlbase)

	# fill-in the form
	br.select_form(nr=0)
	br.add_file(open(file_name),'text/plain',file_name)

	# submit
	response = br.submit()


	parser = MyHTMLParser()
	parser.feed(response.read())

	# get redirection from the response
	urlfile = urlbase+"download.php"+parser.fileid
	print urlfile

	# open redirected location
	br.open(urlfile)

	# save file
	with open(file_name+".pdf", 'w') as f:
		f.write(br.response().read())

	# uploads file to ge.tt
	#os.system('gett '+file_name+".pdf")
	x = os.popen('gett '+file_name+'.pdf').read()
	os.remove(file_name)
	os.remove(file_name+'.pdf')
	return x

