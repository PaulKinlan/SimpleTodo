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
from google.appengine.ext.webapp import template

from google.appengine.api import users

import logging

def RenderThemeTemplate(templatename, data):
	import os
	path = os.path.join(os.path.dirname(__file__), "templates", templatename)

	return template.render(path, data)

class MainHandler(webapp.RequestHandler):
    def get(self):
      # if we reach here, login has worked
      user = users.get_current_user()
      
      if user:
        self.response.out.write(RenderThemeTemplate("index.html", {"user": user}))
      else:
        url = "google.com/accounts/o8/id"
        openId = users.create_login_url(federated_identity = url)
        logging.info(openId)
        self.redirect(openId)
        
class EmbedHandler(webapp.RequestHandler):
    def get(self):
      # if we reach here, login has worked
      self.response.out.write(RenderThemeTemplate("embed.html", {}))

def main():
    application = webapp.WSGIApplication([('/', MainHandler), ('/index.html', MainHandler), ('/embed.html', EmbedHandler)],
                                         debug=True)
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()
