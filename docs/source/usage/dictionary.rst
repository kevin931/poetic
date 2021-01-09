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

The ``Predictor`` class loads the default dictionary by default if the ``dictionary`` parameter is
not specified as in the example below: 

.. code-block:: python

    import poetic

    pred = poetic.Predictor()

Under the hood, the ``Predictor`` calls the ``Initializer`` class to load the dictionary, which is
also a valid way of loading the dictionary independently:

.. code-block:: python

    import poetic

    dictionary = poetic.util.Initializer.load_dict()
    # If a Predictor is to be used:
    pred = poetic.Predictor(dictionary=dictionary)

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

There is now full support for custom dictionary in both the ``Predictor`` and the ``Initializer``
class with all gensim models saved as a text file with the ``save_as_text()`` method or files of 
the same format. There are mainly two use cases of a custom dictionary, which is similar to the
usage of a default dictionary, as documented below.

Loading
--------

The ``load_dict()`` method of the ``Initializer`` class now supports loading a dictionary through
stored elsewhere: 

.. code-block:: python

    import poetic

    dictionary = poetic.util.Initializer.load_dict(dictionary_path="<PATH>")

Custom Dictionary with Predictor
---------------------------------

The workflow of using a custom dictionary with the ``Predictor`` class is practically combining
the loading snippet with the initialization of a predictor:

.. code-block:: python

    import poetic

    dictionary = poetic.util.Initializer.load_dict(dictionary_path="<PATH>")
    pred = poetic.Predictor(dictionary=dictionary)

One **important** thing to note is that the ``dictionary`` and ``model`` parameteres of the ``Predictor``'s 
constructor are independent of each other: loading a custom model will not require a custom dictionary 
and vice versa. Therefore, if a custom model is used, it is **recommended**, though not required by the 
package, to use a custom dictionary. A more common way of using a custom model and dictionary combination
looks like this:

.. code-block:: python

    import poetic

    model = poetic.util.Initializer.load_model(dictionary_path="<PATH>")
    dictionary = poetic.util.Initializer.load_dict(dictionary_path="<PATH>")
    pred = poetic.Predictor(model=model, dictionary=dictionary)

Dictionary Saved with "save()"
------------------------------

Gensim's ``gensim.corpora.dictionary.Dictionary`` class has a ``save()`` method that saves
a dictionary in a format that is not compatible with the ``load_dict()`` method. Therefore,
``gensim`` needs to be imported to load the dictionary separately: 

.. code-block:: python

    import poetic
    import gensim

    dictionary = gensim.corpora.Dictionary.load(fname="<PATH>")
    pred = poetic.Predictor(dictionary=dictionary)