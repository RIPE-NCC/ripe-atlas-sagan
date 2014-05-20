.. _requirements-and-installation:

Requirements & Installation
***************************

.. _installation-requirements:

Requirements
============

As you might have guessed, with all of the magic going on under the hood, there
are a few dependencies:

* `arrow`_
* dnspython `v2`_ or `v3`_
* `pyOpenSSL`_
* `python-dateutil`_
* `pytz`_
* `IPy`_

Additionally, we recommend that you also install `ujson`_ as it will speed up
the JSON-decoding step considerably, and `sphinx`_ if you intend to build the
documentation files for offline use.

.. _arrow: https://pypi.python.org/pypi/arrow/
.. _v2: https://pypi.python.org/pypi/dnspython/
.. _v3: https://pypi.python.org/pypi/dnspython3/
.. _pyOpenSSL: https://pypi.python.org/pypi/pyOpenSSL/
.. _python-dateutil: https://pypi.python.org/pypi/python-dateutil/
.. _pytz: https://pypi.python.org/pypi/pytz/
.. _IPy: https://pypi.python.org/pypi/IPy/
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

The quickest and easiest way to install Sagan is to use ``pip``:::

    $ pip install ripe.atlas.sagan


.. _installation-from-github:

From GitHub
-----------

If you're feeling a little more daring and want to use whatever is on GitHub,
you can have pip install right from there:::

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

Some setups (like MacOS) have trouble with some of the dependencies we're
using, so if they explode during the installation, you can still make use of
*some* of the parsers by deliberately excluding the problematic ones at
install time.

For example, if you want to skip the installation of ``pyOpenSSL`` (required for
parsing SSL certificate results), you can do this:::

     $ SAGAN_WITHOUT_SSL=1 pip install ripe.atlas.sagan


Similarly, you can skip the installation of ``dnspython`` and forgo any DNS
result parsing:::

    $ SAGAN_WITHOUT_DNS=1 pip install ripe.atlas.sagan
