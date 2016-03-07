#!/usr/bin/env python
import zipfile
import json
from pprint import pprint
from random import randint
#from gopigo import *
#import sys

#import atexit
#atexit.register(stop)

archive = zipfile.ZipFile('test.sb2', 'r')
data=json.loads(archive.read('project.json'))

scripts = data['children'][0]['scripts']

variables = {}

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
        print "\nrunning\n -----",cmd

        if cmd[0]=="forward:":
            print "framAt" , cmd[1]
            #fwd()
        elif cmd[0] =="turnRight:":
            print "rotate right" , cmd[1], " degrees"
            #right()
        elif cmd[0] =="turnLeft:":
            print "rotate left" , cmd[1], " degrees"
            #left()
        elif cmd[0] =="doRepeat":
            for index in range(cmd[1]):
                runScript(cmd[2])
        elif cmd[0] =='doIf':
            if isTrue(cmd[1]) :
                runScript(cmd[2])
        elif cmd[0] =='doIfElse':
            if isTrue(cmd[1]):
                runScript(cmd[2])
            else:
                runScript(cmd[3])
        elif cmd[0] =='setVar:to:':
            variables[cmd[1]] = cmd[2]
            print cmd[1],"  =  ",variables[cmd[1]]
        elif cmd[0] =='changeVar:by:':
            variables[cmd[1]] += cmd[2]
            print cmd[1],"  =  ",variables[cmd[1]]


def runScript(script):
    for index in range(len(script)):
        runCommand(script[index])

def findScripts(whichOne):
    for index in range(len(scripts)):
        #First 2 rows is gui posision, but script starts at [2]
        if scripts[index][2][0][0] == whichOne: #First(0) row is the event
            runScript(scripts[index][2])


x = raw_input('What is pushed (ex:"whenClicked"): ')
findScripts(x)
