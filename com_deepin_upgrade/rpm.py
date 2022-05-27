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

import rpm


def get_local_rpmpkgs():
    """
    获取本地已安装的rpm包，类似rpm -qa
    :return:
    """
    local_rpmpkgs = {}
    rpmts = rpm.TransactionSet()
    for h in rpmts.dbMatch():
        local_rpmpkgs[h.name] = "{version}-{release}".format(version=h.version, release=h.release)
    return local_rpmpkgs
