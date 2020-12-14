===================
Installation Guide
===================

Welcome to Poetic (poetic-py on Pypi). Please see below for installation details. 

****
Pip
****

System-wide installation:

.. code-block:: bash

    pip install poetic-py
    python -c "import nltk; nltk.download('punkt')"

The usage of virtualenv is also recommended over system-wide installation.

********************
Conda (Recommended)
********************

Or, using Conda (which I recommend):

.. code-block:: bash

    conda install -c kevin931 poetic-py
    python -c "import nltk; nltk.download('punkt')"

A few notes on Conda:

If you need documentation on how to get this conda working/set up, 
`this is a good guide. <https://docs.conda.io/projects/conda/en/latest/user-guide/getting-started.html>`_

There is a potential bug with tensorflow on Conda for Windows because of maximum path length 
limitation. If you are unable to install tensorflow from conda, please open 
`an issue <https://github.com/kevin931/poetic/issues>`_ or refer
to tensorflow's github Issue Tracker for support. For reference, you can also refer to
`Microsoft's guide <https://docs.microsoft.com/en-us/windows/win32/fileio/maximum-file-path-limitation>`_
. (Caution: Editing registry can potentially have consequences. Please proceed with caution and
be sure to know the issue.) 

**************************
Supported Package Versions
**************************

Python
------
* 3.6
* 3.7
* 3.8 

Note: Newer versions depend on dependencies. 

Dependencies
-------------
* tensorflow >= 2
* nltk >= 3.4
* gensim >= 3.8


**************************
Troubleshooting
**************************

Pip Dependency Issues
----------------------

If dependencies become an issue, try installing them separately from poetic:

.. code-block:: bash

    pip install tensorflow
    pip install gensim
    pip install nltk
    
    pip install poetic-py --no-deps 
    python -c "import nltk; nltk.download('punkt')"


If this does not solve the problem or there is any other unforeseeable problems, please head
to our `Issue Tracker <https://github.com/kevin931/poetic/issues>`_ and hopefully I can help you
out!


Pip Caching
------------
Pip, by default, caches downloads, which may result in downloading previously installed versions and
leading to failure to upgrade. To address this, use the flag:

.. code-block:: bash

    pip install --no-cache-dir poetic-py