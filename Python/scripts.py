#!/usr/bin/env python
import json
import os
import shutil
import zipfile
#from collections import deque


expressions = [
    'doRepeat',
    'doForever',
    'forward:'
    'turnRight:'
    'turnLeft:'
]

code_to_run = []

def getJson(name):
    zip_file = zipfile.ZipFile(name)
    for member in zip_file.namelist():
        if member == 'project.json':
           json_data = zip_file.read(member)
           zip_file.close()
           return json_data

def runCommand(command):
    script_str = str(command[0])
    script_for = command[1]
    print "run:", script_str, "for:", script_for

def runCommands(commands):
    for index in range(len(commands)):
        runCommand(commands[index])

def getCommands(json_data):
    command_list = []
    for k in range(len(json_data[0][2])):
#        print json_data[0][2][k]
        tmp = json_data[0][2][k]
        print "tmp:", tmp
        for n in range(len(tmp)):
            if tmp[n] == 'doRepeat':


    print "Command_list:", command_list
    return command_list

def start(name):
    json_raw_data = getJson(name)
    json_data     = json.loads(json_raw_data)
    json_scripts  = json_data['children'][0]['scripts']

    command_list = getCommands(json_scripts)

    runCommands(command_list)

if __name__ == "__main__":
    import sys
    start(sys.argv[1])
