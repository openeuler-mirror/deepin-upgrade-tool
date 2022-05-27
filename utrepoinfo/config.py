import os
import sys
import signal

# python 版本
PY_VERSION_INFO = sys.version_info
# 转化为特定字符串的python版本
PY_VERSION_STR = "{major}.{minor}".format(major=PY_VERSION_INFO.major, minor=PY_VERSION_INFO.minor)
# log文件
LOG_FILE = "/var/log/repoinfomation.log"
# 存储dnf数据信息目录
REPO_DATA_PATH = "/var/lib/repoinfo"
# cui使用的数据文件
REPO_CLI_MSG = os.path.join(REPO_DATA_PATH, "msg.txt")
# 生成详细yum仓库数据
REPO_DATA = os.path.join(REPO_DATA_PATH, "pkgs.json")
# python 模块名称
PY_MODLE_NAME = "utrepoinfo"
# python 模块路径
PKG_PATH = "/usr/lib/python{pyversion}/site-packages/{name}/".format(pyversion=PY_VERSION_STR, name=PY_MODLE_NAME)
# logo路径
LOGO = "{datapath}/img/{pngname}".format(datapath=PKG_PATH, pngname="notify.png")
# 托盘区定时器刷新时间,单位ms，默认6h
TRAY_INTERVAL = 1000 * 60 * 60 * 6
# 通知和窗口之前的通信信号
CONNECT_SIGNAL = signal.SIGUSR1
# 主窗口命令
WINDOW_CMDLINE = ['/usr/bin/python3', '/usr/bin/utrpmupdatewindow']

