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

*****
Conda
*****

Or, using Conda (which I recommend):

.. code-block:: bash

    conda create --name poetic python=3.8
    conda install tensorflow
    conda install nltk
    conda install gensim
    pip install poetic-py

    python -c "import nltk; nltk.download('punkt')"

Note: I love Conda (and that is what I use on my development machine)! 
At this time, poetic is not yet hosted on conda or conda-forge. More works to 
make that happen are on the way.

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
