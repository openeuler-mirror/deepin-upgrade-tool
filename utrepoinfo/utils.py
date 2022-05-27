import os
import json
import logging
from utrepoinfo.config import RECOARDFILE, RPMPKGSDETAILS
from utrepoinfo.rpm import get_local_rpmpkgs


def del_file(filename):
    if os.path.exists(filename):
        try:
            os.remove(filename)
        except OSError:
            pass


def write_file(file, content):
    with open(file, "w") as f:
        f.write(content)


def write_pyobj_to_jsonfile(file, obj):
    with open(file, 'w') as f:
        json.dump(obj, f, indent=4)


def read_jsonfile_to_pyobj(file):
    with open(file, 'r') as f:
        return json.load(f)


def sigterm_handler(sig, frame):
    del_file(RECOARDFILE)
    exit()


def timeout_handler(sig, frame):
    raise RuntimeError


def get_available_update_rpmpkgs():
    try:
        rpmpkgs = read_jsonfile_to_pyobj(RPMPKGSDETAILS)
        local_rpms = get_local_rpmpkgs()
        for i in rpmpkgs[:]:
            if local_rpms[i["name"]] == "{version}-{release}".format(version=i["version"], release=i["release"]):
                rpmpkgs.remove(i)
    except Exception as e:
        rpmpkgs = []
        logging.error("Can't get rpmpkgs")
        logging.error(e)
    return rpmpkgs


if __name__ == '__main__':
    pass
