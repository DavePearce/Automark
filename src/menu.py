# -*-python-*-

import os
import json

# These functions support the creation of the various dynamic menu options.  
# They are called from the mako html template and used to fill out the 
# menu items.

# Return the list of courses a given user is involved in.
def courses(user):
    return ("Hello","World")

# Return the list of assignments a given user / course is involved in.
def assignments(user,course):
    return ("Hello","World")

# Return the list of tasks for a given assignment.
def tasks(user,course,assignment):
    return ("Hello","World")
