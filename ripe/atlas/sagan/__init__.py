from __future__ import absolute_import

from .base import Result, ResultParseError
from .dns import DnsResult
from .http import HttpResult
from .ping import PingResult
from .ssl import SslResult
from .traceroute import TracerouteResult

def get_version():
    with open("version.txt") as f:
        return f.read()


version = get_version()

__all__ = (
    "Result",
    "PingResult",
    "TracerouteResult",
    "DnsResult",
    "SslResult",
    "HttpResult"
)
