# -*-python-*-

# ============================================================
# Administrative Interface
# ============================================================

class Admin(object):
    def __init__(self,root_url,username):
        self.root_url = root_url
        self.username = username
    # root
    def index(self):
        template = lookup.get_template("admin.html")
        return template.render(ROOT_URL=self.root_url,USER_NAME=self.username)    
    # exposed
    index.exposed = True

