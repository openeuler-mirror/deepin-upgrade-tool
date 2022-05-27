import gi
import gettext
import logging

gi.require_version('Notify', '0.7')
gi.require_version('Gtk', '3.0')
from gi.repository import Notify
from gi.repository import Gtk
from utrepoinfo.utils import get_available_update_rpmpkgs
from utrepoinfo.config import LOGFILE, LOGOPNG
from utrepoinfo.window import main as main_window

locale_path = '/usr/share/locale'
gettext.bindtextdomain('utrepoinfo', locale_path)
gettext.textdomain('utrepoinfo')
_ = gettext.gettext


class RpmUpdateNotify(object):
    def __init__(self, content):
        Notify.init("Software Updates Available")
        self.notification = Notify.Notification.new("Software Updates Available", content,
                                                    LOGOPNG)
        self.notification.set_urgency(Notify.Urgency.NORMAL)
        self.notification.set_urgency(2)
        self.notification.set_timeout(1000000)

    def notify(self):
        self.notification.add_action("Cancle", _("Cancle"), self.cancle_botton)
        self.notification.add_action("Update", "Update", self.action_update)
        self.notification.show()

    def action_update(self, notification, action, user_data=None):
        print(action)
        main_window()
        Gtk.main_quit()

    def cancle_botton(self, notification, action, user_data=None):
        print(action)
        Gtk.main_quit()


def main():
    logging.basicConfig(filename=LOGFILE, level=logging.INFO)
    rpmpkgs = get_available_update_rpmpkgs()
    rpmpkgs_num = len(rpmpkgs)
    if rpmpkgs_num > 0:
        RpmUpdateNotify("There are {0} updates available".format(str(rpmpkgs_num))).notify()
        Gtk.main()


if __name__ == '__main__':
    main()
