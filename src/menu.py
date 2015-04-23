# -*-python-*-

import os
import json
import sqlite3

# These functions support the creation of the various dynamic menu options.  
# They are called from the mako html template and used to fill out the 
# menu items.

# Return the list of courses a given user is involved in.
def courses(user):
    conn = sqlite3.connect('data/data.db')
    c = conn.cursor()
    #r = c.execute("SELECT * FROM USERS")
    conn.close()
    return ("Hello","World")

# Return the list of assignments a given user / course is involved in.
def assignments(user,course):
    return load("data/" + course + "/config.dat")["assignments"]

# Return the list of tasks for a given assignment.
def tasks(user,course,assignment):
    return load("data/" + course + "/" + assignment + "/config.dat")["tasks"]

# Load a given file representing a database table.
def load(filename):
    f = open(filename,"r")
    data = json.load(f)
    f.close()
    return data
