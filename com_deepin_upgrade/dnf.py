import logging
import datetime
import argparse
import re
import rpm
import dnf
import gettext
import dnf.cli.progress
from dnf.cli.format import format_number
from dnf.cli.output import Output, CliTransactionDisplay
from com_deepin_upgrade.config import I18N_DOMAIN, LOCALE_PATH

locale_path = LOCALE_PATH
gettext.bindtextdomain(I18N_DOMAIN, locale_path)
gettext.textdomain(I18N_DOMAIN)
_ = gettext.gettext


class RpmType(object):
    """返回rpm包类型列表"""
    bug = "bugfix"
    sec = "security"
    enhanc = "enhancement"

    i18n_type_dict = {
        bug: _("bugfix"),
        sec: _("security"),
        enhanc: _("enhancement"),
    }

    @classmethod
    def get_sec_pkgs_list(cls, query):
        return list(query.filter(advisory_type__eq=cls.sec))

    @classmethod
    def get_bug_pkgs_list(cls, query):
        return list(query.filter(advisory_type__eq=cls.bug))

    @classmethod
    def get_enhanc_pkgs_list(cls, query):
        return list(query.filter(advisory_type__eq=cls.enhanc))


class UtBase(dnf.Base):
    """This is the base class for ut."""

    def __init__(self, conf=None):
        super(UtBase, self).__init__(conf=conf)

        self.setup()

    def setup(self):
        try:
            # 读取私有变量
            self.conf.substitutions.update_from_etc('/')
            # 读取所有repo
            self.read_all_repos()
            # 读取repo的详细信息
            repos = self.repos
            for repo in repos.iter_enabled():
                repo.load_metadata_other = True
            # 设置打印窗口
            self.output = Output
            # 设置事务展示窗口
            self.display = [CliTransactionDisplay()]
            # 更新源metadata
            self.fill_sack(load_system_repo=True, load_available_repos=True)
            # 查询源信息
            self.query = self.sack.query()
        except Exception as e:
            logging.warning("connetct repo error")
            logging.warning(e)

    def get_available_update_pkgs(self):
        # 获取可更新的软件包
        logging.debug("get update pkg's list")
        self.available_update_pkgs = self.query.available().upgrades()
        return self.available_update_pkgs

    def get_latest_changelogs(self, package):
        """Return list of changelogs for package newer then installed version"""
        newest = None
        for mi in self._rpmconn.readonly_ts.dbMatch('name', package.name):
            changelogtimes = mi[rpm.RPMTAG_CHANGELOGTIME]
            if changelogtimes:
                newest = datetime.date.fromtimestamp(changelogtimes[0])
                break
        chlogs = [chlog for chlog in package.changelogs
                  if newest is None or chlog['timestamp'] > newest]
        return chlogs

    def check_pkgs_update_type(self, package):
        pkg_type = []
        # 使用dnf自带接口判断软件包类型
        pkgs_sec = RpmType.get_sec_pkgs_list(self.available_update_pkgs)
        pkgs_bug = RpmType.get_bug_pkgs_list(self.available_update_pkgs)
        pkgs_enhanc = RpmType.get_enhanc_pkgs_list(self.available_update_pkgs)
        if package in pkgs_sec:
            # 包类型添加安全
            pkg_type.append(RpmType.sec)
        if package in pkgs_bug:
            # 包类型添加bugfix
            pkg_type.append(RpmType.bug)
        if package in pkgs_enhanc:
            # 包类型添加性能提升
            pkg_type.append(RpmType.enhanc)

        # 解析 changelog 判断软件包更新类型
        cve_regex = re.compile(r"cve-\d{4}-\d{4,7}", re.I)
        if RpmType.sec not in pkg_type:
            latest_changelog = self.get_latest_changelogs(package)
            # 获取的changelog格式如下
            # [{'author': 'gaoxingwang <gaoxingwang@huawei.com> - 1.26.2-9',
            #   'text': "- Type:bugfix\n- ID:NA\n- SUG:NA\n- DESC:fix 'nmcli -f NAME,ACTIVE',active column display error",
            #   'timestamp': datetime.date(2021, 8, 4)},
            #  {'author': 'gaoxingwang <gaoxingwang@huawei.com> - 1.26.2-8',
            #   'text': '- Type:bugfix\n- ID:NA\n- SUG:NA\n- DESC:sync from upstream, fix wrongly considering ipv6.may-fail for ipv4',
            #    'timestamp': datetime.date(2021, 8, 3)}]
            for item in latest_changelog:
                if cve_regex.search(item["text"]):
                    pkg_type.append(RpmType.sec)
                    break
        return pkg_type

    def get_available_update_pkgs_details(self):
        # 获取可更新包的详细信息
        logging.debug("get update pkg's detail list")
        pkgs = self.get_available_update_pkgs()
        pkgs_detail = []
        for pkg in list(pkgs):
            if pkg.arch != "src":
                pkg_detail = {"name": pkg.name,
                              "release": pkg.release,
                              "version": pkg.version,
                              "arch": pkg.arch,
                              "downloadsize": pkg.downloadsize,
                              "downloadsize_human_readable": format_number(pkg.downloadsize),
                              "srpm": pkg.sourcerpm,
                              "repo": pkg.reponame,
                              "summary": pkg.summary,
                              "url": pkg.url,
                              "license": pkg.license,
                              "desc": pkg.description,
                              "changelogs": pkg.changelogs,
                              "last_changelogs": self.get_latest_changelogs(pkg),
                              "type": self.check_pkgs_update_type(pkg)}
                pkgs_detail.append(pkg_detail)
        return pkgs_detail

    def add_rpm_to_install_list(self, rpmpkgs):
        # 添加软件包列表到安装列表中
        logging.debug("add rpms to install_list")
        for pkg in self.get_available_update_pkgs():
            if pkg.name in rpmpkgs and pkg.arch != "src":
                self.package_install(pkg)

    def print_trans_info(self):
        # 打印要执行的事务
        output = self.output.list_transaction(self.transaction)
        print(output)
        logging.debug(output)

    def update_rpmpkgs(self, rpmpkgs):
        try:
            # 开始执行升级
            self.add_rpm_to_install_list(rpmpkgs)
            print("Resolving transaction...")
            self.resolve()
            print('Downloading packages')
            progress = dnf.cli.progress.MultiFileProgressMeter()
            updatepkgs = self.transaction.install_set
            self.download_packages(updatepkgs, progress)
            print("Installing")
            self.do_transaction(display=self.display)
        except Exception as e:
            print("Install error")
            print(e)
            exit(1)


def install():
    parse = argparse.ArgumentParser()
    parse.add_argument("-l", "--pkgs", help="rpm pkg list")
    args = parse.parse_args()
    rpmpkgs = args.pkgs.split(' ')
    with UtBase() as base:
        base.update_rpmpkgs(rpmpkgs)


if __name__ == '__main__':
    pass
