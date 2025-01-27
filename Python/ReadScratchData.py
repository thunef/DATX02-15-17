#!/usr/bin/env python
import zipfile
#import sys
#import atexit
import json
import time
import datetime
from pprint import pprint
from random import randint
#from gopigo import *
#atexit.register(stop)

DELAY_BETWEEN_COMMANDS = 0.2 #Sec
DATE = datetime.datetime.now()
DiffSince2000 = datetime.date.today() - datetime.date(2000, 01, 01)

archive = zipfile.ZipFile('alla_kommandon.sb2', 'r')
data=json.loads(archive.read('project.json'))

scripts = data['children'][0]['scripts']

lists     = {}
variables = {}

speed = 50


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
    if isinstance( cmd, int ):
        return cmd
    if cmd[0] == 'timestamp':
        return DiffSince2000.days
    if cmd[0] == 'timeAndDate':
        if (cmd[1] == 'minute'):
            return DATE.minute
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
        ##print "\nrunning:"

        # Motion
        if cmd[0] == "forward:":
            print "framAt" , cmd[1]
            #enc_tgt(1,1,72)  ## m1: 0 to disable targeting for motor 1, 1 to enable it
            ## m2: 0 to disable targeting for motor 2, 1 to enable it
            ## target: number of encoder pulses to target (18 per rotation). For moving the wheel by 2 rotations, target should be 36
            #fwd()
        elif cmd[0] == "turnRight:":
            print "rotate right " , cmd[1], " degrees \n"
            #enc_tgt(0,1,72)
            #fwd()
            #right()
            #set_left_speed(getValue(cmd[1]))
        elif cmd[0] == "turnLeft:":
            print "rotate left ", cmd[1], " degrees \n"
            #enc_tgt(1,0,72)
            #fwd()
            #left()
            #set_right_speed(speed)
        elif cmd[0] == 'maxspeed:':
            print 'maxspeed'
            #set_speed(255) # 255 is the maximum speed of the gopigo
        elif cmd[0] == "accelerate:":
            print "SetSpeed:", cmd[1]
            for k in range(getValue(cmd[1])):
                print "acc"
#                increase_speed()
        elif cmd[0] == "retardate:":
            print "slowing down:", cmd[1]
#            for k in range(getValue(cmd[1])):
#                decrease_speed()
        elif cmd[0] == "nospeed:":
            print "stoping"
            #stop()
        elif cmd[0] == "stopScripts":
            print "stopScripts"
#            stop()  # gopigo
        # Control
        elif cmd[0] == "doRepeat":
            print "doRepeat\n"
            for index in range(getValue(cmd[1])):
                runScript(cmd[2])
        elif cmd[0] == "doUntil":
            print "doUntil\n"
            while isTrue(cmd[1]) == False:
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
        # Data
        elif cmd[0] =='setVar:to:':
            print "setVar to: ", cmd[2], "\n"
            print variables[cmd[1]],"  becomes  ",cmd[1] , " -- is it?"
            variables[cmd[1]] = getValue(cmd[2])
            print variables[cmd[1]]
        elif cmd[0] =='changeVar:by:':
            print variables[cmd[1]]," change by ",cmd[2], " -- is it"
            variables[cmd[1]] += getValue(cmd[2])
            print variables[cmd[1]]
        elif cmd[0] =='append:toList:':
            print "mmokay ", cmd[2] , " add " , cmd[1]
            lists[cmd[2]].append(getValue(cmd[1]))
        elif cmd[0] =='insert:at:ofList:':
            print "mmokay ", cmd[3] , " add " , cmd[1] ," @",cmd[2]
            lists[cmd[3]].insert(cmd[2], getValue(cmd[1]))

        else: print "TODO:", cmd[0]

def runScript(script):
    for index in range(len(script)):
        runCommand(script[index])
        time.sleep(DELAY_BETWEEN_COMMANDS)

def findScripts(whichOne):
    for index in range(len(scripts)):
        #First 2 rows is gui posision, but script starts at [2]
        if scripts[index][2][0][0] == whichOne: #First(0) row is the event
            runScript(scripts[index][2])

if 'variables' in {x for x in data if x in 'variables'}:
    getVariables(data['variables'])

if 'lists' in {x for x in data if x in 'lists'}:
    getLists(data['lists'])

#x = raw_input('What is pushed (ex:"whenClicked"): ')
findScripts("whenGreenFlag")
