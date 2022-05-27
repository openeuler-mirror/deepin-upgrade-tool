import setuptools
import glob
import os
from com_deepin_upgrade.config import HOME_DIR

logrotate_path = "/etc/logrotate.d"
desktop_path = "/usr/share/applications"
system_path = "/usr/lib/systemd"
home_dir = HOME_DIR
bin_dir = "/usr/bin"
policy_dir = "/usr/share/polkit-1/actions"
autostart_path = ".config/autostart/"
autostart_all = "/etc/skel/{}".format(autostart_path)
autostart_root = "/root/{}".format(autostart_path)

current_dir = os.path.dirname(os.path.abspath(__file__))


def get_version():
    version_file = os.path.join(current_dir, 'VERSION')
    with open(version_file, 'r', encoding="utf-8") as file:
        return file.read().strip()


def get_long_description():
    readme_file = os.path.join(current_dir, 'README.md')
    with open(readme_file, "r", encoding="utf-8") as file:
        return file.read()


setuptools.setup(
    name="com_deepin_upgrade",
    version=get_version(),
    license="GPLv3",
    author="weidong",
    author_email="weidong@uniontech.com",
    description="Deepin upgrade tool",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    url="https://gitlabxa.uniontech.com/server/incubator/UnionTech-repoinfo",
    packages=setuptools.find_packages(),
    install_requires=[
        # "PyQt5",
    ],
    include_package_data=True,
    entry_points={
        'console_scripts': [
            # 登陆通知命令
            'pkgs_upgrade_notify=com_deepin_upgrade.upgrade_notify:main',
            # rpm 安装命令
            'pkgs_install_tool=com_deepin_upgrade.dnf:install',
            # 仓库 查询命令
            'pkgs_upgrade_info=com_deepin_upgrade.upgrade_info:main',
            # 主界面
            'pkgs_upgrade_window=com_deepin_upgrade.window:main',
            # 增加可更新软件包统计命令，方便cui调用
            'pkgs_upgrade_count=com_deepin_upgrade.utils:get_available_update_rpmpkgs_number'
        ],
    },
    data_files=[
        (logrotate_path, glob.glob("data/logrotate/*")),
        (desktop_path, glob.glob("data/desktop/*")),
        (autostart_root, ["data/desktop/pkgs_upgrade_notify.desktop"]),
        (autostart_all, ["data/desktop/pkgs_upgrade_notify.desktop"]),
        (f"{system_path}/system-preset", ["data/service/98-pkgs-upgrade-info.preset"]),
        (f"{system_path}/system", ["data/service/pkgs-upgrade-info.service", "data/service/pkgs-upgrade-info.timer"]),
        (f"{home_dir}/icon", glob.glob("data/icon/*")),
        (f"{home_dir}/pixmaps", glob.glob("data/pixmaps/*")),
        (policy_dir, ["data/policy/org.deepin.pkexec.deepin-upgrade.policy"]),
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
