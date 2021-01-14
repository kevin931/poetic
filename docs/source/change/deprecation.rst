===============
Deprecations
===============

As documented in **Development and Supoport** section of the documentation, all
deprecations will be clearly noted and warned. This page aggregates all current
deprecations that are not yet removed from the codebase, and it also provides more
details than the release notes. Support for these features will be removed in the 
next major release.

This list is organized by releases, which represent the time each feature is\
deprecated (not the time they are removed). 

--------------------

***********
v1.0.0
***********

*Launch.py*
-----------

``Launch.py`` is no longer supported starting in this version, and it is not
shipped with official releases on ``pip`` or ``conda``. However, it is still
tracked by git in the repository, and minimal maintenance updates will occur
to ensure that it stays functional. No new features will be supported.

All the functionalities are replaced by ``__main__.py``. To launch the program
from the command line, use ``python -m poetic`` intead. All the command-line
flags and arguments are still valid.