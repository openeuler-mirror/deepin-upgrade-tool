PKGNAME = com_deepin_upgrade
PREFIX = /usr
DATADIR = ${PREFIX}/share


include po.mk

all: po-all

install:  all po-install

clean: po-clean
	@rm -fv *.mo


