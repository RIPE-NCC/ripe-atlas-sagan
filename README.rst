RIPE Atlas Sagan |Build Status| |Documentation|
===============================================

A parsing library for RIPE Atlas measurement results

Why this exists
---------------

RIPE Atlas generates a **lot** of data, and the format of that data changes over
time. Often you want to do something simple like fetch the median RTT for each
measurement result between date ``X`` and date ``Y``. Unfortunately, there are
dozens of edge cases to account for while parsing the JSON, like the format of
errors and firmware upgrades that changed the format entirely.

To make this easier for our users (and for ourselves), we wrote an easy to use
parser that's smart enough to figure out the best course of action for each
result, and return to you a useful, native Python object.

How to install
--------------

The stable version should always be in PyPi, so you can install it with ``pip``:

.. code:: bash

    $ pip install ripe.atlas.sagan

Better yet, make sure you get ujson and sphinx installed with it:

.. code:: bash

    $ pip install ripe.atlas.sagan[fast,doc]

Troubleshooting
~~~~~~~~~~~~~~~

Some setups (like MacOS) have trouble with building the dependencies required
for reading SSL certificates. If you don't care about SSL stuff and only want to
use sagan to say, parse traceroute or DNS results, then you can do the following:

.. code:: bash

    $ SAGAN_WITHOUT_SSL=1 pip install ripe.atlas.sagan

Quickstart: How To Use It
-------------------------

You can parse a result in a few ways. You can just pass the JSON-encoded string:

.. code:: python

    from ripe.atlas.sagan import PingResult

    my_result = PingResult("<result string from RIPE Atlas ping measurement>")

    print(my_result.rtt_median)
    123.456

    print(my_result.af)
    6

You can do the JSON-decoding yourself:

.. code:: python

    from ripe.atlas.sagan import PingResult

    my_result = PingResult(
        json.loads("<result string from RIPE Atlas ping measurement>")
    )

    print(my_result.rtt_median)
    123.456

    print(my_result.af)
    6

You can let the parser guess the right type for you, though this incurs a small
performance penalty:

.. code:: python

    from ripe.atlas.sagan import Result

    my_result = Result.get("<result string from RIPE Atlas ping measurement>")

    print(my_result.rtt_median)
    123.456

    print(my_result.af)
    6

What it supports
----------------

Essentially, we tried to support everything. If you pass in a DNS result string,
the parser will return a ``DNSResult`` object, which contains a list of
``Response``'s, each with an ``abuf`` property, as well as all of the
information in that abuf: header, question, answer, etc.

.. code:: python

    from ripe.atlas.sagan import DnsResult

    my_dns_result = DnsResult("<result string from a RIPE Atlas DNS measurement>")
    my_dns_result.responses[0].abuf  # The entire string
    my_dns_result.responses[0].abuf.header.arcount  # Decoded from the abuf

We do the same sort of thing for SSL measurements, traceroutes, everything. We
try to save you the effort of sorting through whatever is in the result.

Which attributes are supported?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Every result type has its own properties, with a few common between all types.

Specifically, these attributes exist on all ``*Result`` objects:

-  ``created`` An datetime object of the
   ``timestamp`` field
-  ``measurement_id``
-  ``probe_id``
-  ``firmware`` An integer representing the firmware version
-  ``origin`` The ``from`` attribute in the result
-  ``is_error`` Set to ``True`` if an error was found

Additionally, each of the result types have their own properties, like
``packet_size``, ``responses``, ``certificates``, etc. You can take a look at
the classes themselves, or just look at the tests if you're curious. But to get
you started, here are some examples:

.. code:: python

    # Ping
    ping_result.packets_sent  # Int
    ping_result.rtt_median    # Float, rounded to 3 decimal places
    ping_result.rtt_average   # Float, rounded to 3 decimal places

    # Traceroute
    traceroute_result.af                   # 4 or 6
    traceroute_result.total_hops           # Int
    traceroute_result.destination_address  # An IP address string

    # DNS
    dns_result.responses                        # A list of Response objects
    dns_result.responses[0].response_time       # Float, rounded to 3 decimal places
    dns_result.responses[0].headers             # A list of Header objects
    dns_result.responses[0].headers[0].nscount  # The NSCOUNT value for the first header
    dns_result.responses[0].questions           # A list of Question objects
    dns_result.responses[0].questions[0].type   # The TYPE value for the first question
    dns_result.responses[0].abuf                # The raw, unparsed abuf string

    # SSL Certificates
    ssl_result.af                        # 4 or 6
    ssl_result.certificates              # A list of Certificate objects
    ssl_result.certificates[0].checksum  # The checksum for the first certificate

    # HTTP
    http_result.af                      # 4 or 6
    http_result.uri                     # A URL string
    http_result.responses               # A list of Response objects
    http_result.responses[0].body_size  # The size of the body of the first response

    # NTP
    ntp_result.af                          # 4 or 6
    ntp_result.stratum                     # Statum id
    ntp_result.version                     # Version number
    ntp_result.packets[0].final_timestamp  # A float representing a high-precision NTP timestamp
    ntp_result.rtt_median                  # Median value for packets sent & received

What it requires
----------------

As you might have guessed, with all of this magic going on under the hood, there
are a few dependencies:

-  `cryptography`_ (Optional: see "Troubleshooting" above)
-  `python-dateutil`_
-  `pytz`_
-  `IPy`_

Additionally, we recommend that you also install `ujson`_ as it will speed up
the JSON-decoding step considerably, and `sphinx`_ if you intend to build the
documentation files for offline use.

Running Tests
-------------

There's a full battery of tests for all measurement types, so if you've made
changes and would like to submit a pull request, please run them (and update
them!) before sending your request:

.. code:: bash

    $ python setup.py test

You can also install ``tox`` to test everything in all of the supported Python
versions:

.. code:: bash

    $ pip install tox
    $ tox

Further Documentation
---------------------

Complete documentation can always be found on `Read the Docs`_,
and if you're not online, the project itself contains a ``docs`` directory --
everything you should need is in there.


Who's Responsible for This?
---------------------------

Sagan is actively maintained by the RIPE NCC and primarily developed by `Daniel
Quinn`_, while the abuf parser is mostly the responsibility of `Philip Homburg`_
with an assist from Bert Wijnen and Rene Wilhelm who contributed to the original
script. `Andreas Stirkos`_ did the bulk of the work on NTP measurements and
fixed a few bugs, and big thanks go to `Chris Amin`_, `John Bond`_, and
`Pier Carlo Chiodi`_ for finding and fixing stuff where they've run into
problems.


Colophon
--------

But why "`Sagan`_"? The RIPE Atlas team decided to name all of its modules after
explorers, and what better name for a parser than that of the man who spent
decades reaching out to the public about the wonders of the cosmos?

.. _python-dateutil: https://pypi.python.org/pypi/python-dateutil
.. _cryptography: https://pypi.python.org/pypi/cryptography
.. _pytz: https://pypi.python.org/pypi/pytz
.. _IPy: https://pypi.python.org/pypi/IPy/
.. _ujson: https://pypi.python.org/pypi/ujson
.. _sphinx: https://pypi.python.org/pypi/Sphinx
.. _Read the Docs: http://ripe-atlas-sagan.readthedocs.org/en/latest/
.. _Daniel Quinn: https://github.com/danielquinn
.. _Philip Homburg: https://github.com/philiphomburg
.. _Andreas Stirkos: https://github.com/astrikos
.. _Chris Amin: https://github.com/chrisamin
.. _John Bond: https://github.com/b4ldr
.. _Pier Carlo Chiodi: https://github.com/pierky
.. _Sagan: https://en.wikipedia.org/wiki/Carl_Sagan
.. |Build Status| image:: https://travis-ci.org/RIPE-NCC/ripe.atlas.sagan.png?branch=master
   :target: https://travis-ci.org/RIPE-NCC/ripe.atlas.sagan
.. |Documentation| image:: https://readthedocs.org/projects/ripe-atlas-sagan/badge/?version=latest
   :target: http://ripe-atlas-sagan.readthedocs.org/en/latest/?badge=latest
   :alt: Documentation Status
