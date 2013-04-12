# -*-python-*-

import cherrypy
import os
import json

# ============================================================
# Mako Config
# ============================================================

from mako.template import Template
from mako.lookup import TemplateLookup
lookup = TemplateLookup(directories=['html'])

# ============================================================
# Administrative Interface
# ============================================================

class Courses(object):
    def __init__(self,root_url,username,filename):
        self.root_url = root_url
        self.username = username
        self.exposed = True
        self.content = load(filename)
    # select course
    def index(self,id=None):
        if id == None:
            return json.dumps(self.content)
        else:
            for c in self.content:
                if c["id"]==id:
                    return json.dumps(c)
            return ""
    # expose
    index.exposed=True

# Load a given file representing a database table.
def load(filename):
    f = open(filename,"r")
    data = json.load(f)
    f.close()
    return data
