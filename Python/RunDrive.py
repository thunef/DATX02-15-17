#!/usr/bin/env python
import zipfile
import sys
import atexit
import json
import time
import datetime
import os
import RPi.GPIO as GPIO
from pprint import pprint
from random import randint
from gopigo import *
atexit.register(stop)

import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)

GPIO.setup(21, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(20, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(26, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(16, GPIO.IN, pull_up_down=GPIO.PUD_UP)


DELAY_BETWEEN_COMMANDS = 0.1 #Sec
DATE = datetime.datetime.now()
DiffSince2000 = datetime.date.today() - datetime.date(2000, 01, 01)

# hours, minutes, seconds
timer_started = [0,0,0]

ROTATIONTIME = 14 # For waiting on wheels to rotate

os.system("sudo mount -a")

loaded = False
while loaded == False:
    try:
      #archive = zipfile.ZipFile('/home/pi/python/drive.sb2', 'r')
      archive = zipfile.ZipFile('/mnt/usbdrive/drive.sb2', 'r')
      data=json.loads(archive.read('project.json'))
      loaded = True
    except:
      print "Failing"
      time.sleep(3)
      pass

loaded = False
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


def getValue(block):
    print "value of ", block, " type", type(block)

    if type(block) is unicode:
        return int(block)
    if type(block) is int:
        return block
    if type(block) is float:
        return block
    if block[0] == 'timestamp':
        return DiffSince2000.days
    if block[0] == 'timeAndDate':
        DATE = datetime.datetime.now()
        if (block[1] == 'minute'):
            return DATE.minute
        elif block[1] == 'second':
            return DATE.second
        elif block[1] == 'hour':
            return DATE.hour
    if block[0] == 'readVariable':
        return variables[block[1]]
    if block[0] == 'randomFrom:to:':
        return randint(block[1],block[2])
        #us_dist()
    if block[0] == 'getLine:ofList:':
        print "okidok getting position", block[1], " from ", block[2]
        tmp = lists[block[3]]
        return tmp[block[1]]

    if block[0] == 'lineCountOfList:':
        tmp = lists[block[2]]
        return tmp.length

    if block[0] == '%':
        return block[1] % block[2]

    #returns time  since the timer started.
    if block[0] == 'timer':
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

def executeBlock(block):
        #print "speed: ", current_speed
        ##print "\nrunning:"

        # Motion
        if block[0] == "forward:":
            print "framAt" , block[1]
            rot=getValue(block[1])
            enc_tgt(1,1,rot)    ## m1: 0 to disable targeting for motor 1, 1 to enable it
                                ## m2: 0 to disable targeting for motor 2, 1 to enable it
                                ## target: number of encoder pulses to target (18 per rotation). For moving the wheel by 2 rotations, target should be 36

            fwd()
            time.sleep(rot/ROTATIONTIME)
        elif block[0] == "backwards:":
            print "bakka" , block[1]
            rot=getValue(block[1])
            enc_tgt(1,1,rot)
            bwd()
            time.sleep(rot/ROTATIONTIME)
        elif block[0] == "turnRight:":
            print "rotate right " , block[1], " degrees"
            rot = int(getValue(block[1])/5.5)
            enc_tgt(0,1,rot)
            left()
            time.sleep(rot/ROTATIONTIME)
        elif block[0] == "turnLeft:":
            enable_encoders()
            print "rotate left ", block[1], " degrees"
            rot = int(getValue(block[1])/5.5)
            enc_tgt(1,0,rot)
            right()
            time.sleep(rot/ROTATIONTIME)
        elif block[0] == 'maxspeed:':
            print 'maxspeed'
            setSpeed(255) # 255 is the maximum speed of the gopigo
        elif block[0] == "accelerate:":
            print "IncSpeed: ",current_speed  ," with ", block[1]
            setSpeed(current_speed+getValue(block[1]))
        elif block[0] == "retardate:":
            print "slowing down:" ,current_speed  ," with ", block[1]
            setSpeed(current_speed-getValue(block[1]))
        elif block[0] == "minspeed:":
            print "min speed"
            setSpeed(min_speed)
            ##stop()
        elif block[0] == "stopScripts":
            print "stopScripts"
            stop()  # gopigo
        elif block[0] == 'led:l:on':
            print "Left Led on :)"
            led_on(LED_L)
        elif block[0] == 'led:l:off':
            print "Left Led off :)"
            led_off(LED_L)
        elif block[0] == 'led:r:on':
            print "Right Led on :)"
            led_on(LED_R)
        elif block[0] == 'led:r:off':
            print "Right Led off :)"
            led_off(LED_R)
        # Control
        elif block[0] == "doRepeat":
            print "doRepeat\n"
            for index in range(getValue(block[1])):
                executeChunkOfBlocks(block[2])
        elif block[0] == "doUntil":
            print "doUntil\n"
            while isTrue(block[1]) == False:
                executeChunkOfBlocks(block[2])
        elif block[0] == "doForever":
            print "going to loop forever!!"
            print block[1]
            while True:
                executeChunkOfBlocks(block[1])
        elif block[0] == 'doIf':
            print "doIf\n"
            print block[1]
            if isTrue(block[1]) :
                executeChunkOfBlocks(block[2])
        elif block[0] == 'doIfElse':
            print "doIfElse\n"
            if isTrue(block[1]):
                executeChunkOfBlocks(block[2])
            else:
                executeChunkOfBlocks(block[3])
        elif block[0] == 'servo:on':
            enable_servo()
        elif block[0] == 'servo:off':
            disable_servo()
        elif block[0] == 'servo:pos':
            servo(block[1])

        # Data
        elif block[0] =='setVar:to:':
            print "setVar ",block[1], " to: ", block[2], "\n"
            variables[block[1]] = getValue(block[2])
            print block[1] , " === " , variables[block[1]]
        elif block[0] =='changeVar:by:':
            print variables[block[1]]," change by ",block[2], " -- is it"
            variables[block[1]] += getValue(block[2])
            print variables[block[1]]
        elif block[0] =='append:toList:':
            print "mmokay ", block[2] , " add " , block[1]
            lists[block[2]].append(getValue(block[1]))
        elif block[0] =='insert:at:ofList:':
            print "mmokay ", block[3] , " add " , block[1] ," @",block[2]
            lists[block[3]].insert(block[2], getValue(block[1]))
        elif block[0] == 'wait:elapsed:from:':
            time.sleep(getValue(block[1]))

        # Timers
        elif block[0] == 'timerReset':
            reset_timer()
        else: print "TODO:", block[0]

def executeChunkOfBlocks(chunk):
    setSpeed(current_speed)
    for index in range(len(chunk)):
        executeBlock(chunk[index])
        time.sleep(DELAY_BETWEEN_COMMANDS)

def buttonPress(whichOne):
    for index in range(len(scripts)):
        #First 2 rows is gui posision, but script starts at [2]
        if scripts[index][2][0][0] == whichOne: #First(0) row is the event
            executeChunkOfBlocks(scripts[index][2])


if 'variables' in {x for x in data if x in 'variables'}:
    getVariables(data['variables'])

if 'lists' in {x for x in data if x in 'lists'}:
    getLists(data['lists'])

reset_timer()
print "Voltage: " , volt()


def green_callback(channel):
    print "Press Green ----------------------------------"
    GPIO.remove_event_detect(21)
    buttonPress("whenGreen")
    GPIO.add_event_detect(21, GPIO.FALLING, callback=green_callback, bouncetime=300)

def blue_callback(channel):
    print "Press Blue ----------------------------------"
    GPIO.remove_event_detect(26)
    buttonPress("whenBlue")
    GPIO.add_event_detect(26, GPIO.FALLING, callback=blue_callback, bouncetime=300)

def yellow_callback(channel):
    print "Press Yellow ----------------------------------"
    GPIO.remove_event_detect(16)
    buttonPress("whenYellow")
    GPIO.add_event_detect(16, GPIO.FALLING, callback=yellow_callback, bouncetime=300)

GPIO.add_event_detect(21, GPIO.FALLING, callback=green_callback, bouncetime=300)

GPIO.add_event_detect(26, GPIO.FALLING, callback=blue_callback, bouncetime=300)

GPIO.add_event_detect(16, GPIO.FALLING, callback=yellow_callback, bouncetime=300)

try:
    led_on(LED_L)
    led_on(LED_R)
    print "Waiting for input"
    GPIO.wait_for_edge(20, GPIO.FALLING)
    print "Here endeth the program.\n"

    led_off(LED_L)
    led_off(LED_R)
    args = sys.argv[:]

    args.insert(0, sys.executable)

    os.execv(sys.executable, args)

except KeyboardInterrupt:
    GPIO.cleanup()       # clean up GPIO on CTRL+C exit
GPIO.cleanup()           # clean up GPIO on normal exit
