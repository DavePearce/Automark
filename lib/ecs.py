# -*-python-*-

import json
import dircache
import cgi
import os
import re
from stat import *

# ===================================================
# Helpers for interfacing with ECS submission system
# ===================================================
   
# determine the list of students which have submitted something
# for a given assignment
def submitted(course,assignment):
    markingDir = "/vol/submit/" + course + "/" + assignment + "/"
    students = []
    for login in dircache.listdir(markingDir):
        mode = os.stat(markingDir + "/" + login)[ST_MODE]
        if not S_ISDIR(mode):
            continue; # ignore things which aren't directories.
        students.append(login)
    return students

# determine the name and login of a given student
def idName(course,assignment,login):
    markingDir = "/vol/submit/" + course + "/" + assignment + "/"
    name = "unknown"
    id = -1
    nm = re.compile("<Name>([a-zA-Z0-9_, ]*)</Name>*")
    idm = re.compile("<ID>([0-9]*)</ID>*")
    try:
        f = open(markingDir + login + "/marking/userInfo.xml")
    except Exception:
        # for group projects
        try:
            f = open(markingDir + login + "/marking/groupInfo.xml")
        except Exception:
            print ""
            return (-1,"<font color=red>UNKNOWN</font>")
    for l in f:
        if nm.match(l):
            name = nm.match(l).group(1)
        if idm.match(l):
            id = idm.match(l).group(1)
    return (id,name)

def course(path):
    regex = re.compile("([a-zA-Z0-9_]+)\/")    
    r = regex.match(path)
    return (r.group(1))

def courseAssign(path):
    regex = re.compile("([a-zA-Z0-9_]+)\/(Assignment_[0-9]+)")    
    r = regex.match(path)
    return (r.group(1),r.group(2))

def courseAssignLogin(path):
    regex = re.compile("([a-zA-Z0-9_]+)\/(Assignment_[0-9]+)\/([a-z0-9]+)")    
    r = regex.match(path)
    return (r.group(1),r.group(2),r.group(3))


def writeMarkingData(course,assignment,login,name,data):
    markingDir = "/vol/submit/" + course + "/" + assignment + "/" + login + "/marking/"
    f = open(markingDir + name + ".json","w")
    f.write(json.dumps(data))
    f.close()

def loadMarkingData(course,assignment,login,name):
    markingDir = "/vol/submit/" + course + "/" + assignment + "/" + login + "/marking/"
    if os.path.exists(markingDir + name + ".json"):
        f = open(markingDir + name + ".json","r")
        data = json.load(f)
        f.close()
        return data
    else:
        return None
    
