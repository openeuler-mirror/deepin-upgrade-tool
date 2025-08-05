PKGNAME = com_deepin_upgrade
RPMNAME = com.deepin.upgrade
PREFIX = /usr
DATADIR = ${PREFIX}/share
RPMBUILDDIR = $(HOME)/rpmbuild
DISTDIR = dist
SPECFILE = com.deepin.upgrade.spec
RPMVERSION = $(shell cat VERSION)

include po.mk

all: po-all

install:  all po-install

clean: po-clean
	@rm -fv *.mo


# Setup RPM build environment
.PHONY: setup-rpm
setup-rpm:
	@echo "Setting up RPM build environment..."
	@mkdir -p $(RPMBUILDDIR)/{BUILD,RPMS,SOURCES,SPECS,SRPMS}
	@mkdir -p $(RPMBUILDDIR)/RPMS/$(ARCH)
	@echo "RPM build directories created in $(RPMBUILDDIR)"

# Create source tarball
.PHONY: tarball
tarball: setup-rpm
	@echo "Creating source tarball..."
	@mkdir -p $(DISTDIR)
	@tar --exclude='.git' --exclude='$(BUILDDIR)' --exclude='$(DISTDIR)' \
		--exclude='*.pyc' --exclude='__pycache__' --exclude='*.egg-info' \
		--exclude='*.mo' --exclude='*.rpm' --exclude='*.src.rpm' \
		-czf $(RPMBUILDDIR)/SOURCES/$(RPMNAME)-$(RPMVERSION).tar.gz \
		--transform="s,^,$(RPMNAME)-$(RPMVERSION)/," .

# Build source RPM package
.PHONY: srpm
srpm: tarball
	@echo "Building source RPM package..."
	@rm -rf $(DISTDIR)/*
	@rpmbuild -bs $(SPECFILE) \
		--define "_topdir $(RPMBUILDDIR)" 
	@echo "Source RPM package built: "
	@cp $(RPMBUILDDIR)/SRPMS/$(SRPM_PACKAGE)/com.deepin.upgrade*  $(DISTDIR)
	@ls -l $(DISTDIR)