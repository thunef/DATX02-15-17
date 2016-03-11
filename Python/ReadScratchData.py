#!/usr/bin/env python
import zipfile
import json
from pprint import pprint
from random import randint
#from gopigo import *
#import sys

#import atexit
#atexit.register(stop)

archive = zipfile.ZipFile('alla_kommandon.sb2', 'r')
data=json.loads(archive.read('project.json'))

scripts = data['children'][0]['scripts']

lists     = {}
variables = {}

speed = 0

# put the userdefined lists with the content of that
# list in a container, each list keeps its name  
def getLists(json_lists):
    for k in range(len(json_lists)):
        name = json_lists[k]['listName']
        lists[name] = json_lists[k]['contents']

def getVariables(json_variables):
    for k in range(len(json_variables)):
        name = json_variables[k]['name']
        variables[name] = json_variables[k]['value']


def getValue(cmd):
    if cmd[0] == 'readVariable':
        return variables[cmd[1]]
    if cmd[0] == 'randomFrom:to:':
        return randint(cmd[1],cmd[2])
    return 0


def isTrue(statement):
    a = getValue(statement[1])
    b = getValue(statement[2])

    if statement[0] == '=':
        return a == b
    elif statement[0] == '<':
        return a < b
    elif statement[0] == '>':
        return a > b

def runCommand(cmd):
        print "\nrunning:"

        if cmd[0] == "forward:":
            print "framAt" , cmd[1]
            #fwd()
        elif cmd[0] == "turnRight:":
            print "rotate right" , cmd[1], " degrees\n"
            #right()
        elif cmd[0] == "turnLeft:":
            print "rotate left" , cmd[1], " degrees\n"
            #left()
        elif cmd[0] == "doRepeat":
            print "doRepeat\n"
            for index in range(cmd[1]):
                runScript(cmd[2])
        elif cmd[0] == "doForever":
            print "going to loop forever!!"
            print cmd[1]
            while True:
                runScript(cmd[1])
        elif cmd[0] == 'doIf':
            print "doIf\n"
            print cmd[1]
            if isTrue(cmd[1]) :
                runScript(cmd[2])
        elif cmd[0] == 'doIfElse':
            print "doIfElse\n"
            if isTrue(cmd[1]):
                runScript(cmd[2])
            else:
                runScript(cmd[3])
        elif cmd[0] =='setVar:to:':
            print "setVar to: ", cmd[2], "\n"
            variables[cmd[1]] = cmd[2]
            print cmd[1],"  =  ",variables[cmd[1]]
        elif cmd[0] =='changeVar:by:':
            variables[cmd[1]] += cmd[2]
            print cmd[1],"  =  ",variables[cmd[1]]
        elif cmd[0] == "stopScripts":
            print "stopScripts"
#            stop()  # gopigo
            speed = 0
        elif cmd[0] == 'maxspeed:':
            print 'maxspeed'
#        set_speed(255) # 255 is the maximum speed of the gopigo
        elif cmd[0] == "accelerate:":
            print "accelerating:", cmd[1]
#            for k in range(cmd[1]):
#                increase_speed()
        elif cmd[0] == "retardate:":
            print "slowing down:", cmd[1]
#            for k in range(cmd[1]):
#                decrease_speed()
        elif cmd[0] == "nospeed:":
            print "stoping"
            #stop()
            
        else: print "TODO:", cmd[0]

def runScript(script):
    for index in range(len(script)):
        runCommand(script[index])

def findScripts(whichOne):
    for index in range(len(scripts)):
        #First 2 rows is gui posision, but script starts at [2]
        if scripts[index][2][0][0] == whichOne: #First(0) row is the event
            runScript(scripts[index][2])

if 'variables' in {x for x in data if x in 'variables'}:
    getVariables(data['variables'])

if 'lists' in {x for x in data if x in 'lists'}:
    getLists(data['lists'])

x = raw_input('What is pushed (ex:"whenClicked"): ')
findScripts(x)
