==================================
Prediction Results
==================================

As the final part of ``poetic``'s main workflow, the post-processing of prediction results
consists of diagnostics, summary, and file output. The package's ``Diagnostics`` class
provides all these functionalities with a few simple methods, which are documented below.

--------------------------------------------------------------

********************
*Predictions* Class
********************

Both ``predict()`` and ``predict_file()`` methods of the ``Predictor`` class returns an
instance of the ``Predictions`` class:

.. code-block:: python

    import poetic

    pred = poetic.Predictor()
    score = pred.predict("Is this poetic?")

In the example above, the ``score`` object will be a ``Predictions`` object, which can
then call methods to run diagnostics and save results.


Inheritance
------------

The ``Predictions`` class inherits from the ``Diagnostics`` class, and all methods are also
inherited with the only difference in the constructor. The advantage of using an inherited 
class instead of using the ``Diagnostics`` class directly is that the preprocessing of keras 
predictions can occur separately. Thus, the ``Predictions`` class serves as an internal 
interface to distinguish from manually instantiated instances of the ``Diagnostics`` class. 

To use the toolchain and methods separately, use the ``Diagnostics`` class instead. All 
methods of the ``Predictons`` will be documented with the ``Diagnostics`` class unless
they are overridden.

--------------------------------------------------------------

********************
*Diagnostics* Class
********************

As the base class for ``Predictions``, the ``Diagnostics`` class provides a more genralized
framework for working with any prediction results. In the future, more abstractions may be 
added to allow for more versatility to use independently.

A typical workflow will involve making predictions, running diagnostics, and saving the 
results to a file:

.. code-block:: python

    import poetic

    pred = poetic.Predictor()
    score = pred.predict("Is this poetic?")
    score.run_diagnostics()

    print(score.generate_report())
    score.to_file(path="<PATH>")

Instantiation
--------------

To use the ``Diagnostics`` class, only the ``predictions`` argument is required as a list
of floats:

.. code-block:: python

    import poetic

    results = poetic.Diagnostics(predictions = [1, 0, 0.5])

    # OR: with sentences
    sentences = ["Hi.", "I am poetic", "How about you?"]
    results_sentences = poetic.Diagnostics(predictions = [1, 0, 0.5], sentences=sentences)

The ``sentences`` argument is optional. If used, it will store the corresponding sentences of
the predictions as a class attribute; otherwise, it will be ``None``, and all other methods 
are largely unaffected, except the contents of the outputs.

Diagnostic Statistics
-----------------------

As of now, the ``Diagnostics`` class supports five-number summary for predictions. As part of
the workflow, it is automatically called by the ``run_diagnostics()`` method, and the results
are stored in the ``diagnostics`` attribute of the object. As an example:

.. code-block:: python

    import poetic

    results = poetic.Diagnostics(predictions = [1, 0, 0.5])
    results.run_diagnostics()
    # Get the diagnostic results
    print(results.diagnostics)

The ``diagnostics`` attribute is a dictionary with three keywords: "Sentence_count",
"Five_num", and "Predictions". The corresponding values are the following:

    - "Sentence_count": An ``int`` of the length of entries.
    - "Five_num": Five number summary stored with a dictionary.
    - "Predictions": A ``list`` of floats from the ``predictions`` attribute. 

To obtain the five number summary separately using the classmethod ``five_number()``,
which is essentially a utility function that can be use for any array-like objects 
compatible with ``numpy``:

.. code-block:: python

    import poetic

    results = poetic.Diagnostics(predictions = [1, 0, 0.5])
    poetic.Diagnostic.five_number(results.predictions)

    # As a stand-alone method:
    poetic.Diagnostic.five_number([1, 0, 0.5])


Diagnostic Report
------------------

A diagnostic report is a string (or plain text) summary of the object with diagnostic
statistics. To obtain the diagnostic report, the ``run_diagnostics()`` method has to be
called previously on the object. Otherwise, a type error will be raised because the
"diagnostics" attribute will be ``None``.

An example usgae of the method is this:

.. code-block:: python

    import poetic

    results = poetic.Diagnostics(predictions = [1, 0, 0.5])
    results.run_diagnostics()
    print(results.generate_diagnostics())

The contents of the report will be identical to the text file output as documented below.

File Output 
------------

The results and diagnostics can be saved to either ``.txt`` or ``.csv`` file. The former
writes the diagnostics report to a plain text while the latter saves the actual values
separated by comma. The usage is essentially identical to using the ``-o`` option on the 
command line. 

Plain Text File
~~~~~~~~~~~~~~~~~

To save results to a text file:

.. code-block:: python

    import poetic

    results = poetic.Diagnostics(predictions = [2/3, 7/11])
    results.run_diagnostics()
    results.to_file("<PATH>")

The output format is the following:

.. code-block:: text

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

The ``to_file()`` does not enforce file extension for text files, except for ``.csv``
ending. In the latter case, it will automatically call the ``to_csv()`` method. The 
text file output is more for a quick summary than a way to store data, and the format can
potentially change with updates. If an object needs to be restored or data will be further
processed, use the csv format instead. 


.csv File Format
~~~~~~~~~~~~~~~~~

When a file path ending in ``.csv`` is encountered or the ``to_csv()`` method of the
``Diagnostics`` class is explicitly called, the results will be formatted with three
columns separated with ``Sentence_num``, ``Sentence``, and ``Score`` as keywords in
the first row. Each sentence and its prediction is in a new row, which follows the 
Tidy Data format for optimal compatibility. The ``Sentence_num`` column can be treated
as the index.

To save to a csv file as an example:

.. code-block:: python

    import poetic

    results = poetic.Diagnostics(predictions = [2/3, 7/11])
    results.run_diagnostics()
    results.to_csv("<PATH>")

Or, let ``to_file()`` handle it automatically: 

.. code-block:: python

    import poetic

    results = poetic.Diagnostics(predictions = [2/3, 7/11])
    results.run_diagnostics()
    results.to_file("<PATH>.csv")

The raw csv file looks like the following:

.. code-block:: text

    Sentence_num,Sentence,Score
    1,Hi.,0.6666666666666666
    2,This is poetic.,0.6363636363636364

If formated to a table (like if opened in excel or the like), this will be the result:

+--------------+-----------------+--------------------+
| Sentence_num | Sentence        | Score              |
+==============+=================+====================+
| 1            | Hi.             | 0.6666666666666666 |
+--------------+-----------------+--------------------+
| 2            | This is poetic. | 0.6363636363636364 |
+--------------+-----------------+--------------------+


Custom Build-in (Magic) Methods
--------------------------------

String Representation
~~~~~~~~~~~~~~~~~~~~~

The ``str()`` method will return a short summary of the object. It will truncate the output
to 14 characters after the description:

.. code-block:: text

    'Diagnostics object for the following predictions: [0.66666666666...'



The ``repr()`` method will return a dictionary cast into a string with all the predictions,
sentences, and the ``diagnostics`` attributes. It does not truncate any results. This will
be more appropraite for a full representation of the object. It will have the following format:

.. code-block:: text

    "{'Predictions': [0.6666666666666666, 0.6363636363636364], 'Sentences': None, 'Diagnostics': None}"

*len()*
~~~~~~~~~

The ``len()`` method returns the length of the ``predictions`` attribute of the object, 
which is the number of entries in the predictions list. Since the length of ``predictions``
and ``sentences`` are intended to match, the returned length logically represents the
length of the object.


Comparison Operators
~~~~~~~~~~~~~~~~~~~~~~

The ``Diagnostics`` class currently supports the following four operators: ``>``, ``>=``, ``<``, 
and ``<=``. They compare the **mean** values of the ``predictions`` attribute of the compared
onjects. 

When the distribution of the predictions are not normally distributed, such as skewed, the mean
values may not be meaningful. In these cases, manual comparions are necessary. 

Given that the predictions attribute is a list of ``float``, the ``==`` and ``!=`` operators
are currently not implemented.