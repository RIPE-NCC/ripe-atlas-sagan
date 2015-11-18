.. RIPE Atlas Sagan documentation master file, created by
   sphinx-quickstart on Tue Apr 29 13:41:57 2014.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to RIPE Atlas Sagan's documentation!
********************************************

A parsing library for RIPE Atlas measurement results

.. _index-why-this-exists:

Why This Exists
===============

RIPE Atlas generates a **lot** of data, and the format of that data changes over
time.  Often you want to do something simple like fetch the median RTT for each
measurement result between date `X` and date `Y`.  Unfortunately, there are are
dozens of edge cases to account for while parsing the JSON, like the format of
errors and firmware upgrades that changed the format entirely.

To make this easier for our users (and for ourselves), we wrote an easy to use
parser that's smart enough to figure out the best course of action for each
result, and return to you a useful, native Python object.

Contents:

.. toctree::
   :maxdepth: 2

   installation
   use
   types
   contributing
   changelog
