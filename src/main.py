# -*-python-*-

import os
from cherrypy.lib.static import serve_file
import json
import ecs

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
    
    def view(self,template,course=None,assignment=None):
        template = lookup.get_template(template + ".html")
        return template.render(ROOT_URL=self.root_url,
                               USER=self.username,
                               COURSE=course,       
                               ASSIGNMENT=assignment)        
    view.exposed = True

    # --------------------------------------------------------
    # Application Data
    # --------------------------------------------------------
    
    # Retrieve course configuration data (i.e. settings) which are visible
    # to the course coordinator.  For example, the list of assignments
    # and/or tutors is visible to the course coordinator.
    def course(self,course):
        # checkPermission(self,course,["coordinator"])        
        return json.dumps(load("data/" + course + "/config.dat"))
    course.exposed = True

    # Retrieve assignment configuration data (i.e. settings) which is
    # visible to the course coordinator.  For example, the list of actions 
    # is visible to the course coordinator.
    def assignment(self,course,assignment):
        # checkPermission(self,course,["coordinator"])        
        return json.dumps(load("data/" + course + "/" + assignment
                               + "/config.dat"))
    assignment.exposed = True

    # Retrieve the list of submissions for a given assignment which is
    # visible to the course coordinator.  This includes the student ID 
    # and name of each submission, along with a list of the submitted 
    # files.
    def submissions(self,course,assignment):
        # checkPermission(self,course,["coordinator"])        
        config=load("data/" + course + "/" + assignment + "/config.dat")
        return json.dumps(ecs.findSubmissions(course,assignment,config))
    submissions.exposed = True

    # Retrieve the list of marks for a given assignment submission
    # which is visible to the course coordinator.  This includes the
    # student ID and name for each submission, along with the marks
    # for each completed task.
    def marks(self,course,assignment):
        # checkPermission(self,course,["coordinator"])        
        config=load("data/" + course + "/" + assignment + "/config.dat")
        return json.dumps(ecs.findMarks(course,assignment,config))
    marks.exposed = True

    # Retrieve the marking sheet data for this assignment, which is 
    # visible to the tutors.
    def marksheet(self,course,assignment):
        # checkPermission(self,course,["tutor"])
        return json.dumps(load("data/" + course + "/" + assignment
                               + "/marksheet.dat"))
    marksheet.exposed = True

    # Run a given task for a given student in a given course and
    # assignment.  This will produce a mark which is recorded in the
    # database, along with any supplmentary information (i.e. error
    # messages).
    def run(self,course,assignment,login,task):
        return json.dumps(ecs.runTask(course,assignment,login,task))
    run.exposed = True
        

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
