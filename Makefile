MKDIR=mkdir -p
CP=cp
PREFIX=/usr/local
SH=/bin/sh

all: none

none:
	@echo "Nothing to be done, run `make install` instead"

install: bin bashcomp zshcomp scripts

bin: tdm tdmctl
	$(MKDIR) $(PREFIX)/bin
	$(CP) $^ $(PREFIX)/bin

bashcomp: tdmctl.bashcomp
	$(MKDIR) $(PREFIX)/share/bash-completion/completions
	$(CP) $^ $(PREFIX)/share/bash-completion/completions/tdmctl

zshcomp: _tdmctl
	$(MKDIR) $(PREFIX)/share/zsh/site-functions
	$(CP) $^ $(PREFIX)/share/zsh/site-functions

scripts: tdmexit tdminit
	$(MKDIR) $(PREFIX)/share/tdm
	$(CP) $^ $(PREFIX)/share/tdm
	$(MKDIR) $(PREFIX)/share/tdm/sessions
	$(MKDIR) $(PREFIX)/share/tdm/extra
	$(SH) ./links.sh /usr/bin $(PREFIX)/share/tdm/sessions
