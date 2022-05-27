import os
import sys

PYTHONVERSIONINFO = sys.version_info
PYVERSION = "{major}.{minor}".format(major=PYTHONVERSIONINFO.major, minor=PYTHONVERSIONINFO.minor)
LOGFILE = "/var/log/repoinfomation.log"
RECOARDDIR = "/var/infomation"
RECOARDFILE = os.path.join(RECOARDDIR, "msg.txt")
RPMPKGSDETAILS = os.path.join(RECOARDDIR, "pkgs.json")
PYPINAME = "utrepoinfo"
DATAPATH = "/usr/lib/python{pyversion}/site-packages/{name}/".format(pyversion=PYVERSION, name=PYPINAME)
LOGOPNG = "{datapath}/img/{pngname}".format(datapath=DATAPATH, pngname="notify.png")
