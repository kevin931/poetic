=================
Keras Models
=================

``poetic`` relies on machine learning models trained with the ``tensorflow.keras`` framework.
This page gives an overview on the default models, the package's infrastructure for
loading the model and making predictors, and future model support. 

--------------------------------------------------------------

****************
Default Models
****************

The default models are the ones that are "shipped" with package, and currently, ``poetic``
supports only one model: **the lexical model**. See the *The Lexical Model* section for a 
detailed explanation of the model's performance and its backgrounds.

Downloading
------------

The trained model and weights combined are very large (~838MB), which is impractical to
ship with the ``pip`` or ``conda`` package. To address this issue, the models are hosted in
their own repository, `poetic-models <https://github.com/kevin931/poetic-models/>`_, on 
Github as releases. This can not only address the package size issue but also allow users
to decide whether and when to download the models in case there are bandwidth limitations.

A manual download of the models is not necessary. Whenever the ``Initializer`` class is 
called to load the default models, it will automatically check for the local presence of 
the models and in the case the models are not present, the ``poetic.util.Initializer.download_assets()``
method is called to fetch the models and place it in the correct directory. There is no
need to call the method to download the model upon first installation or update.

By default, the ``download_assets()`` method will ask for user input with the sample output
like the following: 

.. code-block:: 

    The following important assets are missing:
    -- lexical_model.json
    -- lexical_model.h5

    Downloading from: https://github.com/kevin931/poetic-models/releases/download/v1.0.0/lexical_model.zip
    Download size: 838MB.


    Would you like to download? [y/n]

If the user denies the download with letters other than "Y" or "y", the program may halt
because of the lack of a model. If there is a need to bypass the command-line input, set
``force_download_assets=True`` when initializing the ``Predictor`` class or ``force_download=True`` 
for ``download_assets()`` and ``load_model()`` methods of the ``Initializer`` class. The following
demonstrates a few valid ways of force downloading without command-line inputs:

.. code-block:: python

    import poetic

    # Approach #1
    poetic.Predictor(force_download_assets=True)
    # Approach #2
    poetic.util.download_assets(force_download=True)
    # Approach #3
    poetic.util.load_model(force_download=True)


Loading
---------

In the simplest use case of ``poetic`` through the ``Predictor`` class, there is no
need to manually load the model as the constructor can automatically load the default
model if the class is initialzed with the following:

.. code-block:: python

    import poetic

    pred = poetic.Predictor(force_download_assets=True)

However, there are benefits to loading the keras models directly, as it can expose
the full keras interface. The ``util`` module provides a few functions to conveiently
load the default model:

    - ``poetic.util.Initializer.initialize()``: This class method returns the command-line arguments, the default keras model, and the gensim dictionary.
    - ``poetic.util.Initializer.load_model()``: This class mothod returns the default keras model.

The advantage of using these two models is that only one function is necessary to load 
the model without having to know the data directory. However, to access the paths of the model
and the weights themselves, use the following snippet:

.. code-block:: python

    import pkg_resources
    import poetic

    data_dir = pkg_resources.resource_filename("poetic", "data/")
    weights_path = data_dir + "sent_model.h5"
    model_path = data_dir + "sent_model.json"


Updating
---------

Currently, model updates are planned to be handled with package updates. At of now, there
is no plan to update the existing model, except for changing its name from "sentence" to
"lexical" model. 

On the roadmap, there is plan to support meterical and combined lexical and metrical
models. With the release of such models, the package will be updated with the new model
urls or a new update mechanism.

If a qualitative update occurs, re-downloading the models will likely prove to be
necessary, and similar procedures will be in place as the initial download of the model.

--------------------------------------------------------------

******************
The Lexical Model
******************

The lexical model is currently the only default model available in ``poetic``. It is
trained using 18th- and 19th-century works with the lexical contexts through embedding 
(i.e. the contents of the works themselves in the form of words).

Essentially, the model is a classifier that classifies whether a given input is poetic.
More precisely, it can be interpreted as whether an input resembles eighteenth- and
nineteenth-century poetry. This definition will be the basis of the concept of the
**"poetic score"** throughout the package and the package's main use case.

**A quick note on naming**: The model has been renamed the "lexical model" stored with 
"lexical_model.h5" and "lexical_model.json" in the latest dev branch. It was previously 
named "sentence model" in v.1.0 because all training sets and inputs are sentence tokenized. 
Since all other future models will also take the same data format in sentence even though 
they are not necessarily lexical based, the model will be renamed  to the lexical model to 
better reflect how it was trained and what it represents. The package will automatically
handle renaming without any need to rename upon update.

Training and Validation Data
-----------------------------

All training and validation data come from Project Gutenberg. The datasets consist of
solely 18th- and 19th-century works separated into two categories: poetry and prose (non-poetry).
The rationale of this time period is that works during these two centuries are vastly
avaible in the public domain and digitized. Further, it is also a time when formal
poetry was still the norm instead of the rapid rise of free verse. Thus, this dataset
will allow the lexical model to train on the most distinguishing features of poetry.

Given the amount of data available on Project Gutenberg, the training and validation
sets consist of a random sample of the aforementioned works. Although a different sample
or the entire corpus may result in a different model, the amount of data within the sample
used can allow reasonable assumption of representativeness of the sample.


Model Architecture
-------------------

The overall architecture of the lexical model is a *bidirectional long-short-term memmoey neural network*
(LSTM) trained using the keras API of tensorflow. LSTM is known to work well with
lexical data although its performance has now been surpassed by large language models,
such as Google's `BERT <https://github.com/google-research/bert>`_.

Below is a high-level overview of the layers used in training the model (in sequential order):

+---------------+------------------+
| Layer         | Output Shape     |
+===============+==================+
| Input         | (None, 456)      |
+---------------+------------------+
| Embedding     | (None, 456, 128) |
+---------------+------------------+
| LSTM          | (None, 456, 128) |
+---------------+------------------+
| LSTM Forward  | (None, 128)      |
+---------------+------------------+
| LSTM Backward | (None, 128)      |
+---------------+------------------+
| Concatenate   | (None, 256)      |
+---------------+------------------+
| Dropout       | (None, 256)      |
+---------------+------------------+
| Dense         | (None, 64)       |
+---------------+------------------+
| Dropout       | (None, 64)       |
+---------------+------------------+
| Dense/Output  | (None, 1)        |
+---------------+------------------+


Model Performance
------------------

The confusion matrix: 

+--------+--------+--------+
|        | Prose  | Poetry |
+========+========+========+
| Prose  | 129168 | 42082  |
+--------+--------+--------+
| Poetry | 38230  | 125316 |
+--------+--------+--------+

Classification Diagnostics:

    - Accuracy: 0.7601
    - Precision: 0.7662
    - Sensitivity: 0.7486

--------------------------------------------------------------

**************
Custom Models
**************

Custom models are now fully supported starting v1.1.0. There are a few requirements for
custom models to work properly with ``poetic``:

    - The model has to be a keras model saved in ``.json``, ``.yaml``, or ``.h5`` format.
    - The input dimension has to be ``(None, int)``.
    - The first layer must be an embedding layer.

These limitations are in place because ``poetic`` is built with the keras framework in mind
and the preprocessing pipeline does not yet support models with different input dimensions.

**A note on gensim dictionary with custom models**: When using a custom model, a custom 
dictionary is recommended unless the custom model is trained with ``poetic``'s default dictionary. 
A custom dictionary can be loaded with the ``poetic.util.Initializer.load_dict()`` method. See the 
"Gensim Dictionary" section for full documentation on its usage and details.


Loading a Custom Model
-----------------------

The ``load_model`` method in the ``Initializer`` class has been updated to support custom models 
with any path:

.. code-block:: python

    import poetic

    # For models and weights saved separately:
    model = poetic.util.Initializer.load_model(model_path="<PATH>", weights_path="<PATH>")

    # For models saved in a single .h5 file:
    model = poetic.util.Initializer.load_model(model_path="<PATH>")

Both ``model_path`` and ``weights_path`` are keyword-only arguments, and when they are not
supplied, the method will default to the default model as expected. However, when ``weights_path``
is given and ``model_path`` is not, a ``ValueError`` will be thrown because it is an unsupported
configuration.


Using Custom Model with Predictor
----------------------------------

The ``Predictor`` class's constructor already supports the use of custom with its preprocessing
pipeline recently updated to automatically detect the correct input length. The simplest example 
will look like this if the model is already loaded as a python object:

.. code-block:: python

    import poetic

    pred = poetic.Predictor(model=custom_model, dictionary=custom_dictionary)

To load the model using the ``util`` module:

.. code-block:: python

    import poetic

    model = poetic.util.Initializer.load_model(model_path="<PATH>", weights_path="<PATH>")
    dictionary = poetic.util.Initializer.load_dict(dictionary_path="<PATH>")

    pred = poetic.Predictor(model=custom_model, dictionary=custom_dictionary)

All other methods function as normal after the model is loaded. 