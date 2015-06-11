# Changelog

* 0.8.1
    * Minor fix to make all `Result` objects properly JSON serialisable.
* 0.8.0
    * Added [iortiz](https://github.com/iortiz)'s patch for flags and `flags`
      and `sections` properties on DNS `Answer` objects.
* 0.7.1
    * Changed `README.md` to `README.rst` to play nice with pypi.
* 0.7
    * Added [pierky](https://github.com/pierky)'s new `RRSigAnswer` class to
      the dns parser.
* 0.6.3
    * Fixed a bug in how Sagan deals with inappropriate firmware versions
* 0.6.2
    * Added [pierky](https://github.com/pierky)'s fix to fix AD and CD flags
      parsing in DNS Header
* 0.6.1
    * Added `rtt_min`, `rtt_max`, `offset_min`, and `offset_max` to `NTPResult`
* 0.6.0
    * Support for NTP measurements
    * Fixes for how we calculate median values
    * Smarter setup.py
* 0.5.0
    * Complete Python3 support!
* 0.4.0
    * Added better Python3 support.  Tests all pass now for ping, traceroute,
      ssl, and http measurements.
    * Modified traceroute results to make use of `destination_ip_responded` and
      `last_hop_responded`, deprecating `target_responded`.  See the docs for
      details.
* 0.3.0
    * Added support for making use of some of the pre-calculated values in DNS
      measurements so you don't have to parse the abuf if you don't need it.
    * Fixed a bug in the abuf parser where a variable was being referenced by
      never defined.
    * Cleaned up some of the abuf parser to better conform to pep8.
* 0.2.8
    * Fixed a bug where DNS `TXT` results with class `IN` were missing a
      `.data` value.
    * Fixed a problem in the SSL unit tests where `\n` was being
      misinterpreted.
* 0.2.7
    * Made abuf more robust in dealing with truncation.
* 0.2.6
    * Replaced `SslResult.get_checksum_chain()` with the
      `SslResult.checksum_chain` property.
    * Added support for catching results with an `err` property as an actual
      error.
* 0.2.5
    * Fixed a bug in how the `on_error` and `on_malformation` preferences
      weren't being passed down into the subcomponents of the results.
* 0.2.4
    * Support for `seconds_since_sync` across all measurement types
* 0.2.3
    * "Treat a missing Type value in a DNS result as a malformation" (Issue #36)
* 0.2.2
    * Minor bugfixes
* 0.2.1
    * Added a `median_rtt` value to traceroute ``Hop`` objects.
    * Smarter and more consistent error handling in traceroute and HTTP
      results.
    * Added an `error_message` property to all objects that is set to `None`
      by default.
* 0.2.0
    * Totally reworked error and malformation handling.  We now differentiate
      between a result (or portion thereof) being malformed (and therefore
      unparsable) and simply containing an error such as a timeout.  Look for
      an `is_error` property or an `is_malformed` property on every object
      to check for it, or simply pass `on_malformation=Result.ACTION_FAIL` if
      you'd prefer things to explode with an exception.  See the documentation
      for more details
    * Added lazy-loading features for parsing abuf and qbuf values out of DNS
      results.
    * Removed the deprecated properties from `dns.Response`.  You must now
      access values like `edns0` from `dns.Response.abuf.edns0`.
    * More edge cases have been found and accommodated.
* 0.1.15
    * Added a bunch of abuf parsing features from
      [b4ldr](https://github.com/b4ldr) with some help from
      [phicoh](https://github.com/phicoh).
* 0.1.14
    * Fixed the deprecation warnings in `DnsResult` to point to the right
      place.
* 0.1.13
    * Better handling of `DNSResult` errors
    * Rearranged the way abufs were handled in the `DnsResult` class to make
      way for `qbuf` values as well.  The old method of accessing `header`,
      `answers`, `questions`, etc is still available via `Response`, but this
      will go away when we move to 0.2.  Deprecation warnings are in place.
* 0.1.12
    * Smarter code for checking whether the target was reached in
      `TracerouteResults`.
    * We now handle the `destination_option_size` and `hop_by_hop_option_size`
      values in `TracerouteResult`.
    * Extended support for ICMP header info in traceroute `Hop` class by
      introducing a new `IcmpHeader` class.
* 0.1.8
    * Broader support for SSL checksums.  We now make use of `md5` and `sha1`,
      as well as the original `sha256`.
