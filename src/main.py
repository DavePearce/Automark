# -*-python-*-

import os
# CherryPy
from cherrypy.lib.static import serve_file
from cherrypy import request
# Application
import data

# ============================================================
# Mako Config
# ============================================================

from mako.template import Template
from mako.lookup import TemplateLookup
lookup = TemplateLookup(directories=['html'])
       
# =================================================================
# Application Entry.  This is the entry point for this application,
# and serves all routes.  
# =================================================================

class Main(object):
    
    def __init__(self,root_url,username):
        # The root url gives the base url for the application root.
        # This is needed to get resources in some situations.
        self.root_url = root_url
        # Current authenticated username of user making this query.
        # This is necessary to limit what the user is and is not
        # allowed to see.
        self.username = username

    # -------------------------------------------------------------
    # Standard resources (images, js, html, etc)
    # -------------------------------------------------------------
    
    # gives access to images/
    def images(self, filename):
        abspath = os.path.abspath("images/" + filename)
        return serve_file(abspath, "image/png")
    images.exposed = True
    
    def js(self, filename):
        abspath = os.path.abspath("js/" + filename)
        return serve_file(abspath, "application/javascript")
    js.exposed = True

    def css(self, filename):
        abspath = os.path.abspath("css/" + filename)
        return serve_file(abspath, "text/css")
    css.exposed = True

    # -------------------------------------------------------------
    # Application Root
    # -------------------------------------------------------------

    def index(self):
        template = lookup.get_template("index.html")
        return template.render(ROOT_URL="")
    index.exposed = True
    # exposed

    # -------------------------------------------------------------
    # Application View
    # -------------------------------------------------------------
    
    def view(self,template,course=None,assignment=None):
        template = lookup.get_template(template + ".html")
        return template.render(ROOT_URL=self.root_url,
                               USER=self.username,
                               COURSE=course,       
                               ASSIGNMENT=assignment)        
    view.exposed = True

    # -------------------------------------------------------------
    # Application Data
    # -------------------------------------------------------------
    
    users = data.Table(data.User)

 

