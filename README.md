tdm
===

**This project is now on standby**. Only version 1 is supported at the
moment.

This was a fork of the TDM display manager program by *mytbk*.
The original source can be found at 
[here](https://github.com/mytbk/console-tdm).

See [Port to Python](#port-to-python) for more information about
version 2 of tdm.

Port to Python
--------------

Shell script is known for its vulnerabilities and few security systems.
This is why I decided it would be best for this program to be ported to 
Python 3, which is a robust language, well fitted for this kind of tasks.

Version 2 is able to handle all operations done in version 1 (the command
line program remain the same and take the same arguments).

There are no dependencies, except for the Python library. To have the 
dialog interface, the `pythondialog` module is required.

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

Original code by mytbk. Currently maintained by dopsi.
