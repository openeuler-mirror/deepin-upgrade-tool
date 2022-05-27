import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="com_deepin_upgrade",
    version="1.1",
    author="weidong",
    author_email="weidong@uniontech.com",
    description="Deepin upgrade tool",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlabxa.uniontech.com/server/incubator/UnionTech-repoinfo",
    packages=["com_deepin_upgrade"],
    # install_requires=[
    #     "PyQt5",
    # ],
    include_package_data=True,
    entry_points={
        # reponotify 通知命令
        'console_scripts': ['pkgs_upgrade_notify=com_deepin_upgrade.upgrade_notify:main',
                            # utrpminstall 安装命令
                            'pkgs_install_tool=com_deepin_upgrade.dnf:install',
                            # repoinfo 查询命令
                            'pkgs_upgrade_info=com_deepin_upgrade.upgrade_info:main',
                            # 主界面
                            'pkgs_upgrade_window=com_deepin_upgrade.window:main',
                            # 增加可更新软件包统计命令，方便cui调用
                            'pkgs_update_count=com_deepin_upgrade.utils:get_available_update_rpmpkgs_number'
                            ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GPL License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
