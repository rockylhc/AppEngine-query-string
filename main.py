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
import cgi
import wsgiref.handlers

from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.ext.webapp import util

class Image(db.Model):
	full = db.StringProperty(multiline=False)
	thumb = db.StringProperty(multiline=False)

class MainHandler(webapp.RequestHandler):
	def get(self):
		self.response.headers['Content-Type'] = "text/xml; charset=utf-8"
		self.response.out.write("""<?xml version="1.0" encoding="utf-8"?> """)
		image = Image()
		image.full = self.request.get('full')
		image.thumb = self.request.get('thumb')
		if image.full !='' and image.thumb != '':
			image.put()

		images = db.GqlQuery("SELECT * "
                             "FROM Image ")
							
		# Parse links to full and thumb
		for allimage in images:
			self.response.out.write('<img>')
			self.response.out.write('<full>%s</full>' % 
									cgi.escape(allimage.full))
			self.response.out.write('<thumb>%s</thumb>' %
									cgi.escape(allimage.thumb))
			self.response.out.write('</img>')
			
	
application = webapp.WSGIApplication([
  ('/', MainHandler),
], debug=True)

	
def main():
   wsgiref.handlers.CGIHandler().run(application)

if __name__ == '__main__':
    main()