.. _requirements-and-installation:

Requirements & Installation
***************************

.. _installation-requirements:

Requirements
============

As you might have guessed, with all of the magic going on under the hood, there
are a few dependencies:

* `cryptography`_
* `python-dateutil`_
* `pytz`_

Additionally, we recommend that you also install `ujson`_ as it will speed up
the JSON-decoding step considerably, and `sphinx`_ if you intend to build the
documentation files for offline use.

.. _cryptography: https://pypi.python.org/pypi/cryptography
.. _python-dateutil: https://pypi.python.org/pypi/python-dateutil/
.. _pytz: https://pypi.python.org/pypi/pytz/
.. _ujson: https://pypi.python.org/pypi/ujson/
.. _sphinx: https://pypi.python.org/pypi/Sphinx/


.. _installation:

Installation
============

Installation should be easy, though it may take a while to install all of the
aforementioned requirements.  Using pip is the recommended method.


.. _installation-from-pip:

Using pip
---------

The quickest and easiest way to install Sagan is to use ``pip``::

    $ pip install ripe.atlas.sagan


.. _installation-from-github:

From GitHub
-----------

If you're feeling a little more daring and want to use whatever is on GitHub,
you can have pip install right from there::

    $ pip install git+https://github.com/RIPE-NCC/ripe.atlas.sagan.git


.. _installation-from-tarball:

From a Tarball
--------------

If for some reason you want to just download the source and install it manually,
you can always do that too.  Simply un-tar the file and run the following in the
same directory as ``setup.py``.::

    $ python setup.py install


.. _installation-troubleshooting:

Troubleshooting
---------------

Some setups (like MacOS) have trouble with building the dependencies required
for reading SSL certificates.  If you don't care about SSL stuff and only want
to use sagan to say, parse traceroute or DNS results, then you can do the following:

     $ SAGAN_WITHOUT_SSL=1 pip install ripe.atlas.sagan

More information can also be found `here`_.

If you *do* care about SSL and have to use a Mac, then `this issue`_ will likely
be of assistance.  Essentially, you will need to uninstall Xcode (if it's
installed already), then attempt to use ``gcc``.  This will trigger the OS to
ask if you want to install the Xcode compilation tools.  Click ``install``, and
when that's finished, install Sagan with this command:

    $ CFLAGS="-I/usr/include" pip install ripe.atlas.sagan

.. _here: https://cryptography.io/en/latest/installation/
.. _this issue: https://github.com/RIPE-NCC/ripe.atlas.sagan/issues/52
