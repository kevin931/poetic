==================================
Package Information and Resources
==================================

There are many ways to get more information on ``poetic``, including official documentation,
Github repository, docstrings, and built-in package information. This guide details some of
these resources and how they can be best utilized.

--------------------------------------------------------------

******************
GitHub Repository
******************

The `GitHub repository <https://github.com/kevin931/poetic>`_ is where all the development
and latest changes take place, and it is perhaps the best quickstart guide for those who
have stumbled upon it.

The default branch is "dev", which is often ahead of the stable release branches, and can be
unstable or broken at times. To view the latest stable release codes, use the 
`main <https://github.com/kevin931/poetic/tree/main>`_ branch. All branches with the name
"maintenance/" are for patches and bug fixes for previous releases, such as v1.0.x.

Be sure to also check out our `Issue Tracker <https://github.com/kevin931/poetic/issues>`_ 
and our new `Discussion Page <https://github.com/kevin931/poetic/discussions>`_ to get involved,
report issues, request features, or to contribute.

--------------------------------------------------------------

******************
Documentation
******************

**Ta-da!!!** You are already reading the official documentation. Congratulations!

The default link `poetic.readthedocs.io <https://poetic.readthedocs.io/en/latest/>`_ links to the 
latest stable release of ``poetic``, which corresponds to the ``main`` branch on GitHub. To view
specific versions of the documentation, select the corrresponding versions at the bottom left
corner of the page (in green text).

Only the latest patch of each minor release will be viewable on our documentation page: for
example, when v1.0.2 is out, its documentation page will replace that of v.1.0.1. All
actively supported versions will have its documentation page active until they have reached
EOL.


--------------------------------------------------------------

******************
CLI Help
******************

When using ``poetic`` on through the command-line interface (CLI), there are two options to
get help and package versions. For more detailed decumentation on CLI, please see the "**Command 
Line Interface (CLI)**" section of the documentation.

To get help on the command-line arguments and flags, use the
``--help`` flag:

.. code-block:: bash

    python -m poetic --help


The outputs of the ``--help`` flag are:

.. code-block:: text

    Poetry Predictor Command Line Mode

    optional arguments:
    -h, --help            show this help message and exit
    -g, --GUI             Flag to launch GUI. No input needed.
    -s SENTENCE, --Sentence SENTENCE
                            A string to be parsed.
    -f FILE, --File FILE  Plain text file to be parsed.
    -o OUT, --Out OUT     Path to save results (txt or csv).
    --version             show program's version number and exit

To get the version of the package:

.. code-block:: bash

    python -m poetic --version


--------------------------------------------------------------

******************
*Info* Class
******************

Within the package, the ``Info`` class provides the basic information of the package, which
is useful for obtaining the version and build status. This has to be used within python.

Version
--------

To get the version: 

.. code-block:: python

    import poetic

    poetic.util.Info.version()


Build status
-------------

To get the build status: 

.. code-block:: python

    import poetic

    poetic.util.Info.build_status()

All official, stable releases will have a build status of "Stable".


Instantiation
--------------

The ``Info`` class is a singleton mainly for internal purposes to store metadata for testing. 
The ``version()`` and ``build_status()`` methods are classmethods, which do not need to be
instantiated. However, if an instance is needed, use the following method:

.. code-block:: python

    import poetic

    info_instance = poetic.util.Info.get_instance()

Directly calling the constructor through ``Info()`` can potentially result in a ``SingletonError``
if a previous instance already exists. The ``get_instance()`` methods returns the existing
instance or instantiates the first instance.

--------------------------------------------------------------

******************
Docstrings
******************

All public modules, classes, methods, and specifically defined magic methods have a docstring. 
It serves as the lowest level documentation for ``poetic``. There are two ways of accessing 
each docstring:

.. code-block:: python

    import poetic

    # Docstring for the Predictor class
    help(poetic.Predictor)

    # OR:
    print(poetic.Predictor.__doc__)

All docstrings are also formated in the "**Full Documentation**" section of documentation.


*****************
Type Annotation
*****************

All functions and methods are type annotated. Although typing, along with dependencies, limit
backwards compatibility of ``poetic``, this will help with maintainability for developer and 
ease of use for end users. 

Variables and attributes are not yet type annotated. This may be a feature to be considered in
the future, when python 3.5 will no longer be supported.