# Project org.deepin.upgrade

Deepin upgrade tool, when the user logs in, an updatable application pop-up window will pop up. Through the pop-up
window, you can open the Software Updater and select the software to update

## Dependencies

### Build dependencies

- python3-devel
- python3dist(setuptools)

### Runtime dependencies

- python3
- logrotate
- python3-PyQt5-base
- python3dist(psutil)
- dde-control-center

## Installation

### Build

````
$ rpmbuild com.deepin.update.spec
````

### Install

```
rpm -ivh com.deepin.upgrade-XXX-rpm
# or
dnf install com.deepin.upgrade-XXX-rpm
```


## Getting involved

We encourage you to report issues and contribute changes

* [Contribution guide for developers](https://www.openeuler.org/zh/community/contribution/) (English)
* [开发者代码贡献指南](https://www.openeuler.org/en/community/contribution/) (中文)

## Copyright

Copyright (C) 2022 Uniontech Software Technology Co., Ltd.

## License

[com.deepin.upgrade] is licensed under [GPL-3.0-only](LICENSE).
