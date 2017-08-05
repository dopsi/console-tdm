# Change Log

All notable changes to this project will be documented in this file.
This project adheres to [Semantic Versioning](http://semver.org/).

## [v1.2.1] 2017-03-28

### Changed

* tdm: revert the user getting logged out
* tdm: return non-zero if no session was executed


## [v1.2.0] 2017-03-25

### Changed

* tdm: change X process detection method
* tdmctl: check extra sessions
* tdmctl: more explicit error messages if the command is not found
* tdmctl: handle no default installations
* tdm: actually log the user out

## [v1.1.2] 2017-02-24

### Changed

* Makefile: use DESTDIR (thanks @hartwork)
* README.md: add installation and usage

## [v1.1.1] 2016-08-04

### Changed

* tdmctl: set PREFIX to /usr/local (to be consistent with Makefile)
* Makefile (bin): set the prefix in tdmctl to the same value as in Makefile

## [v1.1.0] 2016-02-17

### New features

* tdmctl (verify): add verification function to check for directory structure integrity
* tdmctl: add the remove command and update the usage message
* Makefile (doc): add new target to install documentation
* tdm.1: add manpage

### Changed

* Makefile (scripts): add the extra directory to the default configuration
* tdmctl (main script): add verification
  (cache functionality): put extra session in correct directory and check for links
* links.sh (main script): force symlink replacement if already existing

## [v1.0.0] 2015-12-31

### Changed

* tdm (version number): changed to 1.0.0
