from __future__ import absolute_import

import os

from .base import Result, ResultParseError
from .dns import DnsResult
from .http import HttpResult
from .ping import PingResult
from .ssl import SslResult
from .traceroute import TracerouteResult

def get_version():
    version_file = os.path.join(
        os.path.dirname(__file__),
        "version"
    )
    with open(version_file) as f:
        return f.read().strip()


version = get_version()

__all__ = (
    "Result",
    "PingResult",
    "TracerouteResult",
    "DnsResult",
    "SslResult",
    "HttpResult",
    "version",
)

