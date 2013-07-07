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

import random

import os
from google.appengine.ext.webapp import template

from google.appengine.ext.db import Key

import re
import string
import datetime

from password import *
from pagemodel import *

from gaesessions import *

pageslist = '''
<tr>
	<td><h3>{{name}}</h3></td>
	<td><a href="#" class="ico del">Delete</a><a href="editpage?key={{key}}" class="ico edit">Edit</a></td>
</tr>
'''



class EditPage(webapp.RequestHandler):
	def post(self):
		AuthenticateAdmin(self)
		
		key = self.request.get('key')
		html = self.request.get('html')
		
		page = PageCode.get(Key(key))
		
		page.html = html
		
		page.put()
		
		self.redirect("pages")
	def get(self):
		AuthenticateAdmin(self)
		
		key = self.request.get('key')
		page = PageCode.get(Key(key))
	
		values = {}
		
		values['name'] = page.name
		values['html'] = page.html
		
		template_values = {
		'content' : template.render(os.path.join(os.path.dirname(__file__), 'admin/editpage.html'),values),
		'pages' : 'class="active"'
		}
		path = os.path.join(os.path.dirname(__file__), 'admin/template.html')
		self.response.out.write(template.render(path, template_values))

class NewPage(webapp.RequestHandler):
	def post(self):
		AuthenticateAdmin(self)
		
		page = PageCode()
		page.name = self.request.get('name')
		page.html = ""
		page.put()
		
		self.redirect('pages')
	
class PagesPage(webapp.RequestHandler):
	def get(self):
		AuthenticateAdmin(self)
	
		values = {}
		
		pages = ""
		
		query = PageCode.all()
		results = query.fetch(limit=1000)
		
		for page in results:
			html = pageslist.replace("{{name}}", page.name)
			html = html.replace("{{key}}", str(page.key()))
			pages += html
			
		values['pages'] = pages
		
		template_values = {
		'content' : template.render(os.path.join(os.path.dirname(__file__), 'admin/pages.html'),values),
		'pages' : 'class="active"'
		}
		path = os.path.join(os.path.dirname(__file__), 'admin/template.html')
		self.response.out.write(template.render(path, template_values))

class AdminPassword(webapp.RequestHandler):
	def post(self):
		
		p1 = self.request.get('p1')
		
		errors = ""
		
		query = Password.all()
		results = query.fetch(limit=1)
		
		result = 0
		
		if len(results) > 0:
			
			
			p = sha.new()
			p.update(p1)
			pval = p.hexdigest()
			
			if results[0].password == pval:
				result = 2
			else:
				result = 0
				errors += Error("Incorrect Password")
			
		else:
			result = 1
			

		
		if result == 0:
			self.render(errors)
		if result == 1:
			session = get_current_session()
			session.regenerate_id()
			session['admin'] = True
			self.redirect("setpassword")
		if result == 2:
			session = get_current_session()
			session.regenerate_id()
			session['admin'] = True
			self.redirect("home")
		
	def get(self):
		self.render("")
		
	def render(self,error):
	
		results = PageCode.gql("WHERE name = :1", "images").fetch(limit=1)
		if len(results) > 0:
			images = results[0].html.split()
			img = images[random.randint(0,len(images)-1)]
		else:
			img = ""
	
		'''
		images = [
		"http://icanhascheezburger.files.wordpress.com/2008/04/funny-pictures-password-lolspeakeasy.jpg",
		"http://icanhascheezburger.files.wordpress.com/2011/05/funny-pictures-today-password-iz-back-rub.jpg",
		"http://icanhascheezburger.files.wordpress.com/2008/09/funny-pictures-cat-is-suspicious-of-your-intentions.jpg",
		"http://images.cheezburger.com/completestore/2009/9/18/128977704323210964.jpg"
		]
		'''
		
		
		
		
		values = {}
		
		values['img'] = img
		values['errors'] = error
		
		path = os.path.join(os.path.dirname(__file__), 'admin/password.html')
		self.response.out.write(template.render(path, values))
		
class AdminLogout(webapp.RequestHandler):
	def get(self):
		session = get_current_session()
		session.terminate()
		
		self.redirect('home')
		
class AdminHomePage(webapp.RequestHandler):
	def get(self):
		self.redirect('admin/home')

bindings = [
('/admin', AdminHomePage),
('/admin/', PagesPage),
('/admin/home', PagesPage),
('/admin/pages', PagesPage),

('/admin/password', AdminPassword),
('/admin/setpassword', SetAdminPassword),
('/admin/logout', AdminLogout),

('/admin/newpage', NewPage),
('/admin/editpage', EditPage)
]

def main():
	application = webapp.WSGIApplication(bindings, debug=True)
	util.run_wsgi_app(application)


if __name__ == '__main__':
	main()
