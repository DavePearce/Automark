# -*-python-*-

from cherrypy.lib.static import serve_file

# ============================================================
# Mako Config
# ============================================================

from mako.template import Template
from mako.lookup import TemplateLookup
lookup = TemplateLookup(directories=['html'])

# ============================================================
# Assignment View
# ============================================================
class Assignment(object):
    def __init__(self,root_url,data):
        self.root_url=root_url
        self.data = data
        self.exposed = True
        
    # --------------------------------------------------------
    # Page Handlers
    # --------------------------------------------------------
    def index(self,course,assignment):
        self.data.checkPermission(course,"coordinator")
        template = lookup.get_template("assignmentview.html")
        return template.render(ROOT_URL=self.root_url,COURSE=course,ASSIGNMENT=assignment)
    index.exposed = True 
