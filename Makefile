MKDIR=mkdir -p
CP=cp
DESTDIR=
PREFIX=/usr/local
SH=/bin/sh

all: none

none:
	@echo "Nothing to be done, run `make install` instead"

install: bin bashcomp zshcomp scripts doc

bin: tdm tdmctl
	$(MKDIR) $(DESTDIR)$(PREFIX)/bin
	$(CP) $^ $(DESTDIR)$(PREFIX)/bin
	sed -i -e "s_PREFIX=/usr/local_PREFIX=$(PREFIX)_" $(DESTDIR)$(PREFIX)/bin/tdmctl

bashcomp: tdmctl.bashcomp
	$(MKDIR) $(DESTDIR)$(PREFIX)/share/bash-completion/completions
	$(CP) $^ $(DESTDIR)$(PREFIX)/share/bash-completion/completions/tdmctl

zshcomp: _tdmctl
	$(MKDIR) $(DESTDIR)$(PREFIX)/share/zsh/site-functions
	$(CP) $^ $(DESTDIR)$(PREFIX)/share/zsh/site-functions

scripts: tdmexit tdminit
	$(MKDIR) $(DESTDIR)$(PREFIX)/share/tdm
	$(CP) $^ $(DESTDIR)$(PREFIX)/share/tdm
	$(MKDIR) $(DESTDIR)$(PREFIX)/share/tdm/sessions
	$(MKDIR) $(DESTDIR)$(PREFIX)/share/tdm/extra
	$(SH) ./links.sh /usr/bin $(DESTDIR)$(PREFIX)/share/tdm/sessions

doc: tdm.1
	$(MKDIR) $(DESTDIR)$(PREFIX)/share/man/man1
	$(CP) $^ $(DESTDIR)$(PREFIX)/share/man/man1
	ln -s $^ $(DESTDIR)$(PREFIX)/share/man/man1/tdmctl.1
