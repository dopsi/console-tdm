---
layout: post
title:  "Welcome to this website"
date:   2016-05-01 19:00:00 +0200
---

I am proud to announce this new site for the [console-tdm][console-tdm] project.
This website will be the new frontpage and central information place for this 
project.

I would like to highlight some of the major changes done since this repository
was created (I would also like to point out that I did not use the code from
{% include icon-github.html username="mytbk" %} / [console-tdm][base-repo] but 
the code provided by the ArchLinux User Repository package, which was hosted on
Google Code, and is now lost).

* The sessions can now be deleted (they could not, except manually)
* The manpage has been written, to have a consistent and clear documentation
in the Linux way
* `tdmctl` does now also list extra sessions
* Execution safety has been improved, with extra checks before the various 
scripts are executed

I am currently considering rewriting the program in Python 3.5, since it would
be clearer, safer and more flexible to use.

[console-tdm]: https://github.com/dopsi/console-tdm
[base-repo]: https://github.com/mytbk/console-tdm
