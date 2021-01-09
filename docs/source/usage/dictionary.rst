=============================
Gensim Dictionary
=============================

The ``Predictor`` class uses a gensim dictionary to convert words (also called "tokens") into IDs
for the keras model's embedding layer. Each word has a unique numeric ID that allows the model to
create deep embedding to capture the lexical context.

This section of the documentation details the use of gensim dictionaries in ``poetic``, the default,
and custom dictionary options along with examples.

--------------------------------------------------------------

*******************
Default Dictionary
*******************

The ``poetic`` package ships with a default dictionary in both ``pip`` and ``conda`` distributions.
Given its relatively manageable size, it is included as package data with each release, and there 
is no need to download the dictionary separately, unlike the default keras model.

The dictionary is constructed using the entire corpus of 18th- and 19th-century literary works on 
Project Gutenberg, as opposed to the randomly sample used for traning. It should cover a wide range 
of lexicons encountered in both literature of the time and everyday usage although newest words and 
slangs may be lacking. In the ``Predictor`` class, all non-existant words are assigned with the 
value 0 for consistency. 

Format
-------

The dictionary is saved with the ``save_as_text()`` method of the 
``gensim.corpora.dictionary.Dictionary`` class. The file has the following format, which is 
also documented `here <https://radimrehurek.com/gensim/corpora/dictionary.html>`_:

.. code-block::

    76242402
    440	!	4922258
    36666	#	12419
    17501	$	23781
    142	'	2078602
    174	''	5630856

The first line is the number of entries, and following lines each has three tokens separated by
tabs: ID, word, document frequency.

Only dictionaries of this format are supported at this time because a tab-separated text file will
allow the useage without ``gensim`` dependency for best future support with custom classes. If a
custom dictionary is saved with the ``save()`` method, it needs to be loaded manually as documented
below.


Loading
--------

The ``Predictor`` class loads the default dictionary by default if the ``dict`` parameter is not
specified as in the example below: 

.. code-block:: python

    import poetic

    pred = poetic.Predictor()

One **important** thing to note is that the ``dict`` and ``model`` parameters are independent of
each other: loading a custom model will not require a custom dictionary and vice versa. Therefore,
if a custom model is used, it is **recommended**, though not required by the package, to use a custom
dictionary. 

Under the hood, the ``Predictor`` calls the ``Initializer`` class to load the dictionary, which is
also a valid way of loading the dictionary independently:

.. code-block:: python

    import poetic

    dictionary = poetic.util.Initializer.load_dict()
    # If a Predictor is to be used:
    pred = poetic.Predictor(dict=dictionary)

The above two snippets are functionally equivalent as shown, but the latter approach allows for
the use of a dictionary independently, including accessing its own methods attributes, etc.

The dictionary is stored in the data directory of the package. To access the path of the dictionary,
use this snippet:

.. code-block:: python

    import pkg_resources
    import poetic

    data_dir = pkg_resources.resource_filename("poetic", "data/")
    dictionary_path = data_dir + "word_dictionary_complete.txt"

Updating
---------

The dictionary will be updated with the package itself. However, on the current roadmap, there is
no update planned for the gensim dictionary itself. Should there be a change, the process will
be automated without manual downloading, renaming, etc.

--------------------------------------------------------------

*******************
Custom Dictionary
*******************

The current version, v1.0.x, does not have have full support for custom dictionary although
the ``Predictor`` class does allow a custom dictionary during initialization. Since there is
not yet support for custom models, using a custom dictionary will be practically meaningless
with one exception: the use of a custom model with the same input shape with a custom model.
See the "Keras Models" section for a more detailed explanation of the state of custom models.

To use a custom model with the ``Predictor``, the following snippet will work:

.. code-block:: python

    import poetic
    import gensim

    dictionary = gensim.corpora.Dictionary.load_from_text(fname="<PATH>")
    pred = poetic.Predictor(dict=dictionary)

To use a dictionary saved in the format saved with the ``save()`` method:

.. code-block:: python

    import poetic
    import gensim

    dictionary = gensim.corpora.Dictionary.load(fname="<PATH>")
    pred = poetic.Predictor(dict=dictionary)