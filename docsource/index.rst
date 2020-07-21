.. Ori documentation master file, created by
   sphinx-quickstart on Mon Jul 20 19:57:19 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Ori, a high-level concurrency library for Python
=================================================

.. toctree::
   :maxdepth: 2
   :caption: Contents:


Ori is a high-level wrapper around Python's `concurrent.futures` module, designed to make multithreading and multiprocessing as easy as possible.

Ori modules
-----------

The tools that Ori provides are divided into several modules.

`ori.asyncio </ori.asyncio/>`_ -- Tools to integrate Python asyncio code into a synchronous codebase, and vice-versa.
 
`ori.concurrency </ori.concurrency/>`_ -- Tools to run Python functions in the background using multithreading or multiprocessing.

`ori.poolchain </ori.poolchain/>`_ -- A way to chain function calls for parallel processing over any list or other iterable.

`ori.subprocess </ori.subprocess>`_ -- Tools for running external commands as subprocesses and efficiently collecting the standard output and standard error.


Frequently Asked Questions (FAQs)
---------------------------------

**Who made Ori?**

Ori was written by `James Mishra <https://jamesmishra.com>`_ and incubated at `Neocrym <https://neocrym.com>`_, a record label that uses artificial intelligence to find and promote musicians. Neocrym heavily relies on Ori to make their I/O-bound Python code run faster.

The source code for Ori is owned by Neocrym Records Inc, but licensed to Ori under the MIT License.

**Why should I use Ori over directly interfacing with `concurrent.futures`?**

The Python module `concurrent.futures` was introduced as a high-level abstraction over lower-level interfaces like `threading.Thread` and `multiprocessing.Process`. However, `concurrent.futures` merely moves the problem away from managing threads or processes to managing *executors*. Ori has the ambitious goal of also abstracting away the executors--making multithreading or multiprocessing no harder than writing single-threaded code.

**Is Ori a good replacement for Python's asyncio?**

For the hardcore `asyncio` user, probably not. Ori is focused on providing high-level abstractions over Python's `concurrent.futures` module that provides speed boosts for synchronous, I/O-bound Python.

**Where did the name "Ori" come from?**

The name "Ori" is a reference to the god-like villains in the Stargate TV shows. There is no meaningful connection between the villains or concurrency.


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
