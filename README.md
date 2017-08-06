# tdm

[![AUR](https://img.shields.io/aur/version/console-tdm.svg)](https://aur.archlinux.org/packages/console-tdm)
[![GitHub release](https://img.shields.io/github/release/dopsi/console-tdm.svg)](https://github.com/dopsi/console-tdm/releases/latest)

The TDM display manager is a wrapper script for `startx`.

It has a helper script, called `tdmctl` to manage tdm sessions. Each tdm session
is a symlink to an executable script that will be called in place of the final
`exec` in `.xinitrc`.

There are two types of tdm sessions :

* `X`: this session is started within the `.xinitrc` file as part
of the `startx` call (use this for X window manager/desktop
environments)
* `extra`: this session is started in the shell (use this for wayland
sessions, tmux wrappers, etc...)

A tdm session can also be either active or inactive. An active tdm session
is present in the tdm session selection screen, while an inactive tdm session
is not shown. If the path is not an executable file, the tdm session is
always counted as inactive.

As shown below, TDM has both a text and dialog mode:

[![Text mode](https://static.dopsi.ch/console-tdm/console-tdm_screenshot_text.png)](https://static.dopsi.ch/console-tdm/console-tdm_screenshot_text.png)

[![Dialog mode](https://static.dopsi.ch/console-tdm/console-tdm_screenshot_dialog.png)](https://static.dopsi.ch/console-tdm/console-tdm_screenshot_dialog.png)

## Installation

Run `make install` from the source directory (you can optionally set
`DESTDIR` or `PREFIX`).

The dependencies are :

* *xinit*
* *dialog* (optional, for the curses interface)

## Usage

1. To install `tdm` for your local user, run

    tdmctl init
    tdmctl add <session name> <executable path> [X(default)/extra]

This will copy the tdm configuration directory to your home directory.

2. You must then edit your `.profile` (or `.bash_profile`, `.zprofile`, etc...)
file to call `tdm` as last command (this will launch tdm once you log into a
tty).

3. In your `.xinitrc` file, you must then replace the exec line with
`exec tdm --xstart`, which will start your X session (if you do not have a
`.xinitrc` file, create a new one with this line in it).

See also the [ArchWiki page](https://wiki.archlinux.org/index.php/Console_TDM).

### Return value

If no session was executed, returns 1. Otherwise 0.

### Scripts

There are two scripts in the TDM configuration directory (`$HOME/.tdm`)
that are run at the begin and end of `tdm`.

* `tdminit` is run prior to the selection screen (when `tdm` is called
without `--xstart`)
* `tdmexit` executed right before the `startx` command is called (in the
`tdm --xstart` run)

### `tdmctl` commands

Initialize the config directory

    tdmctl init

List available (active) sessions

    tdmctl list: list available sessions  (X and extra)

List cached (inactive) sessions

    tdmctl cache

See which command is called by the session

    tdmctl check <session>
    tdmctl check extra/<session>

Show or set default session

    tdmctl default [session]

Add a session (it is immediately active)

    tdmctl add <name> <path> [X(default)/extra]

Remove session

    tdmctl remove <session>

Enable or disable session

    tdmctl enable/disable <session>: enable/disable session

Versioning
-----------

This project follows the semantic versioning guidelines provided at
[semver.org](http://semver.org/) with versions numbered as `MAJOR.MINOR.
REVISION` :

* `MAJOR` is increased after a backwards incompatible API change.
* `MINOR` is increased after a backwards compatible API change.
* `REVISION` is increased after a change with no effect on the API.

Any version with `MAJOR` being 0 *should* not be considered stable nor
should its API.

Versions history can be found in the file ChangeLog.md

License
-------

> This file is part of tdm.
>
> tdm is free software: you can redistribute it and/or modify
> it under the terms of the GNU General Public License as published by
> the Free Software Foundation, either version 3 of the License, or
> (at your option) any later version.
>
> tdm is distributed in the hope that it will be useful,
> but WITHOUT ANY WARRANTY; without even the implied warranty of
> MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
> GNU General Public License for more details.
>
> You should have received a copy of the GNU General Public License
> along with tdm.  If not, see <http://www.gnu.org/licenses/>.

Authors
=======

Currently maintained by dopsi.

This is a fork of the TDM display manager program by *mytbk*.
The original source can be found at
[here](https://github.com/mytbk/console-tdm).

Contributors:
* Helvethor
