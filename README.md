# RIPE Atlas Sagan

A parsing library for RIPE Atlas measurement results


## Why this exists

RIPE Atlas generates a **lot** of data, and the format of that data changes over
time.  Often you want to do something simple like fetch the median RTT for each
measurement result between date `X` and date `Y`.  Unfortunately, there are are
dozens of edge cases to account for while parsing the JSON, like the format of
errors and firmware upgrades that changed the format entirely.

To make this easier for our users (and for ourselves), we wrote an easy to use
parser that's smart enough to figure out the best course of action for each
result, and return to you a useful, native Python object.


## Changelog

* 0.1.13
    * Better handling of `DNSResult` errors
    * Rearranged the way abufs were handled in the `DnsResult` class to make way
    for `qbuf` values as well.  The old method of accessing `header`, `answers`,
    `questions`, etc is still available via `Response`, but this will go away
    when we move to 0.2.  Deprecation warnings are in place.
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


## How to use it

You can parse a result in a few ways.  You can just pass the JSON-encoded
string:

```python
from ripe.atlas.sagan import PingResult

my_result = PingResult("<result string from RIPE Atlas ping measurement>")

print(my_result.rtt_median)
123.456

print(my_result.af)
6
```

You can do the JSON-decoding yourself:

```python
from ripe.atlas.sagan import PingResult

my_result = PingResult(
    json.dumps("<result string from RIPE Atlas ping measurement>")
)

print(my_result.rtt_median)
123.456

print(my_result.af)
6
```

You can let the parser guess the right type for you, though this incurs a
small performance penalty:

```python
from ripe.atlas.sagan import Result

my_result = Result.get("<result string from RIPE Atlas ping measurement>")

print(my_result.rtt_median)
123.456

print(my_result.af)
6
```


### Which attributes are supported?

Every result type has its own properties, with a few common between all types.

Specifically, these attributes exist on all `*Result` objects:

* `created`  An arrow object (like datetime, but better) of the `timestamp` field
* `measurement_id`
* `probe_id`
* `firmware` An integer representing the firmware version
* `origin`  The `from` attribute in the result
* `is_error` Set to `True` if an error was found

Additionally, each of the result types have their own properties, like
`packet_size`, `responses`, `certificates`, etc.  You can take a look at the
classes themselves, or just look at the tests if you're curious.  But to get you
started, here are some examples:

```python
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
```


### "But... I'd rather my code explode when there's an error"

If you'd like Sagan to be less forgiving, you only need to pass
`on_error=Result.ERROR_FAIL` when you're instantiating your object.  To use one
of our previous examples:

```python
from ripe.atlas.sagan import Result

my_result = Result.get(
    '{"dnserr":"non-recoverable failure in name resolution",...}',
    on_error=Result.ERROR_FAIL
)
```

The above will explode with a `ResultParseError`.


## What it supports

Essentially, we tried to support everything.  If you pass in a DNS result
string, the parser will return a `DNSResult` object, which contains a list of
`Response`s, each with an `abuf` property, as well as all of the information in
that abuf: header, question, answer, etc.

```python
from ripe.atlas.sagan import DnsResult

my_dns_result = DnsResult("<result string from a RIPE Atlas DNS measurement>")
my_dns_result.responses[0].abuf  # The entire string
my_dns_result.responses[0].header.arcount  # Decoded from the abuf
```

We do the same sort of thing for SSL measurements, traceroutes, everything.  We
try to save you the effort of sorting through whatever is in the result.


## What it requires

As you might have guessed, with all of this magic going on under the hood, there
are a few dependencies:

* [arrow](https://pypi.python.org/pypi/arrow)
* dnspython [v2](https://pypi.python.org/pypi/dnspython) or [v3](https://pypi.python.org/pypi/dnspython3)
* [pyOpenSSL](https://pypi.python.org/pypi/pyOpenSSL)
* [python-dateutil](https://pypi.python.org/pypi/python-dateutil)
* [pytz](https://pypi.python.org/pypi/pytz)
* [IPy](https://pypi.python.org/pypi/IPy/)

Additionally, we recommend that you also install
[ujson](https://pypi.python.org/pypi/ujson) as it will speed up the
JSON-decoding step considerably, and [sphinx](https://pypi.python.org/pypi/Sphinx) if you intend to build the
documentation files for offline use.


## How to install

The stable version should always be in PyPi, so you can install it with `pip`:

```bash
$ pip install ripe.atlas.sagan
```


### Troubleshooting

Some setups (like MacOS) have trouble with some of the dependencies we're
using, so if they explode during the installation, you can still make use of
*some* of the parsers by deliberately excluding the problematic ones at
install time.

For example, if you want to skip the installation of `pyOpenSSL` (required for
parsing SSL certificate results), you can do this:

```bash
$ SAGAN_WITHOUT_SSL=1 pip install ripe.atlas.sagan
```

Similarly, you can skip the installation of `dnspython` and forego any DNS
result parsing:

```bash
$ SAGAN_WITHOUT_DNS=1 pip install ripe.atlas.sagan
```


## Further Documentation

Complete documentation can always be found on
[the RIPE Atlas project page](https://atlas.ripe.net/docs/sagan/), and if you're
not online, the project itself contains a `docs` directory -- everything you
should need is in there.


## Colophon

But why *Sagan*?  The RIPE Atlas team decided to name all of its modules after
explorers, and what better name for a parser than that of the man who spent
decades reaching out to the public about the wonders of the cosmos?

