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
from xml.dom.minidom import Document
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
		# Create the minidom document
		doc = Document()
		
		image = Image()
		image.full = self.request.get('full')
		image.thumb = self.request.get('thumb')
		if image.full !='' and image.thumb != '':
			image.put()
		# Create the <img> base element
		img = doc.createElement("img")
		doc.appendChild(img)
		
		images = db.GqlQuery("SELECT * "
                             "FROM Image ")
							
		# Parse links to full and thumb
		for allimage in images:
			full = doc.createElement("full")
			thumb = doc.createElement("thumb")
			img.appendChild(full)
			img.appendChild(thumb)
			fulllink = doc.createTextNode(cgi.escape(allimage.full))
			full.appendChild(fulllink)
			thumblink = doc.createTextNode(cgi.escape(allimage.thumb))
			thumb.appendChild(thumblink)

		# Print our newly created XML
		print doc.toprettyxml(indent="  ")
						  

application = webapp.WSGIApplication([
  ('/', MainHandler),
], debug=True)

	
def main():
   wsgiref.handlers.CGIHandler().run(application)

if __name__ == '__main__':
    main()
