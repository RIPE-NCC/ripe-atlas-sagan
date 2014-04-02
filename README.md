# Sagan

The RIPE Atlas results parser


## Why this exists

RIPE Atlas generates a **lot** of data, and the format of that data changes over
time.  Often you want to do something simple like fetch the median RTT for each
measurement result between date `X` and date `Y`.  Unfortunately, there are are
dozens of edge cases to account for while parsing the JSON, like the format of
errors and firmware upgrades that changed the format entirely.

To make this easier for our users (and for ourselves), we wrote an easy to use
parser that's smart enough to figure out the best course of action for each
result, and return to you a useful, native Python object.


## How to use it

You can parse a result in a few ways.  You can just pass the JSON-encoded
string:

```python
my_result = PingResult("<result string from RIPE Atlas ping measurement>")
print(my_result.rtt_median)
123.456
print(my_result.af)
6
```

You can do the JSON-decoding yourself:

```python
my_result = PingResult(
    json.dumps("<result string from RIPE Atlas ping measurement>")
)
print(my_result.rtt_median)
123.456
print(my_result.af)
6
```

And you can let the parser guess the right type for you:

```python
my_result = Result.get("<result string from RIPE Atlas ping measurement>")
print(my_result.rtt_median)
123.456
print(my_result.af)
6
```


## What it supports

Essentially, we tried to support everything.  If you pass in a DNS result
string, the parser will return a `DNSResult` object, which contains a list of
`Response`s, each with an `abuf` property, as well as all of the information in
that abuf: header, question, answer, etc.

```python
my_dns_result = DnsResult("<result string from a RIPE Atlas DNS measurement>")
my_dns_result.abuf  # The entire string
my_dns_result.responses[0].header.arcount  # Decoded from the abuf
```

We do the same sort of thing for SSL measurements, traceroutes, everything.  We
try to save you the effort of sorting through whatever is in the result.


## What it requires

As you might have guessed, with all of this magic going on under the hood, there
are a few dependencies:

* arrow
* dnspython
* pyOpenSSL
* python-dateutil
* pytz

Additionally, we recommend that you also install `ujson` as it will speed up the
JSON-decoding step considerably.


## How to install

```bash
$ pip install ripe.atlas.sagan
```


## Colophon

But why *Sagan*?  The RIPE Atlas team decided to name all of its modules after
explorers, and what better name for a parser than that of the man who spent
decades reaching out to the public about the wonders of the cosmos?

