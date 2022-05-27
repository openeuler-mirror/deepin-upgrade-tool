#!/usr/bin/python3

import os
import logging
import signal
from utrepoinfo.dnf import UtBase
from utrepoinfo.config import LOGFILE, RECOARDDIR, RECOARDFILE, RPMPKGSDETAILS
from utrepoinfo.utils import sigterm_handler, timeout_handler, write_file, write_pyobj_file

logging.basicConfig(filename=LOGFILE, level=logging.INFO)

signal.signal(signal.SIGTERM, sigterm_handler)


def write_repoinfo_path(file, content):
    if not os.path.exists(RECOARDDIR):
        os.mkdir(RECOARDDIR)
    write_file(file, content)


def outtime():
    print("timeout...")


def createlogfile(timeout=120):
    try:
        signal.signal(signal.SIGALRM, timeout_handler)
        # 设置 timeout 秒的闹钟
        signal.alarm(timeout)
        # num = 0
        with UtBase() as base:
            rpmpkgs_detail = base.get_available_update_pkgs_details()
        msg = "Upgradable packages:" + str(len(rpmpkgs_detail))
        write_repoinfo_path(RECOARDFILE, msg)
        write_pyobj_file(RPMPKGSDETAILS, rpmpkgs_detail)
        logging.info(msg)
        # 关闭闹钟
        signal.alarm(0)
    except RuntimeError as e:
        logging.info('get rpminfo timeout')
        logging.info(e)
        write_repoinfo_path(RECOARDFILE,"")
        return
    except Exception as e:
        write_repoinfo_path(RECOARDFILE, "")
        logging.error("app error")
        logging.error(e)


def main():
    logging.info("Main fun start")
    createlogfile()
    logging.info("Main fun end")
