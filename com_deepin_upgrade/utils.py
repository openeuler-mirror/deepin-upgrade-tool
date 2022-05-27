"""
Copyright (C) 2022 Uniontech Software Technology Co., Ltd.

This program is free software; you can redistribute it and/or modify it under the terms of version 3 of the GNU General
 Public License as published by the Free Software Foundation.

This program is distributed in the hope that it will be useful,but WITHOUT ANY WARRANTY; without even the implied
warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program; If not,
see <https://www.gnu.org/licenses/gpl-3.0.html&gt;.

To contact us about this file by physical or electronic mail, you may find current contact information at
 https://www.uniontech.com/.
"""

import os
import json
import logging
import datetime
from com_deepin_upgrade.config import REPO_CLI_MSG, REPO_DATA
from com_deepin_upgrade.rpm import get_local_rpmpkgs


class ComplexEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, datetime.date):
            return obj.strftime('%Y-%m-%d')
        else:
            return json.JSONEncoder.default(self, obj)


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
        json.dump(obj, f, indent=4, cls=ComplexEncoder)


def read_jsonfile_to_pyobj(file):
    with open(file, 'r') as f:
        return json.load(f)


def sigterm_handler(sig, frame):
    del_file(REPO_CLI_MSG)
    exit()


def timeout_handler(sig, frame):
    raise RuntimeError


def get_available_update_rpmpkgs():
    try:
        rpmpkgs = read_jsonfile_to_pyobj(REPO_DATA)
        local_rpms = get_local_rpmpkgs()
        for i in rpmpkgs[:]:
            if local_rpms[i["name"]] == "{version}-{release}".format(version=i["version"], release=i["release"]):
                rpmpkgs.remove(i)
    except Exception as e:
        rpmpkgs = []
        logging.error("Can't get rpmpkgs")
        logging.error(e)
    return rpmpkgs


def get_available_update_rpmpkgs_number():
    number = len(get_available_update_rpmpkgs())
    print(number)
    return number


if __name__ == '__main__':
    pass
