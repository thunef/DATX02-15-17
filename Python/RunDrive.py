#!/usr/bin/env python
import zipfile
import sys
import atexit
import json
import time
import datetime
from pprint import pprint
from random import randint
from gopigo import *
atexit.register(stop)

DELAY_BETWEEN_COMMANDS = 0.5 #Sec
DATE = datetime.datetime.now()
DiffSince2000 = datetime.date.today() - datetime.date(2000, 01, 01)

# hours, minutes, seconds
timer_started = [0,0,0]

ROTATIONTIME = 14 # For waiting on wheels to rotate

archive = zipfile.ZipFile('drive.sb2', 'r')
data=json.loads(archive.read('project.json'))

scripts = data['children'][0]['scripts']

lists     = {}
variables = {}

current_speed = 120

min_speed = 50

def reset_timer():
    now = time.localtime(time.time())
    timer_started = [now[3], now[4], now[5]]

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
        DATE = datetime.datetime.now()
        if (cmd[1] == 'minute'):
            return DATE.minute
        elif cmd[1] == 'second':
            return DATE.second
        elif cmd[1] == 'hour':
            return DATE.hour
    if cmd[0] == 'readVariable':
        return variables[cmd[1]]
    if cmd[0] == 'randomFrom:to:':
        return randint(cmd[1],cmd[2])
        #us_dist()
    if cmd[0] == 'getLine:ofList:':
        print "okidok getting position", cmd[1], " from ", cmd[2]
        tmp = lists[cmd[3]]
        return tmp[cmd[1]]

    if cmd[0] == 'lineCountOfList:':
        tmp = lists[cmd[2]]
        return tmp.length

    if cmd[0] == '%':
        return cmd[1] % cmd[2]

    #returns time  since the timer started.
    if cmd[0] == 'timer':
        now = time.localtime(time.time())
        return (now[3] - timer_started[0],
                now[4] - timer_started[1],
                now[5] - timer_started[2])

    return 0


def isTrue(statement):
    if statement[0] == 'not':
        return isTrue(statement[1])

    a = getValue(statement[1])
    b = getValue(statement[2])

    if statement[0] == '=':
        return a == b
    elif statement[0] == '<':
        return a < b
    elif statement[0] == '>':
        return a > b

def setSpeed(s):
    #print "setting speed ", current_speed
    global current_speed
    current_speed = s
    set_speed(current_speed)
    print "setting speed ", current_speed

def runCommand(cmd):
        print "speed: ", current_speed
        ##print "\nrunning:"

        # Motion
        if cmd[0] == "forward:":
            print "framAt" , cmd[1]
            rot=getValue(cmd[1])
            enc_tgt(1,1,rot)    ## m1: 0 to disable targeting for motor 1, 1 to enable it
                                ## m2: 0 to disable targeting for motor 2, 1 to enable it
                                ## target: number of encoder pulses to target (18 per rotation). For moving the wheel by 2 rotations, target should be 36

            fwd()
            time.sleep(rot/ROTATIONTIME)
        if cmd[0] == "backwards:":
            print "bakka" , cmd[1]
            rot=getValue(cmd[1])
            enc_tgt(1,1,rot)
            bwd()
            time.sleep(rot/ROTATIONTIME)
        elif cmd[0] == "turnRight:":
            print "rotate right " , cmd[1], " degrees"
            rot = getValue(cmd[1])/6
            enc_tgt(0,1,rot)
            left()
            time.sleep(rot/ROTATIONTIME)
        elif cmd[0] == "turnLeft:":
            enable_encoders()
            print "rotate left ", cmd[1], " degrees"
            rot = getValue(cmd[1])/6
            enc_tgt(1,0,rot)
            right()
            time.sleep(rot/ROTATIONTIME)
        elif cmd[0] == 'maxspeed:':
            print 'maxspeed'
            setSpeed(255) # 255 is the maximum speed of the gopigo
        elif cmd[0] == "accelerate:":
            print "IncSpeed: ",current_speed  ," with ", cmd[1]
            setSpeed(current_speed+getValue(cmd[1]))
        elif cmd[0] == "retardate:":
            print "slowing down:" ,current_speed  ," with ", cmd[1]
            setSpeed(current_speed-getValue(cmd[1]))
        elif cmd[0] == "minspeed:":
            print "min speed"
            setSpeed(min_speed)
            ##stop()
        elif cmd[0] == "stopScripts":
            print "stopScripts"
            stop()  # gopigo
        elif cmd[0] == 'led:l:on':
            print "Left Led on :)"
            led_on(LED_L)
        elif cmd[0] == 'led:l:off':
            print "Left Led off :)"
            led_off(LED_L)
        elif cmd[0] == 'led:r:on':
            print "Right Led on :)"
            led_on(LED_R)
        elif cmd[0] == 'led:r:off':
            print "Right Led off :)"
            led_off(LED_R)
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
        elif cmd[0] == 'servo:on':
            enable_servo()
        elif cmd[0] == 'servo:off':
            disable_servo()
        elif cmd[0] == 'servo:pos':
            servo(cmd[1])

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
        elif cmd[0] == 'wait:elapsed:from:':
            time.sleep(getValue(cmd[1]))

        # Timers
        elif cmd[0] == 'timerReset':
            reset_timer()
        else: print "TODO:", cmd[0]

def runScript(script):
    setSpeed(current_speed)
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

reset_timer()
print "Voltage: " , volt()
#x = raw_input('What is pushed (ex:"whenClicked"): ')
findScripts("whenGreen")
