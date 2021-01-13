==================================
Further Documentation and Links
==================================

There are a few more resources beyond this website, including those included with the
package and those of the dependencies. For links and references, see the appropriate
sections below.

--------------------------------------------------------------

**********************
Package Docstring
**********************

All public modules, classes, functions, and methods have docstrings. To view the rendered
docstrings as documentation, see the "**Full Documentation**" section. To see how to access
such the resources in python, see the "**Package Information and Resources**" section of the
documentation.

--------------------------------------------------------------

**************************
Installation Documentation
**************************

For installation, please see the "**Installation Guide**" page for details. For documentation
on pip and conda themselves, links are provided below.

pip
----

``pip`` documentation: https://pip.pypa.io/en/stable/.

conda 
------

General ``conda`` documentation: https://docs.conda.io/projects/conda/en/latest/index.html

Managing ``conda`` environments: https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html

``conda`` channels: https://docs.conda.io/projects/conda/en/latest/user-guide/concepts/channels.html

--------------------------------------------------------------

*************************
Dependency Documentation
*************************

Keras Models
-------------

For furthur documentation on keras models, refer to tensorflow's offical documentation
through https://www.tensorflow.org/api_docs/python/tf/keras. 

Gensim Dictionaries
--------------------

For furthur documentation on gensim dictionaries, refer to gensim's offical documentation
through https://radimrehurek.com/gensim/corpora/dictionary.html. 

Numpy Arrays
-------------

Numpy arrays are used in some under-the-hood processing. For documentation on numpy arrays in general,
see https://numpy.org/devdocs/reference/generated/numpy.array.html.

For ndarray, which is the return type of the ``preprocess()`` method of the ``Predictor`` class,
see https://numpy.org/doc/stable/reference/generated/numpy.ndarray.html.

NLTK
-----

The ``Predictor`` class uses NLTK's tokenization algorithms through its ``sent_tokenize()``
and ``word_tokenize()``. More detailed documentation can be found here:
https://www.nltk.org/api/nltk.tokenize.html