import os
import json
from utrepoinfo.config import RECOARDFILE


def del_file(filename):
    if os.path.exists(filename):
        try:
            os.remove(filename)
        except OSError:
            pass


def write_file(file, content):
    with open(file, "w") as f:
        f.write(content)


def write_pyobj_file(file, obj):
    with open(file, 'w') as f:
        json.dump(obj, f, indent=4)


def sigterm_handler(sig, frame):
    del_file(RECOARDFILE)
    exit()


def timeout_handler(sig, frame):
    raise RuntimeError


if __name__ == '__main__':
    pass
