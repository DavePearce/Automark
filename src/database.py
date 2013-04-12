# -*-python-*-

import cherrypy
import os
import json

# ============================================================
# Raw Data Interface
# ============================================================
class Database(object):
    def __init__(self,username):
        self.permissions = load("data/permissions.dat")
        self.courses = load("data/courses.dat")
    #
    def index(self,table):
        return "GOT HERE"
    # set exposd
    index.exposed = True 
    # check permissions
    def hasPermission(self,course,permission):
        for c in self.permissions:
            if c["course"]==course and c["user"] == self.username:                
                return c["permission"]==permission
        return False

# Load a given file representing a database table.
def load(filename):
    f = open(filename,"r")
    data = json.load(f)
    f.close()
    return data
       
