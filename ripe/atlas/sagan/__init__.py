from __future__ import absolute_import

from .base import Result, ResultParseError
from .dns import DnsResult
from .http import HttpResult
from .ping import PingResult
from .ssl import SslResult
from .traceroute import TracerouteResult

__version__ = "0.4a"

__all__ = (
    "Result",
    "PingResult",
    "TracerouteResult",
    "DnsResult",
    "SslResult",
    "HttpResult"
)
