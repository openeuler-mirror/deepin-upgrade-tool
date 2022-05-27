#!/usr/bin/python3

import os
import logging
import signal
from utrepoinfo.dnf import UtBase
from utrepoinfo.config import LOGFILE, RECOARDDIR, RECOARDFILE
from utrepoinfo.utils import sigterm_handler, timeout_handler

logging.basicConfig(filename=LOGFILE, level=logging.INFO)

signal.signal(signal.SIGTERM, sigterm_handler)


def recoard_msg(content):
    if not os.path.exists(RECOARDDIR):
        os.mkdir(RECOARDDIR)

    with open(RECOARDFILE, "w") as f:
        f.write(content)


def outtime():
    print("timeout...")


def createlogfile(timeout=60):
    try:
        signal.signal(signal.SIGALRM, timeout_handler)
        # 设置 timeout 秒的闹钟
        signal.alarm(timeout)
        # num = 0
        with UtBase() as base:
            rpmpkgs_detail = base.get_available_update_pkgs_details()
        msg = "Upgradable packages:" + str(len(rpmpkgs_detail))
        recoard_msg(msg)
        logging.info(msg)
        # 关闭闹钟
        signal.alarm(0)
    except RuntimeError as e:
        logging.info('get rpminfo timeout')
        recoard_msg("")
        return


def main():
    logging.info("Main fun start")
    createlogfile()
    logging.info("Main fun end")
