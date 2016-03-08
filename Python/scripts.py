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
    elif script_str == "stopScripts":
        print "stopScripts"
#        stop()  # gopigo
        speed = 0
    elif script_str == "doIf":
        print script_str
        if isTrue(command[1]) :
                runScript(command[2])
    elif command[0] == "doIfElse":
        print "doIfElse"
        if isTrue(command[1]):
            runScript(command[2])
        else:
            runScript(command[3])
    elif script_str == "doForever":
        print "looping forever"
        loop_commands = command[2]
        while True:
            print script_str[1]
            runCommands(loop_commands)
    elif script_str == "doRepeat":
        print "doRepeat"
        loop_commands = command[2]
        for k in range(script_for):
            runCommands(loop_commands)
    elif script_str == 'setVar:to:':
        variables[command[1]] = command[2]
        print command[1],"  =  ",variables[command[1]]
    elif script_str == 'changeVar:by:':
        variables[command[1]] += command[2]
        print command[1],"  =  ",variables[command[1]]

def runCommands(commands):
    for index in range(len(commands)):
        runCommand(commands[index])


def start(name):
    json_raw_data = getJson(name)
    json_data     = json.loads(json_raw_data)
#    json_scripts  = []
    json_scripts  = json_data['children'][0]['scripts']
    json_lists    = json_data['lists']

    getVariables(json_data['variables'])
    getLists(json_lists)
    runCommands(json_scripts)



if __name__ == "__main__":
    import sys
    start(sys.argv[1])
