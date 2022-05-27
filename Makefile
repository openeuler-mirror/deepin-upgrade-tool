.PHONY: translate

all: translate
PREFIX = /usr/share/locale/zh_CN/LC_MESSAGES
translate:
	mkdir -p $(PREFIX)
	msgfmt -o $(PREFIX)/utreponoity.mo utrepoinfo/po/utreponoity.po

clean:
	true
