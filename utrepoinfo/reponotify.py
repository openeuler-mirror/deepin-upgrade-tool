import gi
import dbus
import gettext
import logging

gi.require_version('Notify', '0.7')
gi.require_version('Gtk', '3.0')
from gi.repository import Notify
from gi.repository import Gtk
from dbus.mainloop.glib import DBusGMainLoop
from utrepoinfo.utils import get_available_update_rpmpkgs
from utrepoinfo.config import LOG_FILE, LOGO
from utrepoinfo.window import main as main_window

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

    def notify(self):
        self.notification.add_action("Cancle", _("Cancle"), self.cancle_button)
        self.notification.add_action("Update", "Update", self.update_button)
        self.notification.show()

    def update_button(self, notification, action, user_data=None):
        print(action)
        main_window()
        Gtk.main_quit()

    def cancle_button(self, notification, action, user_data=None):
        print(action)
        Gtk.main_quit()


def upgrade_notify(*args):
    rpmpkgs = get_available_update_rpmpkgs()
    rpmpkgs_num = len(rpmpkgs)
    if rpmpkgs_num > 0:
        RpmUpdateNotify("There are {0} updates available".format(str(rpmpkgs_num))).notify()
        Gtk.main()


def main():
    # 登陆提醒用户更新
    upgrade_notify()
    # 监听锁定登陆
    DBusGMainLoop(set_as_default=True)
    bus = dbus.SystemBus()
    bus.add_signal_receiver(  # define the signal to listen to
        upgrade_notify,  # callback function
        'Unlock',  # signal name
        'org.freedesktop.login1.Session',  # interface
        'org.freedesktop.login1'  # bus name
    )
    mainloop = gi.repository.GLib.MainLoop()
    mainloop.run()


if __name__ == '__main__':
    main()
