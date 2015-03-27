# -*-python-*-

import csv
import roles
import database

# This module contains various admin utilities which typically use the
# database connection.  For example, creating a new course for the
# first time.

# Create a new course.  This requires the course name
# (e.g. "swen221_2015T1"), the course coordinator's login, and the list
# of student logins.
def createNewCourse(connection,course,coordinator,tutors,students):
    # Add course coordinator
    database.addUserRole(connection,coordinator,course,roles.COORDINATOR)
    # Add tutors
    for login in tutors:
        database.addUserRole(connection,login,course,roles.TUTOR)
    # Add students
    for login in students:
        database.addUserRole(connection,login,course,roles.STUDENT)


# ============================================================
# Importing
# ============================================================

# The following imports students from a CSV file.
def importStudentsFromCSV(dbname,course,filename):
    connection = database.createNewDatabase(dbname)    
    with open(filename, 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            if len(row) >= 3:
                database.addUserRole(connection,row[3],course,roles.STUDENT)
        
    
