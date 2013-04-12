# -*-python-*-

import cherrypy
import os
import json

# ============================================================
# Raw Data Interface
# ============================================================
class Database(object):
    def __init__(self,username):
        self.username = username
        self.permissions = load("data/permissions.dat")
        self.courses = load("data/courses.dat")
        self.assignments = {}
        self.exposed = True
        
    # --------------------------------------------------------
    # Page Handlers
    # --------------------------------------------------------
    def index(self):
        return "GOT HERE"    
    index.exposed = True 
    
    def coordinating(self):        
        return json.dumps(join("course",self.courses,select(self.permissions,{"user": self.username, "permission": "coordinator"})))
    coordinating.exposed = True 

    def tutoring(self):        
        return json.dumps(join("course",self.courses,select(self.permissions,{"user": self.username, "permission": "tutor"})))
    coordinating.exposed = True 

    # --------------------------------------------------------
    # Query Functions
    # --------------------------------------------------------
    def checkPermission(self,course,permission):
        for p in self.permissions:
            if p["course"]==course and p["user"] == self.username and p["permission"]==permission:                
                return
        raise cherrypy.HTTPError(403,"You do not have permission to access this resource")

# Load a given file representing a database table.
def load(filename):
    f = open(filename,"r")
    data = json.load(f)
    f.close()
    return data

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
       
def join(key,table1,table2):
    results=[]
    for row1 in table1:
        for row2 in table2:
            if row1[key] == row2[key]:
                results.append(dict(row1.items()+row2.items()))
    return results
