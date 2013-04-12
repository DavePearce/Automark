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

class Permissions(object):
    def __init__(self,root_url,username,filename):
        self.root_url = root_url
        self.username = username
        self.content = load(filename)
        self.exposed = True
    # select course
    def index(self):
        r={}
        r["tutoring"]=[]
        r["coordinating"]=[]
        for c in self.content:
            if c["user"] == self.username:
                if c["permission"]=="tutor":
                    r["tutoring"].append(c["course"])
                elif c["permission"]=="coordinator":
                    r["coordinating"].append(c["course"])
        return json.dumps(r)
    # expose
    index.exposed = True
    # check permissions
    def hasPermission(self,course,permission):
        for c in self.content:
            if c["course"]==course and c["user"] == self.username:                
                return c["permission"]==permission
        return False

# Load a given file representing a database table.
def load(filename):
    f = open(filename,"r")
    data = json.load(f)
    f.close()
    return data
