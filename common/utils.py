import os
from time import sleep


def run_command(command, delay=5):
    if command != "#":
        stream = os.popen('echo "%s" > ./host/commandpipe' % command)
        output = stream.read()
        sleep(delay)
    f = open("./host/output", "r")
    output = f.read()
    f.close()
    if len(output) < 1:
        output = "no output"
    return output + " "


def get_commands_list():
    f = open("./host/commands", "r")
    output = f.read()
    f.close()
    return output.splitlines()
