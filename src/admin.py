# -*-python-*-

import cherrypy

# ============================================================
# Mako Config
# ============================================================

from mako.template import Template
from mako.lookup import TemplateLookup
lookup = TemplateLookup(directories=['html'])

# ============================================================
# Administrative Interface
# ============================================================

class Admin(object):
    def __init__(self,root_url,permissions,courses):
        self.root_url = root_url
        self.permissions = permissions
        self.courses = courses
        self.exposed = True
    # root
    def index(self,course):
        if self.permissions.hasPermission(course,"coordinator"):
            template = lookup.get_template("admin.html")
            return template.render(
                ROOT_URL=self.root_url,
                COURSE=course,
                COURSE_CODE=self.courses.getField(course,"code"),
                COURSE_NUMBER=self.courses.getField(course,"number"),
                COURSE_TITLE=self.courses.getField(course,"title"),
                COURSE_ASSIGNMENTS=self.courses.getField(course,"assignments")
                )    
        else:
            raise cherrypy.HTTPError(403,"You do not have permission to access this resource")
    # exposed
    index.exposed = True

