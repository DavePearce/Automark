# -*-python-*-

import json
import ecs

class Database(object):
    def __init__(self,root_dir):
        # The root directory of the database
        self.root_dir = root_dir

    # Retrieve course configuration data (i.e. settings) which are visible
    # to the course coordinator.  For example, the list of assignments
    # and/or tutors is visible to the course coordinator.
    def courses(self,user):
        return ["hello","world"]

    # Retrieve course configuration data (i.e. settings) which are visible
    # to the course coordinator.  For example, the list of assignments
    # and/or tutors is visible to the course coordinator.
    def course(self,user,course):
        return load(self.root_dir + course + "/config.dat")

    # Retrieve assignment configuration data (i.e. settings) which is
    # visible to the course coordinator.  For example, the list of actions 
    # is visible to the course coordinator.
    def assignment(self,user,course,assignment):
        return load(self.root_dir + course + "/" + assignment + "/config.dat")

    # Retrieve the list of submissions for a given assignment which is
    # visible to the course coordinator.  This includes the student ID 
    # and name of each submission, along with a list of the submitted 
    # files.
    def submissions(self,user,course,assignment):
        config=load(self.root_dir + course + "/" + assignment + "/config.dat")
        return ecs.findSubmissions(course,assignment,config)

    # Retrieve the list of marks for a given assignment submission
    # which is visible to the course coordinator.  This includes the
    # student ID and name for each submission, along with the marks
    # for each completed task.
    def marks(self,user,course,assignment):
        config=load(self.root_dir + course + "/" + assignment + "/config.dat")
        return ecs.findMarks(course,assignment,config)

    # Retrieve the marking sheet data for this assignment, which is 
    # visible to the tutors.
    def marksheet(self,user,course,assignment):
        return load(self.root_dir + course + "/" + assignment + "/marksheet.dat")

# ============================================================
# Helper functions
# ============================================================
    
# Load a given file representing a database table.
def load(filename):
    f = open(filename,"r")
    data = json.load(f)
    f.close()
    return data
