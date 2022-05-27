#!/usr/bin/python3

import os
import logging
import signal
from utrepoinfo.dnf import UtBase
from utrepoinfo.config import LOG_FILE, REPO_DATA_PATH, REPO_CLI_MSG, REPO_DATA
from utrepoinfo.utils import sigterm_handler, timeout_handler, write_file, write_pyobj_to_jsonfile

logging.basicConfig(filename=LOG_FILE, level=logging.INFO)

signal.signal(signal.SIGTERM, sigterm_handler)


def write_repoinfo_path(file, content):
    if not os.path.exists(REPO_DATA_PATH):
        os.mkdir(REPO_DATA_PATH)
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
        write_repoinfo_path(REPO_CLI_MSG, msg)
        write_pyobj_to_jsonfile(REPO_DATA, rpmpkgs_detail)
        logging.info(msg)
        # 关闭闹钟
        signal.alarm(0)
    except RuntimeError as e:
        logging.info('get rpminfo timeout')
        logging.info(e)
        write_repoinfo_path(REPO_CLI_MSG, "")
        return
    except Exception as e:
        write_repoinfo_path(REPO_CLI_MSG, "")
        logging.error("app error")
        logging.error(e)


def main():
    logging.info("Main fun start")
    createlogfile()
    logging.info("Main fun end")
