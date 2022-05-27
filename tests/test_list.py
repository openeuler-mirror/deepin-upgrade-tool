# test_list = ["aa", "bb"]
# print(" ".join(test_list))
# json_str = """[
#     {
#         "name": "python-qt5-rpm-macros",
#         "release": "6.uel20",
#         "version": "5.11.3",
#         "arch": "noarch",
#         "downloadsize": 12276,
#         "downloadsize_human_readable": "12 k",
#         "srpm": "python-qt5-5.11.3-6.uel20.src.rpm",
#         "repo": "aa",
#         "summary": "RPM macros python-qt5",
#         "url": "http://www.riverbankcomputing.com/software/pyqt/",
#         "license": "GPLv3",
#         "desc": "RPM macros python-qt5."
#     },
#     {
#         "name": "python3-qt5",
#         "release": "6.uel20",
#         "version": "5.11.3",
#         "arch": "x86_64",
#         "downloadsize": 1104320,
#         "downloadsize_human_readable": "1.1 M",
#         "srpm": "python-qt5-5.11.3-6.uel20.src.rpm",
#         "repo": "aa",
#         "summary": "Python 3 bindings for Qt5",
#         "url": "http://www.riverbankcomputing.com/software/pyqt/",
#         "license": "GPLv3",
#         "desc": "Python 3 bindings for Qt5."
#     },
#     {
#         "name": "python3-qt5-base",
#         "release": "6.uel20",
#         "version": "5.11.3",
#         "arch": "x86_64",
#         "downloadsize": 2731180,
#         "downloadsize_human_readable": "2.6 M",
#         "srpm": "python-qt5-5.11.3-6.uel20.src.rpm",
#         "repo": "aa",
#         "summary": "Python 3 bindings for Qt5 base",
#         "url": "http://www.riverbankcomputing.com/software/pyqt/",
#         "license": "GPLv3",
#         "desc": "Python 3 bindings for Qt5 base."
#     }
# ]
# """
# import json
#
# pyobj = json.loads(json_str)
# # print(pyobj)
# for i in pyobj:
#     if i["name"] == "python3-qt5":
#         pyobj.remove(i)
#
# print(pyobj)
import datetime
tt=[
            {
                "author": "wangekrong <wangkerong@huawei.com> - 2019.1-2",
                "text": "- DESC:solve the issue which dispaly could not resolve keysym XF86FullScreen",
                "timestamp": "2021-06-28"
            }
        ]


def format_changelog(changelog):
    """Return changelog formatted as in spec file"""
    chlog_str = '* %s %s\n%s\n' % (
        datetime.datetime.strptime(changelog['timestamp'], '%Y-%m-%d').strftime("%a %b %d %Y"),
        changelog['author'],
        changelog['text'])
    return chlog_str

for i in tt:
    print(format_changelog(i))
