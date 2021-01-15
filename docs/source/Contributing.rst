Contribution Guideline
=======================

Bug Reporting/Fixes
--------------------

I get it! I (or the team in the future) make mistakes. If something does not work
as intended or if there are any other bugs, please do let us know! 

     1. Check poetic's Github `issue tracker <https://github.com/kevin931/poetic/issues>`_
     2. If there is already the same issue, feel free to comment or help out! 
     3. If not, please open an issue with as much details as possible.
     4. Information to include (Do use a template if that works for you):

        * Platform
        * OS
        * Package/Dependency versions (exporting the environment through pip or conda will be best)
        * Codes to reproduce the error


Pull Requests
--------------

Any and all help and contrition are welcomed. For consistency and stability, there are a few
quick, easy guidelines to follow if you would like to contribute:

* What to contribute: 
    * Refer to our Issue Tracker and dev branch for the latest updates and developments. 
    * If there is something not already covered, open an issue; otherwise, feel free to comment.
    * Take a look at the `roadmap <https://poetic.readthedocs.io/en/latest/Development.html>`_. 

* For all changes and source codes:
    * All functions and methods must be type annotated with ``typing``.
    * Unittests must be written to ensure new codes work. Existing tests must pass or modified to pass if relevant. Pytest is used for this package.
    * All public methods, functions, and modules must have a `Google-styled docstring <https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html>`_. If an interface is modified, docstring must relfect the change accordingly.
    * Comments are fine and sometimes necesary when codes are obscure, but obvious comments should be avoided. Use of expressive variable names are encouraged.
    * Commits must have a simple, meaningful title (e.g. 'Added support for csv files'. Not: 'Quick update').
    * *Breaking changes* and *deprecations* should be implemented with **extreme caution**. Backwards compatibility should be maintained with a deprecation notice unless absolutely impossible.
    * Additional dependencies should be added with caution since it can have remification for end-users.

* Documentation changes:
    * For all changes to the public interface, add such changes to the development changelog at "docs/source/change/development.rst".
        * All new features will go into the next minor release.
        * Most internal changes, bug fixes, and documentation updates will be included in patches.
        * If you're not sure how the change will be integrated into releases, mention this in the message in PR or issue.
    * Updating documentation in general is not mandatory but very much welcomed. Make sure style is consistent.


Feature Request
----------------

If there is something that you think will make this better, please let us know!

    1. Look through the Issue Tracker and, if appropriate, submit an issue for suggestion (There is a template to follow as well!). 
    2. If the feature deviates from the roadmap significantly, it will not be implemented. Otherwise, it will be considered based on the following factors:

        * Feature relevance
        * Current project development and timeline
        * Implementation logistics/complexity
        * External dependencies (if any)

    3. If you yourself would like to implement the feature, say so in the Issue, and I will evaluate it accordingly. 
    4. Bottomline: it doesn't hurt to ask and I'm pretty openminded.