#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
from google.appengine.ext import webapp
from google.appengine.ext.webapp import util

import os
from google.appengine.ext.webapp import template

from google.appengine.api import urlfetch

from xml.dom.minidom import *

from pagemodel import *

import string

def getText(nodelist):
    rc = []
    for node in nodelist:
        if node.nodeType == node.TEXT_NODE:
            rc.append(node.data)
    return ''.join(rc)
	

class HomePage(webapp.RequestHandler):
	def get(self):
			
		cval = {}
		
		try:
			rssurl = "http://hamiltonnhs.tumblr.com/rss"
			data = urlfetch.fetch(rssurl)
			if data.status_code == 200:
				dom = parseString(data.content)
				
				items = dom.getElementsByTagName("item")
				
				postshtml = ""
				
				posts = 0
				
				for item in items:
					title = getText(item.getElementsByTagName("title")[0].childNodes)
					postcontent = getText(item.getElementsByTagName("description")[0].childNodes)
					link = getText(item.getElementsByTagName("link")[0].childNodes)
					pubDate = getText(item.getElementsByTagName("pubDate")[0].childNodes)
					
					html = """
					<strong>{{TITLE}}</strong> - {{DATE}}<br>
					&nbsp;&nbsp;&nbsp;&nbsp;{{DESC}}&nbsp;&nbsp;<a href="{{LINK}}">See Entire Post</a><br><hr>
					"""
					
					html = html.replace("{{TITLE}}", title)
					html = html.replace("{{DATE}}", string.join(pubDate.split()[:3], " "))
					
					short = ""
					if len(postcontent) > 140:
						short = postcontent[:140] + "..."
					else:
						short = postcontent
						
					#short = postcontent
						
					html = html.replace("{{DESC}}", short)
					html = html.replace("{{LINK}}", link)
					
					postshtml += html
					
					posts = posts + 1
					
					if posts > 3:
						break
				
				
			
				cval['posts'] = postshtml
		except:
			pass
		
		content = template.render(os.path.join(os.path.dirname(__file__), 'html/columns.html'),cval)
		
		results = PageCode.gql("WHERE name = :1", "slider").fetch(limit=1)
		silder = ""
		if len(results) > 0:
			slider = results[0].html
		else:
			template.render(os.path.join(os.path.dirname(__file__), 'html/slider.html'),{})
		
		template_values = {
		'content' : content,
		'pagename' : "Home Page",
		'slider' : slider,
		'home' : "class='active'"
		}
		
		path = os.path.join(os.path.dirname(__file__), 'template/template.html')
		self.response.out.write(template.render(path, template_values))
		
def getEmbeddedGoogleDocs(url):
	content = '''
			<center><br><br>
<iframe frameborder="0" style="width:950px; height:900px; border-style:none; border:0;" src="'''  +  url + '''"></iframe>
	</center>
		'''
		
	return content
		
class ContactPage(webapp.RequestHandler):
	def get(self):
			
		cval = {}
		
		
		content = getEmbeddedGoogleDocs("https://docs.google.com/document/pub?id=1phAmQk5-Cq9-Qmrsred40y387nVq33YNG1slkBg4rH8&amp;embedded=true")

		
		template_values = {
		'content' : content,
		'pagename' : "Contact Info",
		'contact' : "class='active'"
		}
		
		path = os.path.join(os.path.dirname(__file__), 'template/template.html')
		self.response.out.write(template.render(path, template_values))
		
class EventsPage(webapp.RequestHandler):
	def get(self):
			
		cval = {}
		
		content = ""
		
		content = getEmbeddedGoogleDocs("https://docs.google.com/document/pub?id=1La9mBSRaaoxJRg5KW-aZSMpJGqhcoFGaCeiB52dDIxc&amp;embedded=true")
		
		
		template_values = {
		'content' : content,
		'pagename' : "Upcoming Events",
		'events' : "class='active'"
		}
		
		path = os.path.join(os.path.dirname(__file__), 'template/template.html')
		self.response.out.write(template.render(path, template_values))
		
class HandoutsPage(webapp.RequestHandler):
	def get(self):
			
		cval = {}
		
		content = ""
		
		content = getEmbeddedGoogleDocs("https://docs.google.com/document/pub?id=1s8ETomA2-TIQ6FL5RW3ccYLbUi78cq7uJaMArAAhvfM&amp;embedded=true")
		
		template_values = {
		'content' : content,
		'pagename' : "Important Handouts",
		'handouts' : "class='active'"
		}
		
		path = os.path.join(os.path.dirname(__file__), 'template/template.html')
		self.response.out.write(template.render(path, template_values))
		
class PowerPointsPage(webapp.RequestHandler):
	def get(self):
			
		cval = {}
		
		content = ""
		
		content = getEmbeddedGoogleDocs("https://docs.google.com/document/pub?id=1ArYMnWyjTMfh_qoVE6snLhFQA3plipXALFidL11P488&amp;embedded=true")
		
		template_values = {
		'content' : content,
		'pagename' : "General Meeting PowerPoints",
		'pp' : "class='active'"
		}
		
		path = os.path.join(os.path.dirname(__file__), 'template/template.html')
		self.response.out.write(template.render(path, template_values))
		
		
class PhotosPage(webapp.RequestHandler):
	def get(self):
			
		cval = {}
		
		content = ""
		
		content = getEmbeddedGoogleDocs("https://docs.google.com/document/pub?id=1KPBr18k1Hyjm0fmUZkiR0c84hhpVrYfrJKFFf8qFrrY&amp;embedded=true")
		
		template_values = {
		'content' : content,
		'pagename' : "Photos",
		'photos' : "class='active'"
		}
		
		path = os.path.join(os.path.dirname(__file__), 'template/template.html')
		self.response.out.write(template.render(path, template_values))


bindings = [
('/', HomePage),
('/contact', ContactPage),
('/events', EventsPage),
('/powerpoints', PowerPointsPage),
('/handouts', HandoutsPage),
('/photos', PhotosPage)
]
def main():
    application = webapp.WSGIApplication(bindings,
                                         debug=True)
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()
