# -*-python-*-

# This module is responsible for handling all interfaces between the
# database.  In particular, it implements a number of queries for
# the main application.

import sqlite3
import roles

# Create a fresh database using a given filename.  The database will
# be contain all the tables necessary for the application to run, but
# will otherwise be empty.  The current tables are:
#
# users --- associates logins with student IDs, and actual names.
#
# roles --- associates logins with COURSEs and their ROLE within
# those courses.  ROLE identifiers are: 1 = coordinator, 2 = tutor,
# 3 = student.  COURSEs are string identifiers of the form "swen221_2014T1".
#
# marks --- associates logins and courses with assignment parts
def createNewDatabase(filename):
    connection = sqlite3.connect(filename)
    cursor = connection.cursor()
    # Create "Users" table
    cursor.execute('''CREATE TABLE users(login TEXT NOT NULL PRIMARY KEY, id INT, name TEXT)''')
    # Create "Roles" table
    cursor.execute('''CREATE TABLE roles(login TEXT NOT NULL, course TEXT NOT NULL, role INT NOT NULL)''')
    # Create "Marks" table
    cursor.execute('''CREATE TABLE marks(login TEXT NOT NULL, course TEXT NOT NULL, assignment INT NOT NULL, part INT NOT NULL)''')
    # Commit all changes    
    # Commit all changes
    connection.commit()
    # done
    return connection

# =============================================================
# Queries
# =============================================================
       
# Returns the list of all users with a given role in a given course.
def getUsersInCourse(connection,course,role):
    cursor = connection.cursor()
    # Select all matching users
    cursor.execute("SELECT * FROM roles WHERE course='" + course + "' AND role=" + str(role))
    # Return the complete list
    return cursor.fetchall()

# =============================================================
# Mutators
# =============================================================

# Add a new user to the database.  If the user already exists, then do nothing.
def addUserInfo(connection,login,id,name):
    cursor = connection.cursor()
    # First, check to see whether or not this user already exists.
    cursor.execute("SELECT login FROM users WHERE login='" + login +
                   "'")
    data = cursor.fetchone()
    if data is None:
        # Insert the new user role
        cursor.execute("INSERT INTO users VALUES ('" + login + "'," +
                       str(id) + ",'" + name + "')")
        # Commit all changes
        connection.commit()        
        return True
    else:
        # do nout
        return False

# Add a new user role to the database. 
def addUserRole(connection,login,course,role):
    cursor = connection.cursor()
    # Insert the new user role
    cursor.execute("INSERT INTO roles VALUES ('" + login + "','" + course + "'," + str(role) + ")")
    # Commit all changes
    connection.commit()
    # done
