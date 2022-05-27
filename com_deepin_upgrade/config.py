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
