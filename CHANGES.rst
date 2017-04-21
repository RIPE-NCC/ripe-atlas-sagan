Changelog
=========
* 1.2
    * Replaced pyOpenSSL with cryptography
    * Added parsing of subjectAltName X509 extension
* 1.1.11
    * Added first version of WiFi results    
* 1.1.10
    * Added a `parse_all_hops` kwarg to the Traceroute class to tell Sagan to stop parsing Hops and Packets once we have all of the last hop statistics (default=True)
    * Remove dependency on IPy: we were using it for IPv6 canonicalization, but all IPv6 addresses in results should be in canonical form to start with.
* 1.1.9
    * Removed the `parse_abuf` script because no one was using it and its
      Python3 support was suspect anyway.
* 1.1.8
    * Handle case where a traceroute result might not have ``dst_addr`` field.
* 1.1.7
    * Change condition of traceroute's ``last_hop_responded`` flag.
    * Add couple of more traceroute's properties. ``is_success`` and ``last_hop_errors``.
    * Add tests to the package itself.
* 1.1.6
    * Fix for `Issue #56`_ a case where the ``qbuf`` value wasn't being properly
      captured.
    * Fixed small bug that didn't accurately capture the ``DO`` property from
      the qbuf.
* 1.1.5
    * We now ignore so-called "late" packets in traceroute results.  This will
      likely be amended later as future probe firmwares are expected to make
      better use of this value, but until then, Sagan will treat these packets
      as invalid.
* 1.1.4
    * Added a ``type`` attribute to all ``Result`` subclasses
    * Added support for a lot of new DNS answer types, including ``NSEC``,
      ``PTR``, ``SRV``, and more.  These answers do not yet have a complete
      string representation however.
* 1.1.3
    * Changed the name of ``TracerouteResult.rtt_median`` to
      ``TracerouteResult.last_rtt_median``.
    * Modified the ``DnsResult`` class to allow the "bubbling up" of error
      statuses.
* 1.1.2
    * We skipped this number for some reason :-/
* 1.1.1
    * Fixed a `string representation bug`_ found by `iortiz`_
* 1.1.0
    * **Breaking Change**: the ``Authority`` and ``Additional`` classes were
      removed, replaced with the appropriate answer types.  For the most part,
      this change should be invisible, as the common properties are the same,
      but if you were testing code against these class types, you should
      consider this a breaking change.
    * **Breaking Change**: The ``__str__`` format for DNS ``RrsigAnswer`` to
      conform the output of a typical ``dig`` binary.
    * Added ``__str__`` definitions to DNS answer classes for use with the
      toolkit.
    * In an effort to make Sagan (along with Cousteau and the toolkit) more
      portable, we dropped the requirement for the ``arrow`` package.
* 1.0.0
    * 1.0! w00t!
    * **Breaking Change**: the ``data`` property of the ``TxtAnswer`` class was
      changed from a string to a list of strings.  This is a correction from
      our own past deviation from the RFC, so we thought it best to conform as
      part of the move to 1.0.0
    * Fixed a bug where non-ascii characters in DNS TXT answers resulted in an
      exception.
* 0.8.2
    * Fixed a bug related to non-ascii characters in SSL certificate data.
    * Added a wrapper for json loaders to handle differences between ujson and
      the default json module.
* 0.8.1
    * Minor fix to make all ``Result`` objects properly JSON serialisable.
* 0.8.0
    * Added `iortiz`_'s patch for flags and ``flags``
      and ``sections`` properties on DNS ``Answer`` objects.
* 0.7.1
    * Changed ``README.md`` to ``README.rst`` to play nice with pypi.
* 0.7
    * Added `pierky`_'s new ``RRSigAnswer`` class to
      the dns parser.
* 0.6.3
    * Fixed a bug in how Sagan deals with inappropriate firmware versions
* 0.6.2
    * Added `pierky`_'s fix to fix AD and CD flags
      parsing in DNS Header
* 0.6.1
    * Added ``rtt_min``, ``rtt_max``, ``offset_min``, and ``offset_max`` to
      ``NTPResult``
* 0.6.0
    * Support for NTP measurements
    * Fixes for how we calculate median values
    * Smarter setup.py
* 0.5.0
    * Complete Python3 support!
* 0.4.0
    * Added better Python3 support.  Tests all pass now for ping, traceroute,
      ssl, and http measurements.
    * Modified traceroute results to make use of ``destination_ip_responded``
      and ``last_hop_responded``, deprecating ``target_responded``.  See the
      docs for details.
* 0.3.0
    * Added support for making use of some of the pre-calculated values in DNS
      measurements so you don't have to parse the abuf if you don't need it.
    * Fixed a bug in the abuf parser where a variable was being referenced by
      never defined.
    * Cleaned up some of the abuf parser to better conform to pep8.
* 0.2.8
    * Fixed a bug where DNS ``TXT`` results with class ``IN`` were missing a
      ``.data`` value.
    * Fixed a problem in the SSL unit tests where ``\n`` was being
      misinterpreted.
* 0.2.7
    * Made abuf more robust in dealing with truncation.
* 0.2.6
    * Replaced ``SslResult.get_checksum_chain()`` with the
      ``SslResult.checksum_chain`` property.
    * Added support for catching results with an ``err`` property as an actual
      error.
* 0.2.5
    * Fixed a bug in how the ``on_error`` and ``on_malformation`` preferences
      weren't being passed down into the subcomponents of the results.
* 0.2.4
    * Support for ``seconds_since_sync`` across all measurement types
* 0.2.3
    * "Treat a missing Type value in a DNS result as a malformation" (Issue #36)
* 0.2.2
    * Minor bugfixes
* 0.2.1
    * Added a ``median_rtt`` value to traceroute ``Hop`` objects.
    * Smarter and more consistent error handling in traceroute and HTTP
      results.
    * Added an ``error_message`` property to all objects that is set to ``None``
      by default.
* 0.2.0
    * Totally reworked error and malformation handling.  We now differentiate
      between a result (or portion thereof) being malformed (and therefore
      unparsable) and simply containing an error such as a timeout.  Look for
      an ``is_error`` property or an ``is_malformed`` property on every object
      to check for it, or simply pass ``on_malformation=Result.ACTION_FAIL`` if
      you'd prefer things to explode with an exception.  See the documentation
      for more details
    * Added lazy-loading features for parsing abuf and qbuf values out of DNS
      results.
    * Removed the deprecated properties from ``dns.Response``.  You must now
      access values like ``edns0`` from ``dns.Response.abuf.edns0``.
    * More edge cases have been found and accommodated.
* 0.1.15
    * Added a bunch of abuf parsing features from
      `b4ldr`_ with some help from
      `phicoh`_.
* 0.1.14
    * Fixed the deprecation warnings in ``DnsResult`` to point to the right
      place.
* 0.1.13
    * Better handling of ``DNSResult`` errors
    * Rearranged the way abufs were handled in the ``DnsResult`` class to make
      way for ``qbuf`` values as well.  The old method of accessing ``header``,
      ``answers``, ``questions``, etc is still available via ``Response``, but
      this will go away when we move to 0.2.  Deprecation warnings are in place.
* 0.1.12
    * Smarter code for checking whether the target was reached in
      ``TracerouteResults``.
    * We now handle the ``destination_option_size`` and
      ``hop_by_hop_option_size`` values in ``TracerouteResult``.
    * Extended support for ICMP header info in traceroute ``Hop`` class by
      introducing a new ``IcmpHeader`` class.
* 0.1.8
    * Broader support for SSL checksums.  We now make use of ``md5`` and
      ``sha1``, as well as the original ``sha256``.

.. _Issue #56: https://github.com/RIPE-NCC/ripe.atlas.sagan/issues/56
.. _string representation bug: https://github.com/RIPE-NCC/ripe-atlas-tools/issues/1
.. _b4ldr: https://github.com/b4ldr
.. _phicoh: https://github.com/phicoh
.. _iortiz: https://github.com/iortiz
.. _pierky: https://github.com/pierky
