Ori, a high-level concurrency library for Python
=================================================

Ori is a high-level wrapper around Python's `concurrent.futures` module, designed to make multithreading and multiprocessing as easy as possible.

Ori modules
-----------

The tools that Ori provides are divided into several modules.

`ori.asyncio <https://ori.technology.neocrym.com/en/latest/ori.asyncio/>`_ -- Tools to integrate Python asyncio code into a synchronous codebase, and vice-versa.

`ori.concurrency <https://ori.technology.neocrym.com/en/latest/ori.concurrency/>`_ -- Tools to run Python functions in the background using multithreading or multiprocessing.

`ori.poolchain <https://ori.technology.neocrym.com/en/latest/ori.poolchain/>`_ -- A way to chain function calls for parallel processing over any list or other iterable.

`ori.subprocess <https://ori.technology.neocrym.com/en/latest/ori.subprocess/>`_ -- Tools for running external commands as subprocesses and efficiently collecting the standard output and standard error.


Frequently Asked Questions (FAQs)
---------------------------------

**Who made Ori?**

Ori was written by `James Mishra <https://jamesmishra.com>`_ and incubated at `Neocrym <https://neocrym.com>`_, a record label that uses artificial intelligence to find and promote musicians. Neocrym heavily relies on Ori to make their I/O-bound Python code run faster.

The source code for Ori is owned by Neocrym Records Inc, but licensed to Ori under the MIT License.

**Why should I use Ori over directly interfacing with concurrent.futures?**

The Python module `concurrent.futures <https://docs.python.org/3/library/concurrent.futures.html>`_ was introduced as a high-level abstraction over lower-level interfaces like `threading.Thread` and `multiprocessing.Process`. However, `concurrent.futures` merely moves the problem away from managing threads or processes to managing *executors*. Ori has the ambitious goal of also abstracting away the executors--making multithreading or multiprocessing no harder than writing single-threaded code.

**Is Ori a good replacement for Python's asyncio?**

For the hardcore `asyncio <https://docs.python.org/3/library/concurrent.futures.html>`_ user, probably not. Ori is focused on providing high-level abstractions over Python's  `concurrent.futures <https://docs.python.org/3/library/concurrent.futures.html>`_ module that provides speed boosts for synchronous, I/O-bound Python.

**What do I need to know to contribute to Ori?**

Ori manages itself with the Python packaging tool `Poetry <https://python-poetry.org/>`_. You can install Poetry on your system with:

.. code:: text

    pip3 install poetry
    poetry install


To check that your changes to Ori's codebase match our coding standards, and to reformat any errant code to meet our standards, run this command:

.. code:: text

    poetry run make lint

To run Ori's unit tests in the Python virtualenv created by Poetry, just run:

.. code:: text

    poetry run make test
    
We can also run tests across multiple versions of Python with `Tox <https://tox.readthedocs.io/en/latest/>`_, but it requres your system has `Docker <https://docs.docker.com/get-docker/>`_ and `Docker Compose <https://docs.docker.com/compose/install/>`_ installed. If so, just run:

.. code:: text

    poetry run make tox

**Where did the name "Ori" come from?**

The name "Ori" is a reference to the god-like villains in the Stargate TV shows. There is no meaningful connection between the villains or concurrency.
