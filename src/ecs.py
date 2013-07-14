# -*-python-*-

import json
import dircache
import cgi
import os
import re
from stat import *

# ============================================================
# ECS submission system interface
# ============================================================

#ECS_SUBMIT_DIR="/vol/submit/"
ECS_SUBMIT_DIR="/Users/djp/scratch/submit/"
MARKING_DIR_RE = re.compile("marking/([a-zA-Z0-9_/\ \.]*)")

# determine the list of students which have submitted something
# for a given assignment
def findSubmissions(course,assignment):
    markingDir = ECS_SUBMIT_DIR + course + "/" + assignment + "/"
    students = []
    for login in dircache.listdir(markingDir):
        mode = os.stat(markingDir + "/" + login)[ST_MODE]
        if not S_ISDIR(mode):
            continue; # ignore things which aren't directories.
        id,name = getIdName(course,assignment,login)
        students.append({"login": login, "id": id, "name": name})
    return students

# determine the name and login of a given student
def getIdName(course,assignment,login):
    markingDir = ECS_SUBMIT_DIR + course + "/" + assignment + "/"
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
            return (-1,"unknown")
    for l in f:
        if nm.match(l):
            name = nm.match(l).group(1)
        if idm.match(l):
            id = idm.match(l).group(1)
    return (id,name)

# determine the name and login of a given student
def getSubmittedFiles(course,assignment,login):
    markingDir = ECS_SUBMIT_DIR + course + "/" + assignment + "/"
    li=[]
    for file in findfiles(markingDir + login):
    	if not MARKING_DIR_RE.match(file):
	   li.append(file)
    return li 

def getTaskMark(course,assignment,login,stage):
    stageDir = ECS_SUBMIT_DIR + course + "/" + assignment + "/" + login + "/marking/automark/" + stage
    # First, check whether any errors were produced by stage
    try:
        f = open(stageDir + "/run.status")
        status = f.read()
        f.close()
    except Exception:
        return "?"
    return status

# generate the master list of all assignment data
def getMarks(course,assignment,config):
    submissions = findSubmissions(course,assignment)
    for s in submissions:
        login = s["login"]
        for task in config["tasks"]:
            s[task]=getTaskMark(course,assignment,login,task)
    return submissions

# =======================================================================
# HELPER FUNCTIONS
# =======================================================================

# Traverse from the root, and find all files.  
def findfiles(root):
    r = []
    for path,dirs,names in os.walk(root):
        for name in names:
            r.append(os.path.join(path,name).replace(root + "/",""))
    return r

def matchlist(list, matcher):
    rlist = []
    for l in list:
    	if matcher.match(l):
	   rlist.append(l)
    return rlist   

# Copy files into destination directory.  Create subdirectories as
# necessary
def copyfiles(files,src,dest):
    for file in files:
        try:
            os.makedirs(os.path.dirname(dest + file))
        except Exception:
            # silently do nothing
            print ""
        try:
            shutil.copyfile(src + file,dest + "/" + file)
        except Exception:
            print ""
        try:
            shutil.copystat(src + file,dest + "/" + file)
        except Exception:
            print ""
            
