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
import sys
import signal

# python 版本
PY_VERSION_INFO = sys.version_info
# 转化为特定字符串的python版本
PY_VERSION_STR = "{major}.{minor}".format(major=PY_VERSION_INFO.major, minor=PY_VERSION_INFO.minor)
# log文件
LOG_FILE = "/var/log/pkgs_upgrade.log"
# home 目录
HOME_DIR = "/var/lib/pkgs_upgrade"
# 存储dnf数据信息目录
REPO_DATA_PATH = "{}/data".format(HOME_DIR)
# cui使用的数据文件
REPO_CLI_MSG = os.path.join(REPO_DATA_PATH, "msg.txt")
# 生成详细yum仓库数据
REPO_DATA = os.path.join(REPO_DATA_PATH, "pkgs.json")
# python 模块名称
PY_MODLE_NAME = "com_deepin_upgrade"
# python 模块路径
PKG_PATH = "/usr/lib/python{pyversion}/site-packages/{name}/".format(pyversion=PY_VERSION_STR, name=PY_MODLE_NAME)
# logo路径
LOGO = "{home_dir}/icon/{png_name}".format(home_dir=HOME_DIR, png_name="window_notify.png")
# pixmaps path
PIXMAPS_PATH = "{home_dir}/pixmaps".format(home_dir=HOME_DIR)
# 托盘区定时器刷新时间,单位ms，默认6h
TRAY_INTERVAL = 1000 * 60 * 60 * 6
# 通知和窗口之前的通信信号
CONNECT_SIGNAL = signal.SIGUSR1
# 主窗口命令
WINDOW_CMDLINE = ['/usr/bin/python3', '/usr/bin/pkgs_upgrade_window']
LOCALE_PATH = '/usr/share/locale'
I18N_DOMAIN = PY_MODLE_NAME
