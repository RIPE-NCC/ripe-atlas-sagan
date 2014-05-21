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
is_error               bool      Whether or not there were errors in parsing/handling this result
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
seconds_since_sync     int    The number of seconds since the probe last syncronised its clock
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

=====================  ========  ===================================================================================
Property               Type      Explanation
=====================  ========  ===================================================================================
af                     int       The address family.  It's always either a ``4`` or a ``6``.
destination_name       str       The string initially given as the target.  It can be an IP address or a domain name
destination_address    str       An IP address represented as a string
source_address         str       An IP address represented as a string
end_time               datetime  The time at which the traceroute finished
end_time_timestamp     int       A Unix timestamp for the ``end_time`` attribute
paris_id               int
size                   int       The packet size
protocol               str       One of ``ICMP``, ``TCP``, ``UDP``
hops                   list      A list of :ref:`traceroute-hop` objects
total_hops             int       The total number of hops
last_rtt               float     The RTT from the last successful hop
target_responded       bool      Set to ``True`` if the target actually responded
=====================  ========  ===================================================================================


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
error                    str         The error message, if any
arrived_late_by          int         If the packet arrived late, this number represents "how many hops ago" this packet was sent
internal_ttl             int         The time-to-live for the packet that triggered the error ICMP.  The default is 1
destination_option_size  int         The size of the IPv6 destination option header
hop_by_hop_option_size   int         The size of the IPv6 hop-by-hop option header
icmp_header              IcmpHeader  See :ref:`traceroute-icmp-header` below
=======================  ==========  ===========================================================================================


.. _traceroute-icmp-header

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
abuf                   str       The raw, unparsed abuf string
response_time          float     Time, in seconds until response was received
response_id            int       The sequence number of this result within a group of results, available if the resolution was done by the probe's local resolver
header                 Header    See :ref:`dns-header` below
edns0                  Edns0     See :ref:`dns-edns0` below, if any
questions              list      a list of :ref:`dns-question` objects
answers                list      a list of :ref:`dns-answer` objects
authorities            list      a list of :ref:`dns-authority` objects
additionals            list      a list of :ref:`dns-additional` objects, if any
=====================  ========  ===================================================================================


.. _dns-header:

Header
------

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
--------

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
------

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
answer                 str       Text representation of the annswer
rd_length              int
=====================  ========  ===================================================================================


.. _dns-authority:

Authority
---------

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
----------

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
-----

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
------

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
=====================  ========  ===================================================================================

.. _sslcert-methods:

Methods
-------


.. _sslcert-methods-get_checksum_chain:

get_checksum_chain()
....................

This method can come in handy when you're trying to compare checksums of
multiple results.  It returns a list of all checksums for all certificates
in this result, joined with the arbitrary string ``::``.

Example:::

    my_result = SslResult('<JSON data>')
    print(my_result.get_checksum_chan())


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
is_error               bool      If an error message is supplied, this will be ``True``
error_string           str       An error message, if any
=====================  ========  ===================================================================================

