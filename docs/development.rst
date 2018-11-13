.. development:

Development
===========

If you're interested in contributing to the CMIP6 Data Citation Generator, we'd love to have you on board!
This section of the docs details how to get setup to contribute and how best to communicate.

.. contents:: :local:

Contributing
------------

All contributions are welcome, some possible suggestions include:

- tutorials (or support questions which, once solved, result in a new tutorial :D)
- blog posts
- improving the documentation
- bug reports
- feature requests
- pull requests

Please report issues or discuss feature requests in the `CMIP6 Data Citation Generator issue tracker`_.
If your issue is a feature request or a bug, please use the templates available, otherwise, simply open a normal issue :)

As a contributor, please follow a couple of conventions:

- Create issues in the `CMIP6 Data Citation Generator issue tracker`_ for changes and enhancements, this ensures that everyone in the community has a chance to comment
- Be welcoming to newcomers and encourage diverse new contributors from all backgrounds: see the `Python Community Code of Conduct <https://www.python.org/psf/codeofconduct/>`_


Getting setup
-------------

To get setup as a developer, we recommend the following steps (if any of these tools are unfamiliar, please see the resources we recommend in `Development tools`_):

#. Install make
#. Run ``make venv``, if that fails the commands are

    #. Create a Python virtual environment, ``python3 -m venv venv``
    #. Activate your virtual environment, ``source venv/bin/activate`` (on bash, other shells may be different)
    #. Upgrade pip ``pip install --upgrade pip``
    #. Install an editable version of the CMIP6 Data Citation Generator along with development dependencies, ``pip install -e .[test,docs,deploy]``

#. Make sure the tests pass by running ``make test``, if that files the commands are

    #. Run the unit and integration tests ``./venv/bin/pytest --cov -rfsxEX --cov-report term-missing``


Getting help
~~~~~~~~~~~~

Whilst developing, unexpected things can go wrong (that's why it's called 'developing', if we knew what we were doing, it would already be 'developed').
Normally, the fastest way to solve an issue is to contact us via the `issue tracker <https://github.com/znicholls/CMIP6-json-data-citation-generator/issues>`_.
The other option is to debug yourself.
For this purpose, we provide a list of the tools we use during our development as starting points for your search to find what has gone wrong.


Development tools
+++++++++++++++++

This list of development tools is what we rely on to develop the CMIP6 Data Citation Generator reliably and reproducibly.
It gives you a few starting points in case things do go inexplicably wrong and you want to work out why.
We include links with each of these tools to starting points that we think are useful, in case you want to learn more.

- `Git <http://swcarpentry.github.io/git-novice/>`_
- `Make <https://swcarpentry.github.io/make-novice/>`_
- `Tests <https://semaphoreci.com/community/tutorials/testing-python-applications-with-pytest>`_
    - we use a blend of `pytest <https://docs.pytest.org/en/latest/>`_ and the inbuilt Python testing capabilities for our tests so checkout what we've already done in ``tests`` to get a feel for how it works
- `Continuous integration (CI) <https://docs.travis-ci.com/user/for-beginners/>`_
    - we use `Travis CI <https://travis-ci.com/>`_ for our CI but there are a number of good providers
- Sphinx_


Other tools
+++++++++++

We also use some other tools which aren't necessarily the most familiar.
Here we provide a list of these along with useful resources.

.. _regular-expressions:

- `Regular expressions <https://www.oreilly.com/ideas/an-introduction-to-regular-expressions>`_
    - we use `regex101.com <regex101.com>`_ to help us write and check our regular expressions, make sure the language is set to Python to make your life easy!


Formatting
----------

To help us focus on what the code does, not how it looks, we use a couple of automatic formatting tools.
These automatically format the code for us and tell use where the errors are.
To use them, after setting yourself up (see `Getting setup`_), simply run ``make black`` and ``make flake8``.
Note that ``make black`` can only be run if you have committed all your work i.e. your working directory is 'clean'.
This restriction is made to ensure that you don't format code without being able to undo it, just in case something goes wrong.


Buiding the docs
----------------

After setting yourself up (see `Getting setup`_), building the docs is as simple as running ``make docs`` (note, run ``make -B docs`` to force the docs to rebuild and ignore make when it says '... index.html is up to date').
This will build the docs for you.
You can preview them by opening ``docs/_build/html/index.html`` in a browser.

For documentation we use Sphinx_.
To get ourselves started with Sphinx, we started with `this example <https://pythonhosted.org/an_example_pypi_project/sphinx.html>`_ then used `Sphinx's getting started guide <http://www.sphinx-doc.org/en/master/usage/quickstart.html>`_.


Gotchas
~~~~~~~

To get Sphinx to generate pdfs (rarely worth the hassle as they're automatically built on Read the Docs anyway), you require `Latexmk <https://mg.readthedocs.io/latexmk.html>`_.
On a Mac this can be installed with ``sudo tlmgr install latexmk``.
You will most likely also need to install some other packages (if you don't have the full distribution).
You can check which package contains any missing files with ``tlmgr search --global --file [filename]``.
You can then install the packages with ``sudo tlmgr install [package]``.


Docstring style
~~~~~~~~~~~~~~~

For our docstrings we use numpy style docstrings.
For more information on these, `here is the full guide <https://numpydoc.readthedocs.io/en/latest/format.html>`_ and `the quick reference we also use <https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_numpy.html>`_.


Releasing
---------

The steps to release a new version of the CMIP6 Data Citation Generator are shown below.
Please do all the steps below and all the steps for both release platforms.

#. Test installation with dependencies ``make test-install``
#. Update ``CHANGELOG.rst``:

    - add a header for the new version between ``master`` and the latest bullet point
    - this should leave the section underneath the master header empty

#. ``git add .``
#. ``git commit -m "Prepare for release of vX.Y.Z"``
#. ``git push``
#. ``git tag vX.Y.Z``
#. ``git push --tags``


PyPI
~~~~

#. ``make publish-on-testpypi``
#. Go to `test PyPI <https://test.pypi.org/project/cmip6-data-citation-generator/>`_ and check that the new release is as intended. If it isn't, stop and debug.
#. Test the install with ``make test-testpypi-install`` (this doesn't test all the imports as most required packages are not on test PyPI).
#. ``make publish-on-pypi``
#. Go to the `CMIP6 Data Citation Generator's PyPI`_ and check that the new release is as intended.
#. Test the install with ``make test-pypi-install`` (a pip only install will throw warnings about Iris not being installed, that's fine).


Last steps
~~~~~~~~~~

#. If you want to archive this version, follow the `instructions here <https://help.github.com/articles/creating-releases/>`_
#. Update any badges in ``README.rst`` that don't update automatically (note that the commits since badge only updates if you archive the version)
#. ``git add .``
#. ``git commit -m "Update README badges"``
#. ``git push``


Why is there a ``Makefile`` in a pure Python repository?
--------------------------------------------------------

Whilst it may not be standard practice, a ``Makefile`` is a simple way to automate general setup (environment setup in particular).
Hence we have one here which basically acts as a notes file for how to do all those little jobs which we often forget e.g. setting up environments, running tests (and making sure we're in the right environment), building docs, setting up auxillary bits and pieces.


Why did we choose a BSD 2-Clause License?
-----------------------------------------

We want to ensure that our code can be used and shared as easily as possible.
Whilst we love transparency, we didn't want to **force** all future users to also comply with a stronger license such as AGPL.
Hence the choice we made.

We recommend `Morin et al. 2012 <https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1002598>`_ for more information for scientists about open-source software licenses.


.. _Sphinx: http://www.sphinx-doc.org/en/master/
.. _CMIP6 Data Citation Generator issue tracker: https://github.com/znicholls/CMIP6-json-data-citation-generator/issues
.. _`CMIP6 Data Citation Generator's PyPI`: https://pypi.org/project/cmip6-data-citation-generator/
