import json
# CherryPy
import cherrypy
from cherrypy import request
# SQL Alchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

# ===================================================================
# Database sessions
# ===================================================================
engine = create_engine('sqlite:///database.db')
Session = sessionmaker(bind=engine)

# =================================================================
# Schema
# =================================================================
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    fullname = Column(String(50))
    password = Column(String(12))
    #
    # Convert instance into Python dictionary.  This makes for easy
    # conversion into JSON.
    def as_dict(self):        
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}

Base.metadata.create_all(engine)

# ===================================================================
# Application Resource.  This is a helper class which provides a
# RESTful resource interface.  Specifically, it allows application
# objects to be built which respond to GET/PUT requersts, etc in the
# appropriate fashion.
# ===================================================================

class MethodDispatcher(object):
    # --------------------------------------------------------
    # Resource Root
    # --------------------------------------------------------
    def index(self,**kwargs):
        if request.method == "GET":
            return self.GET(kwargs)
        elif request.method == "POST":
            return self.POST(kwargs)                  
        elif request.method == "PUT":
            return self.PUT(kwargs)                  
        elif request.method == "DELETE":            
            return self.DELETE(kwargs)
        else:
            cherrypy.HTTPError(500,"unknown HTTP request method")
    index.exposed = True

# ===================================================================
# Application Table.  A table provides a RESTful interface to an
# underlying database table.
# ===================================================================
class Table(MethodDispatcher):
    
    def __init__(self,table):
        # The table is used to identify the database table to which
        # this resource corresponds.
        self.table = table

    # -------------------------------------------------------------
    # Table GET.  Return the contents of this resource, potentially
    # with a query applied as given by the arguments.
    # -------------------------------------------------------------
    def GET(self,kwargs):
        session = Session()
        result = []
        for row in session.query(User).all():
            result.append(row.as_dict())
        return json.dumps(result)
    # -------------------------------------------------------------
    # POST
    # -------------------------------------------------------------
    def POST(self,kwargs):
        return "POST" + str(kwargs)



