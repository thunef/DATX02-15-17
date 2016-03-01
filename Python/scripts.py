import json
import os
import shutil
import zipfile
from collections import deque

def getJson():
    zip_file = zipfile.ZipFile("Untitled.zip")
    for member in zip_file.namelist():
        if member == 'project.json':
           json_data = zip_file.read(member)
           zip_file.close()
           return json_data


json_poop = getJson()
json_data = json.loads(json_poop)

json_scripts = json_data['children'][0]['scripts']


def runScript(script):
    script_str = str(script[0])
    script_for = script[1]
    print "run:", script_str, "for:", script_for
#    for index in range(len(script)):
#        print "run",script[index]

# To check if string is same as event(in list form)
def isSame(script,whichOne):
#    print range(len(script))
#    for index in range(len(script)):
    if script == whichOne:
        return 1
    return 0


def findScripts():
    for index in range(len(scripts)):
        #Don't know first 2 rows but it script starts at [2]
        #temp = isSame(scripts[index][0],whichOne)
        #if temp:
        runScript(scripts[index])

print range(len(json_scripts[0][2]))
#print scripts
scripts = []
for k in range(len(json_scripts[0][2])):
    scripts.append(json_scripts[0][2][k])

print scripts
#x = raw_input('What is pushed: ')

findScripts()

