#!/usr/bin/python3

import os
import subprocess
import re
import logging
import signal

LOGFILE = "/var/log/repoinfomation.log"
RECOARDDIR = "/var/infomation"
RECOARDFILE = os.path.join(RECOARDDIR, "msg.txt")
logging.basicConfig(filename=LOGFILE, level=logging.DEBUG)


def handler(sig, frame):
    delfile(RECOARDFILE)
    exit()


signal.signal(signal.SIGTERM, handler)


def myrecoard(content):
    if not os.path.exists(RECOARDDIR):
        os.mkdir(RECOARDDIR)

    with open(RECOARDFILE, "w") as f:
        f.write(content)


def delfile(filename):
    if os.path.exists(filename):
        try:
            os.remove(filename)
        except OSError:
            pass


def createlogfile():
    num = 0
    FNULL = open(os.devnull, 'w')
    proc = subprocess.Popen('/usr/bin/dnf-3 check-update',
                            shell=True,
                            stdin=None,
                            stdout=subprocess.PIPE,
                            stderr=FNULL)
    try:
        outs, errs = proc.communicate(timeout=60)
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
    logging.info('Connect repo server success')
    msg = "Upgradable packages:" + str(num)
    myrecoard(msg)
    logging.info(msg)


def main():
    logging.info("Main fun start")
    createlogfile()
    logging.info("Main fun end")


if __name__ == '__main__':
    print(RECOARDFILE)
    # main()
