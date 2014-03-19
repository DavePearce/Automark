# -*-python-*-

import os
from cherrypy.lib.static import serve_file
import json

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
        # The root url gives the base url for the application root.
        # This is needed to get resources in some situations.
        self.root_url = root_url
        # Current authenticated username of user making this query.
        # This is necessary to limit what the user is and is not
        # allowed to see.
        self.username = username
        # Always load permissions, since we almost always need that.
        # We immediately select those permission relevant for this
        # user, since we don't care about others.
        self.permissions = select(load("data/permissions.dat"),{"user": self.username})

    # --------------------------------------------------------
    # Standard resources (images, js, html, etc)
    # --------------------------------------------------------
    
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

    # --------------------------------------------------------
    # Application Root
    # --------------------------------------------------------

    def index(self):
        template = lookup.get_template("index.html")
        return template.render(ROOT_URL="")
    index.exposed = True
    # exposed

    # --------------------------------------------------------
    # Application Views
    # --------------------------------------------------------
    
    def view(self,year):
        template = lookup.get_template("index.html")
        return template.render(ROOT_URL=self.root_url,YEAR=year)        
    view.exposed = True

    # --------------------------------------------------------
    # Application Data
    # --------------------------------------------------------
    
    # Retrieve course specific data (e.g. settings)
    def course(self,course,table):
        return json.dumps(load("data/" + year + "/" + table + ".dat"))
    course.exposed = True

    # Retrieve allocation of tutors to students for marking.  This is
    # a list of student ID's for the given tutor, representing those
    # students the tutor must mark.
    def tutor_allocation(self,course,assignment):
        #checkPermission(self,course,["tutor","coordinator"])
        # Load table of allocations
        allocation = load("data/" + course + "/" + assignment + "/tutor-allocation.dat")
        # Return allocations of user only
        return json.dumps(select(allocation,{"tutor": self.username}))
    tutor_allocation.exposed = True

    # --------------------------------------------------------
    # Authentication
    # --------------------------------------------------------
    
    # Check whether or not the given user has one of a list of
    # permissions for a given course.  If not, an HTTPError is raised.
    # For example, we might wish to check that a user has permission
    # as either "tutor" or "coordinator".  This makes sense if we
    # assume that a coordinator can always do what a tutor can do.
    def checkPermission(self,course,permissions):
        for mp in self.permissions:
            for rp in permissions: 
                if mp["course"]==course and mp["permission"]==rp:
                    return
        # If we get here, then user doesn't have required permission
        # so raise HTTP error.
        raise cherrypy.HTTPError(403,"You do not have permission to access this resource")

# ============================================================
# Helper functions
# ============================================================

# Straightforward implementation of select query
def select(table,matches):
    results=[]
    for row in table:
        m=True
        for key,match in matches.items():
            if row[key] != match:
                m=False
                break
        if m:
            results.append(row)
    return results
       
# Straightforward implementation of join query
def join(key,table1,table2):
    results=[]
    for row1 in table1:
        for row2 in table2:
            if row1[key] == row2[key]:
                results.append(dict(row1.items()+row2.items()))
    return results

# Load a given file representing a database table.
def load(filename):
    f = open(filename,"r")
    data = json.load(f)
    f.close()
    return data
