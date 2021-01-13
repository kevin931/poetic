==================================
Making Predictions
==================================

The most important functionality of ``poetic`` is the interface to make predictions using
pretrained keras models. The ``Predictor`` class provides a simple-to-use, one-stop solution
to predict how poetic any given input is and how much it resembles 18th- and 19th-century
poetry if the default models are used.

This page documents the usage of the ``Predictor`` class along with common topics and examples.

--------------------------------------------------------------

******************
Initialization
******************

The ``Predictor`` class requires instantiation to work properly since there are no utility
functions or class methods in this class. To create an instance, simply use ``poetic.Predictor()``
becasue it is a package-level class: 

.. code-block:: python

    import poetic

    pred = poetic.Predictor()

In this example, all default parameters are used, and the default lexical model and dictionary
will be loaded. There is **not yet** official support for custom model and dictionary. However,
``Predictor`` does accept previously loaded assets using either keras and gensim's API or poetic's
``Initializer`` class:

.. code-block:: python

    import poetic

    model = poetic.util.Initializer.load_model()
    dictionary = poetic.util.Initializer.load_dict()
    pred = poetic.Predictor(model=model, dict=dictionary)

If the default models have not been downloaded from its GitHub repo, there is an option to
override the user input prompt: 

.. code-block:: python

    import poetic

    pred = poetic.Predictor(force_download_assets=True)

Once a ``Predictor`` object is instantiated, it can be reused to make multiple predictions and to
preprocess different inputs. No method will have meaningful side effects, although the ``tokenize()``
method modifies the internal ``_sentences``, which temporarily stores the tokenized input and 
will be overridden with each subsequent operation. Therefore, a ``Predictor`` instance is fully 
reuable and safe.

--------------------------------------------------------------

*******************
Making Predictions
*******************

The ``Predictor`` allows users to make poetic predictons using either the ``predict()`` or the
``predict_file()`` method. All preprocessing steps are automatically handled without any need
to manually clean inputs.

Prediction with Strings
-------------------------

To predict a string, use the ``predict()`` method of the ``Predictor`` instance. The input
string can consist of multiple sentences, which are then tokenized by preprocessor. The **longest**
supported sentence (after sentence tokenization) is **456 tokens**, including words and 
punctuations. 

As an example of string prediction:

.. code-block:: python

    import poetic

    pred = poetic.Predictor()
    result = pred.predict("Hi. I am poetic. Are you?")

The ``predict()`` method will return a ``Predictions`` object, which in turn supports post-
processing, such as running diagnostics and saving results to file. 

Prediction with Text Files
----------------------------

Plain text files are also supported. To load and predict a file, use the ``predict_file()``
method, and all preprocessing and the object returned will function exactly the same as the
``predict()`` method. 

Under the hood, it loads the file into a single string, and it then calls the ``predict()`` 
method. For large files that can potentially exceed system RAM, it will be better to manually
load the files and make predictions.

.. code-block:: python

    import poetic

    pred = poetic.Predictor()
    result = pred.predict_file("<PATH>")

--------------------------------------------------------------

*******************
Preprocessing
*******************

The preprocessing toolchain consists of the following steps: tokenization, word ID
conversion, lower-case conversion, and padding. The latter two steps are primarily 
for keras models while tokenization can apply to other NLP workflows. This sections 
documents some of the details and their supported usage.

One-step Preprocessing
-----------------------

To preprocess the input for the default model of ``poetic``:

.. code-block:: python

    import poetic

    pred = poetic.Predictor()
    model_input = pred.preprocess("This is poetic. Isn't it?")

The ``preprocess()`` method returns a 2-d numpy array of tokenized word IDs that can
be directly predicted using the keras model's ``predict()`` method. However, the 
predictor's ``predict()`` method does not support a preprocessed input: only raw
input in strings are supported. 


Tokenization
-------------

Tokenization is the process of separating a string input into tokens, which are units
of texts that the algorithms support. The ``Predictor`` uses NLTK's ``sent_tokenize()``
and ``word_tokenize()`` functions respectively to perform two-step tokenization: first, 
the string, regardless of length, is tokenized into complete sentences; then, each 
sentence is tokenized into words and punctuations.

The ``tokenize()`` methods can be used as a stand-alone function although it is not a 
proper classmethod for compatibility with the ``Predictions`` class.

As an example:

.. code-block:: python

    import poetic

    pred = poetic.Predictor()
    model_input = pred.tokenize("This is poetic. Isn't it?")

The output will be a 2-d nested list in the following format: 

.. code-block:: text

    [['This', 'is', 'poetic', '.'], ['Is', "n't", 'it', '?']]


Padding
--------

Padding is part of the ``preprocess()`` method, and it cannot be called seprately.
It pads each tokenized input in accordance with the input shape of the default lexical
model used, which is 456. There is not yet support to adjust the padding length in this 
release, and this is the reason why custom model support is very limited.

Under the hood, the ``tf.keras.preprocessing.sequence.pad_sequences()`` method is called,
and the default pre-padding is used. Given that the default lexical model uses an LSTM
architechture, the pre-padding strategy makes sense. Currently, there is no support for
other types of padding.

Word IDs
---------

All tokens (mostly words, contractions, and punctuations after tokenized) are converted
into word IDs, which are all postive ``int``. By default, the gensim dictionary shipped
by the package is used. However, if a custom dictionary is supplied at initialization of
the ``Predictor``, it will likely  be incomptabile with the default model because models 
are specifically trained with one set of word IDs. Therefore, it is **not recommended**
to use a custom dictionary.