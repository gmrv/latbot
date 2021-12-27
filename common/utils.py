import os
from time import sleep

from common import config


def run_command(command, delay=5):
    if command != "#":
        stream = os.popen('echo "%s" > ./host/commandpipe' % command)
        sr = stream.read()
        sleep(delay)
    try:
        f = open("./host/output", "r")
        output = f.read()
        f.close()
    except OSError:
        output = str(OSError)
    if len(output) < 1:
        output = "no output"
    return output + " "


def get_commands_list():
    f = open("./host/commands", "r")
    output = f.read()
    f.close()
    return output.splitlines()


def set_app_root_path():
    """
    Finding out of running service path

    root     25678  0.0  0.3 113304  2792 ?        Ss   23:24   0:00 /bin/bash /home/master/docker/latbot/dopipe.sh
    cd $(ps aux | grep -Eo "/[^ ]*dopipe.sh" | grep -Eo "/.*/")

    "/[^ ]*dopipe.sh" - get the last part /home/master/docker/latbot/dopipe.sh
    / - begins with /
    [^ ]* - any numbers any chars except space
    dopipe.sh - ends with dopipe.sh

    /home/master/docker/latbot/dopipe.sh
    "/.*/" - entire path without dopipe.sh
    :return:
    """
    path = run_command("ps aux | grep -Eo '/[^ ]*dopipe.sh' | grep -Eo '/.*/'", delay=1)

    if path[0] == '/':
        app_config = config.get_config()
        app_config.APP_ABSOLUTE_PATH = path
        _ = run_command("cd " + path, delay=1)
