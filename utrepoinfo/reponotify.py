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
from gi.repository import Notify
from gi.repository import Gtk
from dbus.mainloop.glib import DBusGMainLoop
from utrepoinfo.utils import get_available_update_rpmpkgs
from utrepoinfo.config import CONNECT_SIGNAL, LOGO, LOG_FILE

window_cmdline = ['/usr/bin/python3', '/usr/bin/utrpmupdatewindow']
locale_path = '/usr/share/locale'
gettext.bindtextdomain('utrepoinfo', locale_path)
gettext.textdomain('utrepoinfo')
_ = gettext.gettext


class RpmUpdateNotify(object):
    def __init__(self, content):
        Notify.init("Software Updates Available")
        self.notification = Notify.Notification.new("Software Updates Available", content,
                                                    LOGO)
        self.notification.set_urgency(Notify.Urgency.NORMAL)
        self.notification.set_urgency(2)
        self.notification.set_timeout(1000000)

    def notify_action(self):
        self.notification.add_action("Cancle", _("Cancle"), self.cancle_button)
        self.notification.add_action("Update", _("Update"), self.update_button)
        self.notify()

    def notify(self):
        self.notification.show()

    def update_button(self, notification, action, user_data=None):
        print(action)
        subprocess.Popen(window_cmdline)
        Gtk.main_quit()

    def cancle_button(self, notification, action, user_data=None):
        print(action)
        Gtk.main_quit()


def get_session_cmd_pid(sid, cmdline=None):
    if cmdline is None:
        cmdline = window_cmdline
    pids = []
    for proc in psutil.process_iter(['pid', 'cmdline']):
        pinfo = proc.info
        if pinfo['cmdline'] == cmdline:
            pids.append(pinfo['pid'])
    for pid in pids:
        if os.getsid(pid) == sid:
            return pid
    return None


def update_notify(*args):
    sid = os.getsid(os.getpid())
    logging.debug("sid is :{}".format(sid))
    pid = get_session_cmd_pid(sid)
    logging.debug("获取到session下的pid是{}".format(pid))
    rpmpkgs = get_available_update_rpmpkgs()
    rpmpkgs_num = len(rpmpkgs)
    if rpmpkgs_num > 0:
        if pid is not None:
            RpmUpdateNotify("There are {0} updates available".format(str(rpmpkgs_num))).notify()
        else:
            RpmUpdateNotify("There are {0} updates available".format(str(rpmpkgs_num))).notify_action()
        Gtk.main()


def lock_window(*args):
    sid = os.getsid(os.getpid())
    logging.warning("sid is :{}".format(sid))
    pid = get_session_cmd_pid(sid)
    logging.warning("获取到session下的pid是{}".format(pid))
    if pid is not None:
        os.kill(pid, signal.SIGKILL)


def main():
    update_notify()
    DBusGMainLoop(set_as_default=True)
    system_bus = dbus.SystemBus()
    system_bus.add_signal_receiver(  # define the signal to listen to
        update_notify,  # callback function
        signal_name='Unlock',
        dbus_interface='org.freedesktop.login1.Session',
        bus_name='org.freedesktop.login1'  # system_bus name
    )
    # system_bus.add_signal_receiver(  # define the signal to listen to
    #     lock_window,  # callback function
    #     signal_name='Lock',
    #     dbus_interface='org.freedesktop.login1.Session',
    #     bus_name='org.freedesktop.login1'  # system_bus name
    # )
    mainloop = gi.repository.GLib.MainLoop()
    mainloop.run()


if __name__ == '__main__':
    main()
