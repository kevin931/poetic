=================
Module Overview
=================

This page documents the public interfaces of ``poetic`` as a high-level overview. While
all classes and methods are accessible using their full path, some classes are designed
to be called at the package level and a few others are more or less "internal" even if
they are not strictly protected with underscores. For more detailed documentation on the
parameters and exact behaviors of each class and method, refer to the **Full Documentation**
section. 

--------------------------------------------------------------

****************
Import Behavior
****************

Modules
--------

There are five modules in total:
    - ``exceptions``: An internal module for custom exceptions.
    - ``gui``: An internal module for the GUI invoked by ``-g`` flag.
    - ``predictor``: A module including the ``Predictor`` class to make predictions.
    - ``results``: A module for prediction results and diagnostics.
    - ``util``: A utility module for utility class, functions, and package information.

Package-level Classes 
----------------------

Two classes are directly exposed as package-level classes: ``Predictor`` and 
``Diagnostics``. Respectively, they can be accessed directly with ``poetic.Predictor`` 
and ``poetic.Diagnostics``. 

These two classes, especially ``Predictor``, are the main interfaces of the package.
Therefore, they are directly exposed instead of requiring the access through
``poetic.predictor.Predictor`` and ``poetic.results.Diagnostics``, which are both valid
as well. 

--------------------------------------------------------------

***********************
Modules Overview
***********************

Each module will be documentation in its own topic at length. This section is
a quick overview of their functionalities.


*exceptions*
---------------

The ``exceptions`` module contains three classes: ``InputLengthError``, ``UnsupportedConfigError``,
``SingletonError``, and ``ModelShapeError``. They all inherit directly from python's base
``Exception`` class, and they are raised by various methods and classes in ``poetic``.

Although the module and its classes are not preceded by _ to allow for better acceessibility
and more obvious documentation, it is mainly intended for internal use. 


*gui*
---------------

The ``gui`` module contains the ``GUI`` class which implements a Tkinter GUI for 
``poetic``. All the methods of ``GUI`` are private, and the ``gui`` module is mainly
an internal interface. 

To launch the GUI, using the ``-g`` flag on the command line is recommended instead of
importing ``poetic`` and invoking the ``GUI`` class.



*predictor*
---------------

The ``predictor`` class and its package-level ``Predictor`` class serve as the main
interface for the class to predict poetic scores using Keras model. The ``Predictor``
class is a one-step solution for making predictions as it can load models and dictionaries
automatically. To make a prediction, simply follow the following example: 

.. code-block:: python

    import poetic

    pred = poetic.Predictor()
    prediction = pred.predict("Is this poetic?")

The ``Predictions`` class is the return type of the ``predict()`` and ``predict_file()``
methods of the ``Predictor``, and it inherits directly from ``Diagnostics`` class. It currently
contains all the same methods as its base class and is mainly intended to be invoked
internally. To use its functionalities without the ``Predictor`` class, directly use the
``Diagnostics`` class instead.


*results*
---------------

The ``results`` module contains the ``Diagnostics`` class, which is the base class for
the ``Predictions`` class. Its main functionality includes running diagnotics for predictions,
outputing to files, and generating diagnostics report. The ``Diagnostics`` can be used as
a standalone class for any predictions, and more utility and functionalities are planned 
for the future to add more common, useful diagnotics.


*util*
---------------

The ``util`` module provides utility functions and classes for ``poetic``, including package
metadata, loading and downloading assets, and parsing commandline arguments. It contains
two public classes: ``Info`` and ``Initializer``. The ``_Arguments`` class is intended strictly
for internal use to parse command-line arguments for ``__main__.py``.


The ``Info`` class is a singleton that provides basic package information: package vesion,
build status, and a unittest variable as a debug flag. To initialize the ``Info`` class, use
``poetic.util.Info.get_instance()`` instead of the constructor to avoid a ``SingletonError``.
The version and build status of the package can be accessed with use methods
``poetic.util.Info.get_instance().version()`` and ``poetic.util.Info.get_instance().build()``
respectively.

The ``Initializer`` class initializes assets for the ``Predictor`` class, and it contains 
all class methods without no need of a class instance. The most common use is to load both
the model and dictionary using the ``poetic.util.Initializer.initialize()`` method which is
automatically called by the ``Predictor`` by default. 