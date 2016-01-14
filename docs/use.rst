.. _use-and-examples:

Use & Examples
**************

The library contains a full test suite for each measurement type, so if you're
looking for examples, it's a good idea to start there.  For this document we'll
cover basic usage and some simple examples to get you started.


.. _use:

How To Use This Library
=======================

Sagan's sole purpose is to make RIPE Atlas measurements manageable from within
Python.  You shouldn't have to be fiddling with JSON, or trying to find values
that changed locations between firmware versions.  Instead, you should always
be able to pass in the JSON string and immediately get usable Python objects.


.. _use-basics:

Important Note
--------------

The one thing that tends to confuse people when first trying out Sagan is that
this library operates on **single measurement results**, and not a list of
results.  If you have a list of results (for example, the output of the
measurement results API), then you must loop over those results and pass each
result to Sagan for parsing.

Basics
------

To that end, the interface is pretty simple.  If you have a ping measurement
result, then use the PingResult class to make use of the data::

    from ripe.atlas.sagan import PingResult

    my_result = PingResult('this is where your big JSON blob goes')

    my_result.af
    # Returns 6

    my_result.rtt_median
    # Returns 123.456

Note that ``rtt_median`` isn't actually in the JSON data passed in.  It's
calculated during the parsing phase so you don't need to fiddle with looping
over attributes in a list and doing the math yourself.


.. _use-plain-text-not-required:

Plain Text Not Required
-----------------------

It should be noted that while all of the examples here use a plain text string
for our results, Sagan doesn't force you to pass in a string.  It's just as
happy with a Python dict, the result of already running your result string
through ``json.loads()``::

    import json
    from ripe.atlas.sagan import PingResult

    my_result_dict = json.loads('this is where your big JSON blob goes')
    my_result = PingResult(my_result_dict)

    my_result.af
    # Returns 6

    my_result.rtt_median
    # Returns 123.456


.. _use-agnostic-parsing:

Agnostic Parsing
----------------

There may be a case where you have code that's just expected to parse a result
string, without knowing ahead of time what type of result it is.  For this we
make use of the parent ``Result`` class' ``get()`` method::

    from ripe.atlas.sagan import Result

    my_result = Result.get('this is where your big JSON blob goes')

    my_result.af
    # Returns 6

    my_result.rtt_median
    # Returns 123.456

As you can see it works just like PingResult, but doesn't force you to know its
type up front.  Note that this does incur a small performance penalty however.


.. _use-errors-and-malformations:

Errors & Malformations
----------------------

RIPE Atlas, like the Internet is never 100% what you'd expect.  Sometimes your
measurement will return an error such as a timout or DNS lookup problem, and
sometimes the data in a result might even be malformed on account of data
corruption, damaged probe storage, etc.

And like the most applications on the Internet, Sagan attemps to handle these
inconsistencies gracefully.  You can decide just how gracefully however.

Say for example you've got a result that looks alright, but the ``abuf`` value
is damaged in some way rendering it unreadable.  You'll find that while the
``DnsResult`` object will not have a ``is_malformed=False``, the portion that is
unreadable will be set to ``True``::

    from ripe.atlas.sagan import DnsResult
    my_result = DnsResult('your JSON blob')

    my_result.is_error                        # False
    my_result.is_malformed                    # False
    my_result.responses[0].abuf.is_malformed  # True
    my_result.responses[1].abuf.is_malformed  # False

You can control what you'd like Sagan to do in these cases by setting
``on_malformation=`` when parsing::

    from ripe.atlas.sagan import DnsResult

    # Sets is_malformed=True and issues a warning
    my_result = DnsResult('your JSON blob')

    # Sets is_malformed=True
    my_result = DnsResult('your JSON blob', on_malformation=DnsResult.ACTION_IGNORE)

    # Sets explodes with a ResultParseError
    my_result = DnsResult('your JSON blob', on_malformation=DnsResult.ACTION_FAIL)

Similarly, you can do the same thing with ``on_error=``, which perform the same
way when Sagan encounters an error like a timeout or DNS lookup problem.

Error handling is not yet complete in Sagan, so if you run across a case where
it behaves in a way other than what you'd expect, please send a copy of the
problematic result to atlas@ripe.net and we'll use it to update this library.


.. _examples:

Examples
========

.. _examples-file:

Parsing Results out of a Local File
-----------------------------------

Assume for a moment that you've downloaded a bunch of results into a local file
using our *fragmented JSON* format.  That is, you have in your possession a file
that has a separate JSON result on every line.  For the purposes of our example
we'll call it ``file.txt``.::

    from ripe.atlas.sagan import Result

    my_results_file = "/path/to/file.txt"
    with open(my_results_file) as results:
        for result in results.readlines():
            parsed_result = Result.get(result)
            print(parsed_result.origin)

Basically you use Python to open the file (using ``with``) and then loop over
each line in the file (``.readlines()``), sending each line into Sagan which
returns a ``parsed_result``.  With that result, you can then pull out any of
the values you like, using the :ref:`attributes-methods` documentation as a
reference.


.. _examples-api:

Pulling Directly from the API
-----------------------------

A common use case for the parser is to plug it into our RESTful API service.
The process for this is pretty simple: fetch a bunch of results, loop over them,
and for each one, apply the parser to get the value you want.

Say for example you want to get the ``checksum`` value for each result from
measurement `#1012449`_.  To do this, we'll fetch the latest results from each
probe via the ``measurement-latest`` API, and parse each one to get the
checksum values::

    import requests
    from ripe.atlas.sagan import SslResult

    source = "https://atlas.ripe.net/api/v1/measurement-latest/1012449/"
    response = requests.get(source).json

    for probe_id, result in response.items():

        result = result[0]                 # There's only one result for each probe
        parsed_result = SslResult(result)  # Parsing magic!

        # Each SslResult has n certificates
        for certificate in parsed_result.certificates:
            print(certificate.checksum)  # Print the checksum for this certificate

        # Make use of the handy get_checksum_chain() to render the checksum of each certificate into one string if you want
        print(parsed_result.get_checksum_chain())


.. _#1012449: https://atlas.ripe.net/measurements/1012449/


.. _examples-types:

Samples from Each Type
----------------------


.. _examples-types-ping:

Ping
....

For more information regarding all properties available, you should consult the
:ref:`ping` section of this documentation.::

    ping_result.packets_sent  # Int
    ping_result.rtt_median    # Float, rounded to 3 decimal places
    ping_result.rtt_average   # Float, rounded to 3 decimal places


.. _examples-types-traceroute:

Traceroute
..........

For more information regarding all properties available, you should consult the
:ref:`traceroute` section of this documentation.::

    traceroute_result.af                   # 4 or 6
    traceroute_result.total_hops           # Int
    traceroute_result.destination_address  # An IP address string


.. _examples-types-dns:

DNS
....

For more information regarding all properties available, you should consult the
:ref:`dns` section of this documentation.::

    dns_result.responses                        # A list of Response objects
    dns_result.responses[0].response_time       # Float, rounded to 3 decimal places
    dns_result.responses[0].headers             # A list of Header objects
    dns_result.responses[0].headers[0].nscount  # The NSCOUNT value for the first header
    dns_result.responses[0].questions           # A list of Question objects
    dns_result.responses[0].questions[0].type   # The TYPE value for the first question
    dns_result.responses[0].abuf                # The raw, unparsed abuf string


.. _examples-types-sslcert:

SSL Certificates
................

For more information regarding all properties available, you should consult the
:ref:`sslcert` section of this documentation.::

    ssl_result.af                        # 4 or 6
    ssl_result.certificates              # A list of Certificate objects
    ssl_result.certificates[0].checksum  # The checksum for the first certificate


.. _examples-types-http:

HTTP
....

For more information regarding all properties available, you should consult the
:ref:`http` section of this documentation.::

    http_result.af                      # 4 or 6
    http_result.uri                     # A URL string
    http_result.responses               # A list of Response objects
    http_result.responses[0].body_size  # The size of the body of the first response
