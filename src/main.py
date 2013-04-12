# -*-python-*-

import os
from cherrypy.lib.static import serve_file
import filedb

import database

# ============================================================
# Mako Config
# ============================================================

from mako.template import Template
from mako.lookup import TemplateLookup
lookup = TemplateLookup(directories=['html'])

# ============================================================
# Application Entry
# ============================================================

class Main(object):
    def __init__(self,root_url,username):
        self.root_url = root_url
        self.username = username
        self.data = database.Database(username)

    # gives access to images/
    def images(self, filename):
        abspath = os.path.abspath("images/" + filename)
        return serve_file(abspath, "image/png")
    
    # gives access to js/
    def js(self, filename):
        abspath = os.path.abspath("js/" + filename)
        return serve_file(abspath, "application/javascript")
    
    def css(self, filename):
        abspath = os.path.abspath("css/" + filename)
        return serve_file(abspath, "text/css")
    
    # application root
    def index(self):
        template = lookup.get_template("index.html")
        return template.render(ROOT_URL=self.root_url,USER_NAME=self.username)
    
    # exposed
    index.exposed = True
    images.exposed = True
    js.exposed = True
    css.exposed = True