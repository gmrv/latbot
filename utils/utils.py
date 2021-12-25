import os
from time import sleep

import utmp
from telegram.ext import CallbackContext
from utils.lastb_entry import LastbEntry


def get_last_btmp_entry():
    with open('/var/log/btmp', 'rb') as fd:
        buf = fd.read()
        for entry in utmp.read(buf):
            pass
            # print(entry.time, entry.type, entry)
    last_entry = LastbEntry(username=entry.user, host=entry.host, timestamp=entry.sec)
    return last_entry


def remove_job_if_exists(name: str, context: CallbackContext) -> bool:
    """Remove job with given name. Returns whether job was removed."""
    current_jobs = context.job_queue.get_jobs_by_name(name)
    if not current_jobs:
        return False
    for job in current_jobs:
        job.schedule_removal()
    return True


def run_command(command, delay=5):
    """Sends explanation on how to use the bot."""
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
    """Sends explanation on how to use the bot."""
    f = open("./host/commands", "r")
    output = f.read()
    f.close()
    return output.splitlines()