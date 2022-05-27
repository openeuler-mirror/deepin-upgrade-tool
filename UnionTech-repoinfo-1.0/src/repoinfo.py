#!/usr/bin/python3

import time
import os
import atexit
import subprocess
import re
#from threading import Timer
import logging
import signal

LOGFILE = "/var/log/repoinfomation.log"
RECOARDFILE = "/run/infomation/msg.txt"

def handler(sig, frame):
    delfile(RECOARDFILE)
    exit()

logging.basicConfig(filename = LOGFILE,level = logging.DEBUG)
signal.signal(signal.SIGTERM, handler)

def myrecoard(content):
    try:
        os.stat("/run/infomation/")
    except:
        os.mkdir("/run/infomation/")

    with open(RECOARDFILE, "w+") as f:
        read_data = f.read()
        f.truncate()   #清空文件
        f.write(content)
        f.close()
def delfile(filename):
    if os.path.exists(filename):
        try:
            os.remove(filename)
        except OSError:
            pass
def createlogfile():
    num = 0
    FNULL = open(os.devnull, 'w')
    proc=subprocess.Popen('/usr/bin/dnf-3 check-update',
            shell=True,
            stdin=None,
            stdout=subprocess.PIPE,
            stderr=FNULL)
    try:
        outs, errs = proc.communicate(timeout = 60 )
    except subprocess.TimeoutExpired:
        proc.kill()
        logging.info('Exec command timeout')
        myrecoard("")
        return 

    if proc.returncode == 1:
        logging.info('Connect repo server error')
        myrecoard("")
        return 
    for line in outs.decode("utf-8").splitlines():
        if re.search("uel20", line):
            num += 1
    msg="Available upgrade package: "+str(num)
    myrecoard(msg)
    logging.info(msg)

def main():
    logging.info("Main fun start")
    atexit.register(delfile,filename = LOGFILE)
    createlogfile()
    logging.info("Main fun end")

if __name__ == '__main__':
    main()
