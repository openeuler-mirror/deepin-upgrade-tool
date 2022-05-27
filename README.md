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

## Getting help

Any usage issues can ask for help via

* [Gitter](https://gitter.im/orgs/linuxdeepin/rooms)
* [IRC channel](https://webchat.freenode.net/?channels=deepin)
* [Forum](https://bbs.deepin.org)
* [WiKi](https://wiki.deepin.org/)

## Getting involved

We encourage you to report issues and contribute changes

* [Contribution guide for developers](https://github.com/linuxdeepin/developer-center/wiki/Contribution-Guidelines-for-Developers-en)
  . (English)
* [开发者代码贡献指南](https://github.com/linuxdeepin/developer-center/wiki/Contribution-Guidelines-for-Developers) (中文)

## License

[Project name] is licensed under [GPLv3](LICENSE).
