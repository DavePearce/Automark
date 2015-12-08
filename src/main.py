# -*-python-*-

import os
from cherrypy.lib.static import serve_file
from cherrypy import request

# ============================================================
# Mako Config
# ============================================================

from mako.template import Template
from mako.lookup import TemplateLookup
lookup = TemplateLookup(directories=['html'])

# ===================================================================
# Application Resource.  This is a helper class which provides a
# RESTful resource interface.  Specifically, it allows application
# objects to be built which respond to GET/PUT requersts, etc in the
# appropriate fashion.
# ===================================================================

class Resource(object):
    # --------------------------------------------------------
    # Resource Root
    # --------------------------------------------------------
    def index(self,**kwargs):
        if request.method == "GET":
            return self.GET(kwargs)
        else:
            return self.PUT(kwargs)            
    index.exposed = True

# ===================================================================
# Application Table.  A table provides a RESTful interface to an
# underlying database table.
# ===================================================================

class Table(Resource):
    
    def __init__(self,table):
        # The table is used to identify the database table to which
        # this resource corresponds.
        self.table = table

    # -------------------------------------------------------------
    # Table GET.  Return the contents of this resource, potentially
    # with a query applied as given by the arguments.
    # -------------------------------------------------------------
    def GET(self,kwargs):
        return "GOT HERE: " + str(kwargs)

    # -------------------------------------------------------------
    # Table PUT
    # -------------------------------------------------------------
    def PUT(self):
        return "PUT HERE"
        
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
    
    courses = Table("courses")

 

