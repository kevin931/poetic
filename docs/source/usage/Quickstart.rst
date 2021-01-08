====================
Quickstart Reference
====================

Welcome to Poetic (poetic-py on PyPi). Please see below for installation details. 

***********************
Set Up/Assets Download
***********************

First-time Set Up (Default Behavior)
-------------------------------------

All machine learning models are not shipped with the package because of their size (~1GB).
However, poetic provides a utility to download them upon first use. 

When the models are needed, the package will call the ``poetic.util.Initializer.check_assets()``
method to check for assets and if assets are missing, it then subsequently calls the 
``poetic.util.Initializer.download_assets()`` method which will prompt a command-line input: 

.. code-block:: bash

    The following important assets are missing:

    Downloading from: https://github.com/kevin931/poetic-models/releases/download/v0.1-alpha/sent_model.zip
    Download size: 835MB.


    Would you like to download? [y/n]

This behavior is intended to take bandwidth and user consent into consideration.


Download without Asking
-----------------------

If there is a use case in which command line input is undesirable or inefficient
(or if you just don't want to), include the following commands to download them:

.. code-block:: python

    import poetic
    assets =  poetic.util.Initializer.check_assets()
    poetic.util.Initializer.download_assets(assets_status=assets, force_download=True)


********************
Command-line Mode
********************

Launch GUI
------------

.. code-block:: bash

    python -m poetic 


Prediction with Sentence Input
------------------------------------

.. code-block:: bash

    python -m poetic -s "I am poetic."


Prediction with Plain Text File Input
---------------------------------------

.. code-block:: bash

    python -m poetic -f <PATH_TO_FILE>


Save Results to File
----------------------

.. code-block:: bash

    python -m poetic -f <PATH_TO_FILE> -o <PATH_TO_TXT>
    python -m poetic -f <PATH_TO_FILE> -o <PATH_TO_CSV>
    python -m poetic -s "I am poetic. Are you?" -o <PATH_TO_TXT>



****************
Use in Python
****************

Import Behavior
----------------------

Directly exposed classes:
    * Predictor
    * Diagnostics 

Utility module:
    * util


Make a Simple Prediction
-------------------------

.. code-block:: python

    import poetic

    new_pred = poetic.Predictor()
    sentence_result = new_pred.predict("I am poetic. Are you?") # Directly
    file_result = new_pred.predict_file("FILE_PATH.txt") # From a file


Prediction Diagnostics
-------------------------

.. code-block:: python

    # sentence_result is from the previous section.
    sentence_result.run_diagnostics()
    sentence_result.to_file("SAVE_PATH.txt")
    sentence_result.to_csv("SAVE_PATH.csv")
