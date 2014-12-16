.. _attributes-methods:

Attributes & Methods
********************


.. _common-attributes:

Common Attributes
=================

All measurement results have a few common properties.

=====================  ========  ================================================================
Property               Type      Explanation
=====================  ========  ================================================================
raw_data               dict      The entire measurement result, as-is from `json.loads()`
created                arrow     The time at which this result was initiated
created_timestamp      int       A Unix timestamp value for the ``created`` attribute
measurement_id         int
probe_id               int
firmware               int       The probe firmware release
origin                 str       The IP address of the probe
seconds_since_sync     int       The number of seconds since the probe last syncronised its clock
is_malformed           bool      Whether the result (or related portion thereof) is unparseable
is_error               bool      Whether or not there were errors in parsing/handling this result
error_message          str       If the result is an error, the message string is in here
=====================  ========  ================================================================

* Note that an ``arrow`` object is essentially a ``datetime`` object with some
  additional magic.  If you're curious as to the nature of that magic, `the Arrow website`_
  should get you started.

.. _the Arrow website: http://crsmithdev.com/arrow/


.. _ping:

Ping
====

The simplest measurement type, ``ping`` measurement results contain all of the
properties :ref:`common to all measurements <common-attributes>` as well as the following:

=====================  =====  ===================================================================================
Property               Type   Explanation
=====================  =====  ===================================================================================
af                     int    The address family.  It's always either a ``4`` or a ``6``.
duplicates             int    The number duplicates found
rtt_average            float
rtt_median             float
rtt_min                float
rtt_max                float
packets_sent           int
packets_received       int
packet_size            int
destination_name       str    The string initially given as the target.  It can be an IP address or a domain name
destination_address    str    An IP address represented as a string
step                   int    The number of seconds between ping requests (interval)
packets                list   A list of ping :ref:`ping-packet` objects
=====================  =====  ===================================================================================


.. _ping-packet:

Packet
------

Each ping request sends ``n`` packets, where ``n`` is a value specified at
measurement creation time.  We represent these packets as ``Packet`` objects.

=====================  =====  ================================================================
Property               Type   Explanation
=====================  =====  ================================================================
rtt                    float
dup                    bool   Set to ``True`` if this packet is a duplicate
ttl                    int
source_address         str    An IP address represented as a string
=====================  =====  ================================================================


.. _traceroute:

Traceroute
==========

Probably the largest result type, ``traceroute`` measurement results contain all
of the properties :ref:`common to all measurements <common-attributes>` as well as the following:

========================  ========  ===================================================================================
Property                  Type      Explanation
========================  ========  ===================================================================================
af                        int       The address family.  It's always either a ``4`` or a ``6``.
destination_name          str       The string initially given as the target.  It can be an IP address or a domain name
destination_address       str       An IP address represented as a string
source_address            str       An IP address represented as a string
end_time                  datetime  The time at which the traceroute finished
end_time_timestamp        int       A Unix timestamp for the ``end_time`` attribute
paris_id                  int
size                      int       The packet size
protocol                  str       One of ``ICMP``, ``TCP``, ``UDP``
hops                      list      A list of :ref:`traceroute-hop` objects
total_hops                int       The total number of hops
ip_path                   list      A list of dicts containing the IPs at each hop. This is just for convenience as all of these values are accessible via the :ref:`traceroute-hop` and :ref:`traceroute-packet` objects.
last_rtt                  float     The RTT from the last successful hop
destination_ip_responded  bool      Set to ``True`` if the last hop was a response from the destination IP
last_hop_responded        bool      Set to ``True`` if the last hop was a response at all
========================  ========  ===================================================================================


.. _traceroute-hop:

Hop
----

Each hop in the traceroute is available as a ``Hop`` object.

=====================  =====  ================================================================
Property               Type   Explanation
=====================  =====  ================================================================
index                  int    The hop number, starting with 1
packets                list   A list of tracroute :ref:`traceroute-packet` objects
=====================  =====  ================================================================


.. _traceroute-packet:

Packet
------

=======================  ==========  ===========================================================================================
Property                 Type        Explanation
=======================  ==========  ===========================================================================================
origin                   str         The IP address of where the packet is coming from
rtt                      float
size                     int
ttl                      int
arrived_late_by          int         If the packet arrived late, this number represents "how many hops ago" this packet was sent
internal_ttl             int         The time-to-live for the packet that triggered the error ICMP.  The default is 1
destination_option_size  int         The size of the IPv6 destination option header
hop_by_hop_option_size   int         The size of the IPv6 hop-by-hop option header
icmp_header              IcmpHeader  See :ref:`traceroute-icmp-header` below
=======================  ==========  ===========================================================================================


.. _traceroute-icmp-header:

IcmpHeader
----------

This class is slightly different than other parts of Sagan as it in ``objects``
we find a complex generic list containing generic dictionaries pulled directly
from the JSON blob.  The decision not to further parse this bob into separate
Python models was made based on the assumption that much of this section is very
edge-case and the contents are present sporadically.

If however there is a demand for further development of this portion of the
result, we can expand it.  Until then though, ``IcmpHeader`` is a very simple
class, the majority of data living in ``objects``.

For further information about this portion of a traceroute result, you should
consult our `data structure documenttaion`_

.. _data structure documenttaion: https://atlas.ripe.net/docs/data_struct/#v4610_traceroute

=====================  ==========  =========================================================================
Property               Type        Explanation
=====================  ==========  =========================================================================
version                int         RFC4884 version
rfc4884                bool        ``True`` if length indication is present, ``False`` otherwise
objects                list        As mentioned above a complete dump of whatever is in the ``obj`` property
=====================  ==========  =========================================================================


.. _dns:

DNS
====

The most complicated result type, ``dns`` measurement results contain all of the
properties :ref:`common to all measurements <common-attributes>` as well as the following:


=====================  ========  ===================================================================================
Property               Type      Explanation
=====================  ========  ===================================================================================
responses              list      A list of DNS :ref:`dns-response` objects (see below)
=====================  ========  ===================================================================================


.. _dns-response:

Response
--------

Most DNS measurement results consist of a single response, but in some cases,
there may be more than one.  Regardless, every ``Response`` instance has the
following properties:

=====================  ========  ===================================================================================
Property               Type      Explanation
=====================  ========  ===================================================================================
raw_data               dict      The fragment of the initial JSON that pertains to this response
af                     int       The address family.  It's always either a ``4`` or a ``6``.
destination_address    str       An IP address represented as a string
source_address         str       An IP address represented as a string
protocol               str       One of ``TCP``, ``UDP``
abuf                   Message   See :ref:`dns-message` below
qbuf                   Message   See :ref:`dns-message` below
response_time          float     Time, in seconds until response was received
response_id            int       The sequence number of this result within a group of results, available if the resolution was done by the probe's local resolver
=====================  ========  ===================================================================================


.. _dns-message:

Message
-------

Responses can contain either an ``abuf`` or a ``qbuf`` which are both ``Message``
objects.  If you want the string representation, simply cast the object as a
string with ``str()``.

=====================  ========  ===================================================================================
Property               Type      Explanation
=====================  ========  ===================================================================================
raw_data               dict      The fragment of the initial JSON that pertains to this response
header                 Header    See :ref:`dns-header` below
edns0                  Edns0     See :ref:`dns-edns0` below, if any
questions              list      A list of :ref:`dns-question` objects
answers                list      A list of :ref:`dns-answer` objects
authorities            list      A list of :ref:`dns-authority` objects
additionals            list      A list of :ref:`dns-additional` objects, if any
=====================  ========  ===================================================================================

.. _dns-message-precalculatedvalues:

A note on pre-calculated values
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

By default, when you pass a result into Sagan, it will attempt to parse the
``abuf`` and ``qbuf`` strings (if any) into ``Message`` objects.  However, some
of the values in that abuf may have already been pre-calculated and stored
alongside the other attributes in the result.  Many ``Header`` values for
example, can be found in the raw result (outside of the abuf string), so parsing
the abuf for these values is redundant and potentially unnecessary if these
values are all you need.

For this case, Sagan supports passing ``parse_buf=False`` to the ``DnsResult``
class.  If you opt for this method, the abuf will not be parsed, and any values
not immediately available in the result will return ``None``.  For example::


    from ripe.atlas.sagan import DnsResult
    my_result = DnsResult(
        '<some result data including name, type, and rdata, but not ttl or class>',
        parse_buf=False
    )
    result.responses[0].abuf.answers[0].name       # "version.bind"
    result.responses[0].abuf.answers[0].klass      # None
    result.responses[0].abuf.answers[0].rd_length  # None
    result.responses[0].abuf.answers[0].type       # "TXT"
    result.responses[0].abuf.answers[0].ttl        # None
    result.responses[0].abuf.answers[0].data       # "Some RDATA value"

Note also that ``Result.get()`` accepts ``parse_buf=`` as well::

    from ripe.atlas.sagan import Result
    my_result = Result.get(
        '<some result data including name, type, and rdata, but not ttl or class>',
        parse_buf=False
    )
    result.responses[0].abuf.answers[0].name  # "version.bind"
    ...


.. _dns-header:

Header
~~~~~~

All of these properties conform to `RFC 1035`_, so we won't go into detail about
them here.

.. _RFC 1035: https://www.ietf.org/rfc/rfc1035.txt

=====================  ========  ===================================================================================
Property               Type      Explanation
=====================  ========  ===================================================================================
raw_data               dict      The portion of the parsed abuf that represents this section
aa                     bool
qr                     bool
nscount                int
qdcount                int
ancount                int
tc                     bool
rd                     bool
arcount                int
return_code            str
opcode                 str
ra                     bool
z                      int
id                     int
=====================  ========  ===================================================================================


.. _dns-question:

Question
~~~~~~~~

The question section of the response.

  **NOTE**: In keeping with Python conventions, we use the propertyname
  ``klass`` here instead of the more intuitive (and illegal in Python)
  ``class``.  It may be confusing for non-Python programmers, but unfortunately
  it's a limitation of the language.

=====================  ========  ===================================================================================
Property               Type      Explanation
=====================  ========  ===================================================================================
raw_data               dict      The portion of the parsed abuf that represents this section
klass                  str       The ``CLASS`` value, spelt this way to conform to Python norms
type                   str
name                   str
=====================  ========  ===================================================================================


.. _dns-answer:

Answer
~~~~~~

The answer section of the response.

  **NOTE**: In keeping with Python conventions, we use the propertyname
  ``klass`` here instead of the more intuitive (and illegal in Python)
  ``class``.  It may be confusing for non-Python programmers, but unfortunately
  it's a limitation of the language.

=====================  ========  ===================================================================================
Property               Type      Explanation
=====================  ========  ===================================================================================
raw_data               dict      The portion of the parsed abuf that represents this section
klass                  str       The ``CLASS`` value, spelt this way to conform to Python norms
type                   str
name                   str
ttl                    int
address                str       An IP address
rd_length              int
=====================  ========  ===================================================================================


.. _dns-authority:

Authority
~~~~~~~~~

The authority section of the response.

  **NOTE**: In keeping with Python conventions, we use the propertyname
  ``klass`` here instead of the more intuitive (and illegal in Python)
  ``class``.  It may be confusing for non-Python programmers, but unfortunately
  it's a limitation of the language.

=====================  ========  ===================================================================================
Property               Type      Explanation
=====================  ========  ===================================================================================
raw_data               dict      The portion of the parsed abuf that represents this section
klass                  str       The ``CLASS`` value, spelt this way to conform to Python norms
type                   str
name                   str
ttl                    int
target                 str       An IP address
rd_length              int
=====================  ========  ===================================================================================


.. _dns-additional:

Additional
~~~~~~~~~~

The optional additional section of the response.

  **NOTE**: In keeping with Python conventions, we use the propertyname
  ``klass`` here instead of the more intuitive (and illegal in Python)
  ``class``.  It may be confusing for non-Python programmers, but unfortunately
  it's a limitation of the language.

=====================  ========  ===================================================================================
Property               Type      Explanation
=====================  ========  ===================================================================================
raw_data               dict      The portion of the parsed abuf that represents this section
klass                  str       The ``CLASS`` value, spelt this way to conform to Python norms
type                   str
name                   str
ttl                    int
address                str       An IP address
rd_length              int
=====================  ========  ===================================================================================


.. _dns-edns0:

EDNS0
~~~~~

The optional EDNS0 section of the response.

=====================  ========  ===================================================================================
Property               Type      Explanation
=====================  ========  ===================================================================================
raw_data               dict      The portion of the parsed abuf that represents this section
extended_return_code   int
name                   str
type                   str
udp_size               int
version                int
z                      int
options                list      A list of :ref:`dns-edns0-option` objects
=====================  ========  ===================================================================================


.. _dns-edns0-option:

Option
......

=====================  ========  ===================================================================================
Property               Type      Explanation
=====================  ========  ===================================================================================
raw_data               dict      The portion of the EDNS0 section that represents this option
nsid                   str
code                   int
length                 int
name                   str
=====================  ========  ===================================================================================


.. _sslcert:

SSL Certificate
===============

SSL certificate measurement results contain all of the properties
:ref:`common to all measurements <common-attributes>` as well as the following:

=====================  ========  ===================================================================================
Property               Type      Explanation
=====================  ========  ===================================================================================
af                     int       The address family.  It's always either a ``4`` or a ``6``.
destination_name       str       The string initially given as the target.  It can be an IP address or a domain name
destination_address    str       An IP address
source_address         str       An IP address
port                   int       The port numer
method                 str       This should always be "SSL"
version                str
response_time          float     Time, in seconds until response was received
time_to_connect        float     Time, in seconds until the connection was established
certificates           list      A list of :ref:`sslcert-certificate` objects
is_signed              bool      Set to ``True`` if the certificate is self-signed
checksum_chain         str       A list of all checksums for all certificates in this result, joined with the arbitrary string ``::``.  This can come in handy when you're trying to compare checksums of multiple results.
=====================  ========  ===================================================================================

.. _sslcert-certificate:

Certificate
-----------

Each SSL certificate measurement result can contain multiple ``Certificate`` objects.

=====================  ========  ===================================================================================
Property               Type      Explanation
=====================  ========  ===================================================================================
raw_data               dict      The fragment of the initial JSON that pertains to this response
subject_cn             str       The subject's common name
subject_o              str       The subject's organisation
subject_c              str       The subject's country
issuer_cn              str       The issuer's common name
issuer_o               str       The issuer's organisation
issuer_c               str       The issuer's country
valid_from             datetime
valid_until            datetime
checksum_md5           str       The md5 checksum
checksum_sha1          str       The sha1 checksum
checksum_sha256        str       The sha256 checksum
has_expired            bool      Set to ``True`` if the certificate is no longer valid
=====================  ========  ===================================================================================


.. _http:

HTTP
====

HTTP measurement results contain all of the properties
:ref:`common to all measurements <common-attributes>` as well as the following:

=====================  ========  ===================================================================================
Property               Type      Explanation
=====================  ========  ===================================================================================
uri                    str
method                 str       The HTTP method
responses              list      A list of :ref:`http-response` objects
=====================  ========  ===================================================================================


.. _http-response:

Response
--------

Each HTTP measurement result can contain multiple ``Response`` objects.

=====================  ========  ===================================================================================
Property               Type      Explanation
=====================  ========  ===================================================================================
raw_data               dict      The portion of the JSON that pertains to this response
af                     int       The address family.  It's always either a ``4`` or a ``6``.
body_size              int       The total number of bytes in the body
head_size              int       The total number of bytes in the head
destination_address    str       An IP address
source_address         str       An IP address
code                   int       The HTTP response code
response_time          float     Time, in seconds until response was received
version                str       The HTTP version
=====================  ========  ===================================================================================


.. _ntp:

NTP
====

NTP measurement results contain all of the properties
:ref:`common to all measurements <common-attributes>` as well as the following:

=====================  ========  ===================================================================================
Property               Type      Explanation
=====================  ========  ===================================================================================
leap_second_indicator  str       Leap second indicator
poll                   int       Poll interval
precision              float
protocol               str       ``UDP``
reference_id           str       Reference id returned by server
reference_time         float     The NTP time the server last contacted the reference time source
root_delay             float     Round trip time from the server to the reference time source
root_dispersion        float     Accuracy of server's clock
stratum                int       How far in hops is server from reference time source
version                int       The NTP version
mode                   str       Ntp communication mode. Usually ``server``
rtt_median             float     The median value of packets' rtt
offset_median          float     The median value of the packets' offset
packets                list      A list of ntp :ref:`ntp-packet` objects
=====================  ========  ===================================================================================


.. _ntp-packet:

Response
--------

Each HTTP measurement result can contain multiple ``Response`` objects.

========================  ========  ===================================================================================
Property                  Type      Explanation
========================  ========  ===================================================================================
raw_data                  dict      The portion of the JSON that pertains to this response
offset                    float     The NTP offset
rtt                       float     The response time
final_timestamp           float     A full-precision Unix timestamp for when the NTP client received the response
origin_timestamp          float     A full-precision Unix timestamp for when the NTP client send packet to the server
received_timestamp        float     A full-precision Unix timestamp for when the NTP server received the request
transmitted_timestamp     float     A full-precision Unix timestamp for when the NTP server transmitted the response
final_time                datetime  A Python datetime object with limited precision[1] based on ``final_timestamp``
origin_time               datetime  A Python datetime object with limited precision[1] based on ``origin_timestamp``
received_time             datetime  A Python datetime object with limited precision[1] based on ``received_timestamp``
transmitted_time          datetime  A Python datetime object with limited precision[1] based on ``transmitted_timestamp``
========================  ========  ===================================================================================

.. [1] Python ``datetime`` objects are limited to 6 decimal places of precision.
