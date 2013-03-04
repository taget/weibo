#!/usr/bin/python
import subprocess
from subprocess import Popen, PIPE, STDOUT
import os
import sys
import traceback
import logging
from types import *


class TermColor(object):
    black = 30
    red = 31
    green = 32
    yellow = 33
    blue = 34
    magenta = 35
    cyan = 36
    white = 37


log_file = "./util.log"

formatter = logging.Formatter(fmt='%(asctime)s - %(levelname)s - %(module)s - %(message)s')
handler = logging.FileHandler(log_file)
handler.setFormatter(formatter)
logger = logging.getLogger("test")
logger.setLevel(logging.ERROR)
logger.addHandler(handler)

failed = 0
ok = 0

def exec_command(argv):
    """
    This function executes a given shell command.
    """
    rc = 0
    out = ''
    err = ''
    try:
        p = Popen(argv, shell=True, stdout=PIPE,
                             stderr=PIPE)
        out, err = p.communicate()
        rc = p.returncode
    except:
        logger.error(traceback.format_exc())

    return (rc, out, err)


def failed_print(msg, out, err):
    sys.stdout.write('\x1b[%s;1m%s\x1b[0m' % (TermColor.red, '[FAILED]'))
    sys.stdout.write('---%s\n' % msg)
    sys.stdout.flush()
    logger.error(msg + '\n' + out + '\n' + err)
    global failed
    failed = failed + 1
    return 0


def tested_print(msg, out):
    sys.stdout.write('\x1b[%s;1m%s\x1b[0m' % (TermColor.green, '[  OK  ]'))
    sys.stdout.write('---%s\n' % msg)
    sys.stdout.flush()
    logger.info(msg + '\n' + out)
    global ok
    ok = ok + 1
    return 0


#flag : True - 0 is OK
#flag : False - non 0 is OK
def test(cmd, testname, flag = True):
    rc = -1
    out = ''
    err = ''

    if type(cmd) is InstanceType:
		# cmd is a class instance
        rc, out, err = cmd.runtest()
    elif type(cmd) is StringType:
		# cmd is a command line
        rc, out, err = exec_command(cmd)
    elif type(cmd) is FunctionType:
        # Run function test
        rc, out, err = cmd()
    else:
        pass 
    if rc == 0 and flag == True:
        tested_print(testname, out)
    elif flag == True:
        failed_print(testname, out, err)
    else :
        tested_print(testname, out)

    return rc


def subprocess_closefds(*args, **kwargs):
    kwargs.update({
        "close_fds": True
    })

    return subprocess.Popen(*args, **kwargs)


def system_closefds(cmd):
    proc = subprocess_closefds(cmd, shell=True)
    return proc.wait()
