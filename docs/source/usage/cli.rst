=============================
Command Line Interface (CLI)
=============================

One of the most common usages of poetic is to make predictions using the command
line. A number of arguments are supported to allow some common operations, such as
making predictions from string or text file input, saving results to csv, and 
launching the GUI. This page details all the options and their usecases.

*************
Basic How-To
*************

To use ``poetic`` in the command-line mode, it is necessary to run the package
using python's ``-m`` argument to run ``__main__.py``. The simplest example without
any additional option will be the following, which launches the gui by default:

.. code-block:: bash
    
    python -m poetic

To use specific flags and options for poetic (instead of for python), append them
to the usual python call:

.. code-block:: bash
    
    python -m poetic -s "This is poetic"

For help, use the following command:

.. code-block:: bash
    
    python -m poetic --help

-------------------------------------------------------------------------

********************************
Platform and Python Interpreter
********************************

For documentation including all examples on this page, all shell commands assume 
the python interpreter can be invoked by ``python``. However, for platforms such 
as **linux**, specifying ``python3`` is often necessary to ensure that the correct 
python interpreter is used. 

For those who use virtual environment implementations, such as ``conda``, or  have 
multiple versions of python interpreters installed, make sure to activate the
virtual environment or invoke the correct python interpreter.


********************
Arguments and Flags
********************

+--------------------------+----------------------------+------------------------------------+
| Arguments                | Type                       | Functionality                      | 
+==========================+============================+====================================+
| ``-h`` or ``--help``     | Flag                       | Command-line help                  | 
+--------------------------+----------------------------+------------------------------------+
| ``-g`` or ``--GUI``      | Flag                       | Launch GUI (default option)        | 
+--------------------------+----------------------------+------------------------------------+
| ``-s`` or ``--Sentence`` | Argument: A string         | Sentence input for prediction      | 
+--------------------------+----------------------------+------------------------------------+
| ``-f`` or ``--File``     | Argument: Input file path  | Plain text file input              | 
+--------------------------+----------------------------+------------------------------------+
| ``-o`` or ``--Out``      | Argument: Output file path | Ouput results to a csv or txt file | 
+--------------------------+----------------------------+------------------------------------+
| ``--version``            | Flag                       | Package version                    | 
+--------------------------+----------------------------+------------------------------------+

-h
----

The ``-h`` and ``--help`` flags prints out a simple help guide for command-line arguments.
It is also invoked when unrecognized flags or arguments are used.


-g
----

The ``-g`` and ``--GUI`` flags launch the package's gui. this flag is intended to be used
in combination with ``-s`` or ``-f`` to override their default behabvior, which only processes
the given inputs and bypasses the GUI.

Launching the GUI is the default behavior of ``python -m poetic``, and in the cases when 
other arguments are not used, ``-g`` is unnecessary.


-s
----

The ``-s`` and ``--Sentence`` arguments accept a string to be predicted using the 
``Predictor`` class with default parameters. By default, the results will be printed 
to ``stdout``, and no GUI will be launched.

-f
----

The ``-f`` and ``--File`` arguments accept the path to a plain text file as a string. 
The contents of the file will be predicted using the ``Predictor`` with default parameters.
Like ``-s``, outputs will be directed to ``stdout`` by default and no GUI will be launched.

-o
----

The ``-o`` and ``--Out`` arguments accept the path as a string for ouputing the prediction
results. This option has to used in conjunction with ``-f`` or ``-s``, and it does not
affect the GUI and its processing, should the GUI is to be launched by ``-g``.

Plain text and CSV are supported and parsed according to the file extension, and
no strict file extension check will be enforced. However, to save a csv file, use only 
``.csv`` extension.

------------------------------------------------------------------------------------------

**********************
Argument Combinations
**********************

There are a few common configurations and options that are worth listing here separately.

Default
-------

This will lauch the GUI without any additional options (Note: the ``-g`` flag is
unnecessary here.)

.. code-block:: bash
    
    python -m poetic


Prediction with a String Input
-------------------------------

The ``-s`` argument tells the program to predict using the supplied string. A string can
have multiple sentences, which in turn will be tokenized internally.

Without any further arguments, all ouputs will be printed:

.. code-block:: bash
    
    python -m poetic -s "I love ice cream."

To save the results to a ``txt`` or ``csv`` file, use the ``-o`` argument with the
appropriate arguments: 

.. code-block:: bash

    # Save to txt (File extention not enforced)
    python -m poetic -s "I love ice cream." -o "<PATH>.txt"

    # Save to csv (File extention enforced)
    python -m poetic -s "I love ice cream." -o "<PATH>.csv"


Prediction with a File Input
-----------------------------

The ``-f`` argument accepts a file path to a plain text file, which will be sentence
tokenized and treated as strings. 

Operationally, ``-f`` is similarly to ``-s`` for file IO.

.. code-block:: bash
    
    python -m poetic -f "<LOAD_PATH>" 
    python -m poetic -f "<LOAD_PATH>" -o "<SAVE_PATH>"


File IO
--------

For file input, only plain text files are supported. File extension is not strictly
enforced, and all file types will be treated as plain text files.

For file output, both plain text and csv files are supported, and ``-o`` option 
determines the file type using extension. File extensive for csv file has to be
``.csv`` for correct parsing, but it does not matter for text files.

.txt File Format
~~~~~~~~~~~~~~~~

``-o`` will format all plain text output in the following way (Note: This can be
subject to change. For consistent results, use csv files instead).

.. code-block::

    Poetic
    Version: 1.0.2
    For latest updates: www.github.com/kevin931/Poetic

    Diagnostics Report

    Model: Lexical Model
    Number of Sentences: 2

    ~~~Five Number Summary~~~
    Minimum: 0.6363636363636364
    Mean: 0.6515151515151515
    Median: 0.6515151515151515
    Maximum: 0.6666666666666666
    Standard Deviation: 0.015151515151515138

    ~~~All Scores~~~
    Sentence #1: 0.6666666666666666
    Sentence #2: 0.6363636363636364


.csv File Format
-----------------

When a file path ending in ``.csv`` is encountered or the ``to_csv()`` method of the
``Diagnostics`` class is explicitly called, the results will be formatted with three
columns separated with ``Sentence_num``, ``Sentence``, and ``Score`` as keywords. Each
sentence and its prediction is in a new row, which is essentially the Tidy Data format
for optimal compatibility. The ``Sentence_num`` column can be treated as the index if
desired or necessary.

The raw csv file looks like the following:

.. code-block::

    Sentence_num,Sentence,Score
    1,Hi.,0.6666666666666666
    2,This is poetic.,0.6363636363636364

If formated to a table (like if opened in excel or the like), this will be the result:

+--------------+-----------------+--------------------+
| Sentence_num | Sentence        | Score              |
+==============+=================+====================+
| 1            | Hi.             | 0.6666666666666666 |
+ -------------+-----------------+--------------------+
| 2            | This is poetic. | 0.6363636363636364 |
+--------------+-----------------+--------------------+


Launch GUI
-----------

The GUI is a useful part of the program for a few purposes such as demo. Given that the
main function of the package is to make predictions, the program defaults to launching
the GUI when no other arguments are supplied. On the other hand, when argument ``-s`` or
``-f`` is supplied, the program assumes that it is used as for command-line purposed only,
and the GUI will not be launch.

To launch the GUI anyways, add the ``-g`` or ``--GUI`` flag to the existing command, which
will process everything else and then launch the GUI:

.. code-block:: bash

    python -m poetic -s "This is for prediction" -g


------------------------------------------------------------------------------------------

************************************
Unsupported Argument Configurations
************************************

Given the functionalities of all the options, certain options will conflict and cause
exceptions to be raised. All the incompatibilities are listed below. 

-s and -f
----------

``-s`` and ``-f`` cannot be used concurrently on the commandline because each call to
the ``Predictor`` supports only one type of input. Further, since results are printed
out to ``stdout`` by default, it does not make sense to print two separate batches of
results. Therefore, ``UnsupportedConfigError`` from the ``poetic.excptions`` module will 
be raised.

The ``Predictor`` supports sentence tokenization with a single string, and if multiple
inputs can be formed into a single string with mutiple sentences, this will be the best
approach. There is currently no support for command-line processing of mutiple separate
input. For this use case, a ``poetic`` needs to be imported as a package in python.


-o without -s or -f
---------------------

The ``-o`` argument by itself, even if a path is provided, will not have any effect on 
how the package is run. It has to be used with either ``-s`` or ``-f`` to save results 
of predictions made through the command line. ``-o`` does not change any global parameter
otherwise. If no other options are present, it will be ignored and the default GUI will 
be launched.


-s, -f, or -o without Arguments
--------------------------------

``-s``, ``-f``, and ``-o`` all expected one argument. If only the flags are used without
supplying the necessary argument, an error will occur and the program will terminate.