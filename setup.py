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
    packages=setuptools.find_packages(),
    install_requires=[
        "PyQt5",
    ],
    entry_points={
        'console_scripts': ['reponotify=utrepoinfo.reponotify:main',
                            'repoinfo=utrepoinfo.repoinfo:main'],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
