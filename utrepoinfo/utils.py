import signal
import time
import os
from utrepoinfo.config import RECOARDFILE


def delfile(filename):
    if os.path.exists(filename):
        try:
            os.remove(filename)
        except OSError:
            pass


def sigterm_handler(sig, frame):
    delfile(RECOARDFILE)
    exit()


def timeout_handler(sig, frame):
    raise RuntimeError


if __name__ == '__main__':
    pass
