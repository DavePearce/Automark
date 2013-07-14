# -*-python-*-

import os
import os
import json
import dircache
import re

from cherrypy.lib.static import serve_file

import ecs

# ============================================================
# Mako Config
# ============================================================

from mako.template import Template
from mako.lookup import TemplateLookup
lookup = TemplateLookup(directories=['html'])

# ============================================================
# Data Model
# ============================================================

class Model(object):
    def __init__(self,username):
        self.username = username
        self.permissions = load("permissions.dat")
        self.courses = load("courses.dat")
        self.exposed = True
        
    # --- Page Handlers ---
    def coordinating(self):        
        return json.dumps(join("course",self.courses,select(self.permissions,{"user": self.username, "permission": "coordinator"})))
    coordinating.exposed = True 
    
    def tutoring(self):        
        return json.dumps(join("course",self.courses,select(self.permissions,{"user": self.username, "permission": "tutor"})))
    tutoring.exposed = True 
    
    def config(self,course,assignment=None):
        self.checkPermission(course,"coordinator")
        if assignment == None:
            return json.dumps(load(course + "/config.dat"))
        else:
            return json.dumps(load(course + "/" + assignment + "/config.dat"))            
    config.exposed = True 
    
    def submissions(self,course,assignment):
        self.checkPermission(course,"coordinator")
        config = load(course + "/" + assignment + "/config.dat")
        return json.dumps(ecs.getMarks(course,assignment,config))
    submissions.exposed = True
    
    # --- Query Functions ---
    def checkPermission(self,course,permission):
        for p in self.permissions:
            if p["course"]==course and p["user"] == self.username and p["permission"]==permission:                
                return
        raise cherrypy.HTTPError(403,"You do not have permission to access this resource")

# ============================================================
# Application Entry
# ============================================================

class Main(object):
    def __init__(self,root_url,username):
        self.root_url = root_url
        self.username = username
        self.data = Model(username)
        #self.view = View(root_url,self.data)

    def view(self,course,name=None):
        if name == None:
            template = lookup.get_template("view/course.html")
            return template.render(ROOT_URL=self.root_url,COURSE=course)
        else:
            self.data.checkPermission(course,"coordinator")
            template = lookup.get_template("view/assignment.html")
            return template.render(ROOT_URL=self.root_url,COURSE=course,ASSIGNMENT=name)
    view.exposed = True 
    
    # gives access to images/
    def images(self, filename):
        abspath = os.path.abspath("images/" + filename)
        return serve_file(abspath, "image/png")
    images.exposed = True
    
    # gives access to js/
    def js(self, filename):
        abspath = os.path.abspath("js/" + filename)
        return serve_file(abspath, "application/javascript")
    js.exposed = True
    
    # gives access to css/
    def css(self, filename):
        abspath = os.path.abspath("css/" + filename)
        return serve_file(abspath, "text/css")    
    css.exposed = True    
    
    # application root
    def index(self):
        template = lookup.get_template("index.html")
        return template.render(ROOT_URL=self.root_url,USER_NAME=self.username)
    index.exposed = True

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
    f = open("data/" + filename,"r")
    data = json.load(f)
    f.close()
    return data
