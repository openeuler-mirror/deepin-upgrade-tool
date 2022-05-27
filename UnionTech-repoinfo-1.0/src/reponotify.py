import os
import time
import gi.repository.GLib
import dbus
from dbus.mainloop.glib import DBusGMainLoop
import subprocess

RECOARDFILE = "/var/infomation/msg.txt"

def Notify(msg):
    subprocess.run(["gdbus",\
        "call",\
        "--session",\
        "--dest",\
        "org.freedesktop.Notifications",\
        "--object-path",\
        "/org/freedesktop/Notifications",\
        "--method",\
        "org.freedesktop.Notifications.Notify",\
        "rpm update infomation",\
        "1",\
        "/usr/share/repoinfo/notify.png", \
        "",\
        msg,\
        "[]",\
        "{}",\
        "60000"],stdin=None, input=None, stdout=None, stderr=None, shell=False, timeout=None, check=False)

#first login display the notifycation 
if os.access(RECOARDFILE, os.R_OK):
    f = open(RECOARDFILE)
    msg = f.read()
    if len(msg) != 0:
        Notify(msg)
    f.close()

def locker_callback(*args):
    if os.access(RECOARDFILE, os.R_OK):
        f = open(RECOARDFILE)
        msg = f.read()
        if len(msg) != 0:
            Notify(msg)
        f.close()
DBusGMainLoop(set_as_default=True)
bus = dbus.SystemBus()
bus.add_signal_receiver(                                  # define the signal to listen to
locker_callback,                                      # callback function
    'Unlock',                                         # signal name
    'org.freedesktop.login1.Session',  # interface
    'org.freedesktop.login1'  # bus name
)
mainloop = gi.repository.GLib.MainLoop()
mainloop.run()
