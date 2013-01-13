# -*-python-*-

# ============================================================
# Mako Config
# ============================================================

from mako.template import Template
from mako.lookup import TemplateLookup
lookup = TemplateLookup(directories=['templates'])

# ============================================================
# Automark Application
# ============================================================

class Automark:
    def index(self):
        template = lookup.get_template("index.html")
        return template.render()
    index.exposed = True
    


