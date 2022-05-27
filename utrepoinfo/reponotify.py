import gi
import gettext
import os
import subprocess
import psutil
import dbus
import signal
import logging

gi.require_version('Notify', '0.7')
gi.require_version('Gtk', '3.0')
from gi.repository import Notify, GLib
from dbus.mainloop.glib import DBusGMainLoop
from utrepoinfo.utils import get_available_update_rpmpkgs
from utrepoinfo.config import CONNECT_SIGNAL, LOGO, LOG_FILE, WINDOW_CMDLINE
from threading import Thread

locale_path = '/usr/share/locale'
gettext.bindtextdomain('utrepoinfo', locale_path)
gettext.textdomain('utrepoinfo')
_ = gettext.gettext


class RpmUpdateNotify(object):
    def __init__(self, content):
        """
        Args:
            content:str
        """
        # 初始化通知信息
        Notify.init(_("Software Updates Available"))
        self.notification = Notify.Notification.new(_("Software Updates Available"), content,
                                                    LOGO)
        self.notification.set_urgency(Notify.Urgency.NORMAL)
        self.notification.set_urgency(2)
        self.notification.set_hint('x-deepin-action-_details', GLib.Variant.new_string(WINDOW_CMDLINE[1]))

        # 使用正常超时机制，不再增加永不过期
        # self.notification.set_timeout(1000000)

    def notify_action(self):
        # 带有动作的通知
        self.notification.add_action("_cancle", _("Cancle"), self.cancle_button)
        self.notification.add_action("_details", _("Details"), self.detail_button)
        self.notify()

    def notify(self):
        # 不带动作的通知
        self.notification.show()

    def detail_button(self, notification, action, user_data=None):
        # 详细信息按钮
        logging.debug(action)

    def cancle_button(self, notification, action, user_data=None):
        # 取消按钮
        logging.debug(action)


def get_session_cmd_pid(sid, cmdline=None):
    """
    Gets the PID of the specified command in the same session

    Args:
        sid: session id
        cmdline: command

    Returns:

    """
    if cmdline is None:
        cmdline = WINDOW_CMDLINE
    pids = []
    # 遍历进程列表，获取匹配的进程列表
    for proc in psutil.process_iter(['pid', 'cmdline']):
        pinfo = proc.info
        if pinfo['cmdline'] == cmdline:
            pids.append(pinfo['pid'])
    # 检测进程列表中是否存在指定session的进程，存在就返回pid,不存在返回None
    for pid in pids:
        if os.getsid(pid) == sid:
            return pid
    return None


def get_user_cmd_pid(uid, cmdline=None):
    """
    Gets the PID of the specified command in the same uid

    Args:
        uid: user id
        cmdline: command

    Returns:

    """
    if cmdline is None:
        cmdline = WINDOW_CMDLINE
    # 遍历进程列表，获取匹配的进程列表
    for proc in psutil.process_iter(['pid', 'uids', 'cmdline']):
        pinfo = proc.info
        if pinfo['cmdline'] == cmdline and pinfo['uids'].real == uid:
            return pinfo['pid']
    return None


def update_notify(*args):
    """
    update notifaction
    Args:
        *args:

    Returns:

    """
    # 获取当前用户的id
    uid = os.getuid()
    logging.debug("uid is :{}".format(uid))
    pid = get_user_cmd_pid(uid)
    logging.debug("cmd pid is: {}".format(pid))
    # 获取rpm更新列表
    rpmpkgs = get_available_update_rpmpkgs()
    rpmpkgs_num = len(rpmpkgs)
    logging.debug("The number of RPM packages is: {}".format(rpmpkgs_num))
    # 当存在可更新的rpm包时通知
    if rpmpkgs_num > 0:
        msg = gettext.ngettext("There is {0} update available".format(str(rpmpkgs_num)),
                               "There are {0} updates available".format(str(rpmpkgs_num)), rpmpkgs_num)
        # 如果存在同一会话下的桌面进程，则发的通知不带按钮
        if pid is not None:
            RpmUpdateNotify(msg).notify()
        # 如果当前桌面没有驻留进程，则发带按钮的通知
        else:
            RpmUpdateNotify(msg).notify_action()


def lock_window(*args):
    # 锁定窗口方法
    sid = os.getsid(os.getpid())
    logging.debug("sid is :{}".format(sid))
    pid = get_session_cmd_pid(sid)
    logging.debug("session id is{}".format(pid))
    if pid is not None:
        os.kill(pid, signal.SIGKILL)


def main():
    # logging.basicConfig(
    #     level=logging.DEBUG,
    #     format='%(levelname)s %(asctime)s %(filename)s[line:%(lineno)d] %(message)s',
    #     datefmt='%Y-%m-%d %H:%M:%S'
    # )
    logging.debug('Send first notification')
    update_notify()
    logging.debug('Start to enter the daemon and listen for the login of the current session')
    DBusGMainLoop(set_as_default=True)
    system_bus = dbus.SystemBus()
    system_bus.add_signal_receiver(  # define the signal to listen to
        update_notify,  # callback function
        signal_name='Unlock',
        dbus_interface='org.freedesktop.login1.Session',
        bus_name='org.freedesktop.login1'  # system_bus name
    )
    mainloop = gi.repository.GLib.MainLoop()
    mainloop.run()


if __name__ == '__main__':
    main()
