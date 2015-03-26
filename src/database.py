# -*-python-*-

# This module is responsible for handling all interfaces between the database.  In particular, it implements a number of queries for the main application.

import sqlite3

# Role identifiers
COORDINATOR = 1
TUTOR = 2
STUDENT = 3

# Create a fresh database using a given filename.  The database will be contain all the tables necessary for the application to run, but will otherwise be empty.  The current tables are:
#
# roles --- associates USERNAMEs with COURSEs and their ROLE within those courses.  ROLE identifiers are: 1 = coordinator, 2 = tutor, 3 = student.  COURSEs are string identifiers of the form "swen221_2014T1".
def createNewDatabase(filename):
    connection = sqlite3.connect(filename)
    c = connection.cursor()
    # Create ROLES table
    c.execute('''CREATE TABLE roles(username TEXT NOT NULL, course TEXT NOT NULL, role INT)''')
    # Commit all changes
    connection.commit()
    # done
    return connection

# Add a new user role to the database.  This is a TRUSTED operation, as it is granting permissions.
def addUserRole(connection,username,course,role):
    c = conn.cursor()
    # Insert the new user role
    c.execute("INSERT INTO roles VALUES ('" + username + "','" + course + "'," + str(role) + ")")
    # Commit all changes
    connection.commit()
    # done

# Returns the list of all users with a given role in a given course.
def getUsersInCourse(connection,course,role):
    c = conn.cursor()
    # Select all matching users
    c.execute("SELECT * FROM roles WHERE course='" + course + "'")
    # Return the complete list
    return c.fetchall()
    

conn = createNewDatabase("test.db")
addUserRole(conn,"djp","swen221_2014T1",COORDINATOR)
print getUsersInCourse(conn,"swen221_2014T1",COORDINATOR)
