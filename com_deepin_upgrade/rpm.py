import rpm


def get_local_rpmpkgs():
    """
    获取本地已安装的rpm包，类似rpm -qa
    :return:
    """
    local_rpmpkgs = {}
    rpmts = rpm.TransactionSet()
    for h in rpmts.dbMatch():
        local_rpmpkgs[h.name] = "{version}-{release}".format(version=h.version, release=h.release)
    return local_rpmpkgs
