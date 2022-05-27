PO_INSTALL = /usr/bin/install -c
PO_INSTALL_DATA = $(PO_INSTALL) -m 644
PO_INSTALL_DIR  = /usr/bin/install -d
PO_INSTALL_NLS_DIR = $(DESTDIR)$(DATADIR)/locale
PO_MSGFMT = msgfmt
PO_POFILES = zh_CN.po

po-all:
	$(PO_MSGFMT) -o  po/$(PKGNAME).mo po/$(PO_POFILES)


po-clean:
	@rm -fv po/*.mo

po-install: $(PO_MOFILES)
	$(PO_INSTALL_DIR) $(PO_INSTALL_NLS_DIR)/zh_CN/LC_MESSAGES
	$(PO_INSTALL_DATA) po/$(PKGNAME).mo $(PO_INSTALL_NLS_DIR)/zh_CN/LC_MESSAGES/$(PKGNAME).mo



