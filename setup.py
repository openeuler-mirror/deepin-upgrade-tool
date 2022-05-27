import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="utrepoinfo",
    version="2.0",
    author="weidong",
    author_email="weidong@uniontech.com",
    description="Available package information display",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlabxa.uniontech.com/server/incubator/UnionTech-repoinfo",
    packages=["utrepoinfo"],
    # install_requires=[
    #     "PyQt5",
    # ],
    include_package_data=True,
    entry_points={
        # reponotify 通知命令
        'console_scripts': ['reponotify=utrepoinfo.reponotify:main',
                            # utrpminstall 安装命令
                            'utrpminstall=utrepoinfo.dnf:install',
                            # repoinfo 查询命令
                            'repoinfo=utrepoinfo.repoinfo:main'],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
