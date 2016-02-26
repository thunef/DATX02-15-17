#!/usr/bin/env python
import zipfile
import json
from pprint import pprint
archive = zipfile.ZipFile('test.sb2', 'r')
jsondata = archive.read('project.json')
data=json.loads(jsondata)

scripts = data['children'][0]['scripts']


def runScript(script):
    for index in range(len(script)):
        print "run",script[index]

# To check if string is same as event(in list form)
def isSame(script,whichOne):
    for index in range(len(script)):
        if script[index] == whichOne:
            return 1
    return 0


def findScripts(whichOne):
    for index in range(len(scripts)):
        #Don't know first 2 rows but it script starts at [2]
        temp = isSame(scripts[index][2][0],whichOne) #First(0) row is the event
        if temp:
            runScript(scripts[index][2])


x = raw_input('What is pushed: ')

findScripts(x)
