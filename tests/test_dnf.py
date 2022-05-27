import logging
import dnf.logging
from dnf.cli.format import format_number

logger = logging.getLogger('dnf')
logger.info('aa')
base = dnf.Base()
conf = base.conf
conf.substitutions.update_from_etc('/')

base.read_all_repos()
# base.load_metadata_other(True)
repos = base.repos
for repo in repos.iter_enabled():
    repo.load_metadata_other = True

def pkgs_filter( query, bugfix=False, enhancement=False, security=False, cmp_type="eq"):
    filters = []
    if bugfix:
        key = {'advisory_type__' + cmp_type: 'bugfix'}
        filters.append(query.filter(**key))
    if enhancement:
        key = {'advisory_type__' + cmp_type: 'enhancement'}
        filters.append(query.filter(**key))
    if security:
        key = {'advisory_type__' + cmp_type: 'security'}
        filters.append(query.filter(**key))
base.fill_sack(load_system_repo=True, load_available_repos=True)
query = base.sack.query()#.run()
a = query.available()
a=a.upgrades()

class RpmPkgsType(object):
    type_check="advisory_type__eq"
    bug="bugfix"
    sec="security"
    enhanc="enhancement"


bugfix_filter=pkgs_filter(a,bugfix=True)[0]
asggw="advisory_type__eq"
print(list(q))
if list(q)[0] in list(a):
    print("OK")
else:
    print("False")

# print()
print("Available dnf packages:")
# print(bas)
print(a)
for pkg in a:  # a only gets evaluated here
    print(pkg)
    print(type(pkg))
    print(pkg.name+"-"+pkg.release+"-"+pkg.version+"-"+pkg.arch)
    print(format_number(pkg.downloadsize))
    print(pkg.enhances)
    print(pkg.changelogs)
    print(type(pkg))
base.close()
