import logging
import dnf
import dnf.cli.progress
from dnf.cli.format import format_number
from dnf.cli.output import Output, CliTransactionDisplay


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
        return self.query.available().upgrades()

    def get_available_update_pkgs_details(self):
        # 获取可更新包的详细信息
        logging.debug("get update pkg's detail list")
        pkgs = self.get_available_update_pkgs()
        pkgs_detail = []
        for pkg in pkgs:
            pkg_detail = {}
            # <class 'dnf.package.Package'>
            pkg_detail["name"] = pkg.name
            pkg_detail["release"] = pkg.release
            pkg_detail["version"] = pkg.version
            pkg_detail["arch"] = pkg.arch
            pkg_detail["downloadsize"] = pkg.downloadsize
            pkg_detail["downloadsize_human_readable"] = format_number(pkg.downloadsize)
            pkg_detail["srpm"] = pkg.sourcerpm
            pkg_detail["repo"] = pkg.reponame
            pkg_detail["summary"] = pkg.summary
            pkg_detail["url"] = pkg.url
            pkg_detail["license"] = pkg.license
            pkg_detail["desc"] = pkg.description
            pkgs_detail.append(pkg_detail)
        return pkgs_detail

    def add_rpm_to_install_list(self, rpmpkgs):
        # 添加软件包列表到安装列表中
        logging.debug("add rpms to install_list")
        for pkg in self.get_available_update_pkgs():
            if pkg.name in rpmpkgs:
                self.package_install(pkg)

    def print_trans_info(self):
        # 打印要执行的事务
        output=self.output.list_transaction(self.transaction)
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
