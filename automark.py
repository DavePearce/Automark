# -*-python-*-

# ============================================================
# Automark Application
# ============================================================

class Automark:
    def index(self):
        return "<h1>Automark</h1>"
    def test(self,rest,argument=None):
        return "<h1>TEST</h1>" + argument + "<br>" + rest
    index.exposed = True
    test.exposed = True
    

