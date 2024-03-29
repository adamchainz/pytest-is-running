=================
pytest-is-running
=================

.. image:: https://img.shields.io/github/actions/workflow/status/adamchainz/pytest-is-running/main.yml?branch=main&style=for-the-badge
   :target: https://github.com/adamchainz/pytest-is-running/actions?workflow=CI

.. image:: https://img.shields.io/badge/Coverage-100%25-success?style=for-the-badge
  :target: https://github.com/adamchainz/pytest-is-running/actions?workflow=CI

.. image:: https://img.shields.io/pypi/v/pytest-is-running.svg?style=for-the-badge
   :target: https://pypi.org/project/pytest-is-running/

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg?style=for-the-badge
   :target: https://github.com/psf/black

.. image:: https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white&style=for-the-badge
   :target: https://github.com/pre-commit/pre-commit
   :alt: pre-commit

pytest plugin providing a function to check if pytest is running.

Unmaintained (2024-01-02)
=========================

I stopped maintaining this package as it doesn’t provide much value over checking whether pytest has been imported:

.. code-block:: python

    import sys

    if "pytest" in sys.modules:
        ...

In every project I’ve seen, pytest is only imported when running.

----

**Working on a Django project?**
Check out my book `Boost Your Django DX <https://adamchainz.gumroad.com/l/byddx>`__ which covers many ways to improve your development experience.
I created pytest-is-running whilst working on the book!

----

Installation
============

Install with:

.. code-block:: bash

    python -m pip install pytest-is-running

Python 3.8 to 3.12 supported.

Usage
=====

pytest will automatically find the plugin and use it when you run ``pytest``.
You can check if pytest is running with the ``is_running()`` function:

.. code-block:: python

    import pytest_is_running


    if pytest_is_running.is_running():
        ...

The package avoids importing pytest if it is not running, so that you don’t incur that overhead in non-test paths.

The package registers its plugin hooks as early as possible in pytest’s process, so it should be loaded before any of your non-test modules.

Rationale
=========

This plugin is an alternative to re-implementing `the pattern in the pytest documentation <https://docs.pytest.org/en/latest/example/simple.html#detect-if-running-from-within-a-pytest-run>`__.
As a plugin, it is loaded earlier than ``conftest.py`` or any other code in your project.
This makes it a more robust way of checking whether pytest is currently running.

Upstream `issue #9502 <https://github.com/pytest-dev/pytest/issues/9502>`__ discusses adding a feature to pytest.
It also covers an alternative which is often “good enough” - a simple check if pytest has been imported with:

.. code-block:: python

    "pytest" in sys.modules

This won’t be strictly accurate if you happen to import pytest outside of your test run, but that is not very common.
You may prefer to using this simpler technique instead of this plugin.
