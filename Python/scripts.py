#!/usr/bin/env python
import json
import os
import shutil
import zipfile
#import gopigo
from collections import defaultdict

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

def getJson(name):
    zip_file = zipfile.ZipFile(name)
    for member in zip_file.namelist():
        if member == 'project.json':
           json_data = zip_file.read(member)
           zip_file.close()
           return json_data

def runCommand(command):
    script_str = command[0]
    script_for = command[1]
#    print "run:", script_str, "for:", script_for
    # TODO: Rewrite this later
    if script_str == "forward:":
        print "framAt:",  script_for
        if speed == 0:
#            increase_speed() # gopigo
            speed = read_motor_speed()
        i = 0
        for k in range(script_for):
            i = i + 1
#        stop() # gopigo
        speed = 0

    elif script_str == 'accelerate:':
        print script_str
#        increase_speed()

    elif script_str == 'retardate:':
        print script_str
#        decrease_speed()

    elif script_str == 'maxspeed:':
        print script_str
#        set_speed(255)

    elif script_str == 'nospeed:':
        print script_str
#        set_speed(0)

    elif script_str == "stopScripts":
        print script_str
#        stop()  # gopigo

    elif script_str == "doIf":
        if isTrue(command[1]) :
            runScript(command[2])

    elif script_str == "doIfElse":
        if isTrue(command[1]):
            runScript(command[2])
        else:
            runScript(command[3])

    elif script_str == "doForever":
        loop_commands = command[2]
        while True:
            print script_str[1]
            runCommands(loop_commands)

    elif script_str == "doRepeat":
        loop_times = command[1]
        loop_commands = command[2]
        for k in range(loop_times):
            runCommands(loop_commands)

    elif script_str == 'setVar:to:':
        variables[command[1]] = command[2]
        print command[1],"  =  ",variables[command[1]]

    elif script_str == 'changeVar:by:':
        variables[command[1]] += command[2]
        print command[1],"  =  ",variables[command[1]]

    elif script_str == 'led:on:':
        print script_str
#        led_on()
    elif script_str == 'led:off:':
        print script_str
#        led_off():
    elif script_str == 'servo:on':
        print script_str
#        enable_servo()
    elif script_str == 'servo:off':
        print script_str
#        disable_servo()
    elif script_str == 'servo:pos':
        print script_str
        servo(command[1] % 180)

def runCommands(commands):
    for index in range(len(commands)):
        runCommand(commands[index])


def start(name):
    json_raw_data = getJson(name)
    json_data     = json.loads(json_raw_data)
    json_scripts  = json_data['children'][0]['scripts']

    if 'variables' in {x for x in json_data if x in 'variables'}:
        getVariables(json_data['variables'])

    if 'lists' in {x for x in json_data if x in 'lists'}:
        getLists(json_data['lists'])

    runCommands(json_scripts)



if __name__ == "__main__":
    import sys
    start(sys.argv[1])
