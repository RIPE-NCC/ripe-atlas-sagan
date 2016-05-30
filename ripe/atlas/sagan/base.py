# Copyright (c) 2016 RIPE NCC
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import logging
import pytz

from calendar import timegm
from datetime import datetime

from .helpers.compatibility import string

# Try to use ujson if it's available
try:
    import ujson as json
except ImportError:
    import json


class ResultParseError(Exception):
    pass


class ResultError(Exception):
    pass


class Json(object):
    """
    ujson, while impressive, is not a drop-in replacement for json as it doesn't
    respect the various keyword arguments permitted in the default json parser.
    As a workaround for this, we have our own class that defines its own
    .loads() method, so we can check for whichever we're using and adjust the
    arguments accordingly.
    """

    @staticmethod
    def loads(*args, **kwargs):
        try:
            if json.__name__ == "ujson":
                return json.loads(*args, **kwargs)
            return json.loads(strict=False, *args, **kwargs)
        except ValueError:
            raise ResultParseError("The JSON result could not be parsed")


class ParsingDict(object):
    """
    A handy container for methods we use for validation in the various result
    classes.

    Note that Python 2.x and 3.x handle the creation of dictionary-like objects
    differently.  If we write it this way, it works for both.
    """

    ACTION_IGNORE = 1
    ACTION_WARN = 2
    ACTION_FAIL = 3

    PROTOCOL_ICMP = "ICMP"
    PROTOCOL_UDP = "UDP"
    PROTOCOL_TCP = "TCP"
    PROTOCOL_MAP = {
        "ICMP": PROTOCOL_ICMP,
        "I":    PROTOCOL_ICMP,
        "UDP":  PROTOCOL_UDP,
        "U":    PROTOCOL_UDP,
        "TCP":  PROTOCOL_TCP,
        "T":    PROTOCOL_TCP,
    }

    def __init__(self, **kwargs):

        self._on_error = kwargs.pop("on_error", self.ACTION_WARN)
        self.is_error = False
        self.error_message = None

        self._on_malformation = kwargs.pop("on_malformation", self.ACTION_WARN)
        self.is_malformed = False

    def __nonzero__(self):
        # If we don't define this, Python ends up calling keys()
        # via __len__()  whenever we evaluate the object as a bool.
        return True

    def __len__(self):
        return len(self.keys())

    def __iter__(self):
        for key in self.keys():
            yield getattr(self, key)

    def __getitem__(self, key):
        return getattr(self, key)

    def __setitem__(self, key, item):
        setattr(self, key, item)

    def keys(self):
        return [p for p in dir(self) if self._is_property_name(p)]

    def ensure(self, key, kind, default=None):
        try:
            if kind == "datetime":
                return datetime.fromtimestamp(
                    self.raw_data[key], tz=pytz.UTC)
            return kind(self.raw_data[key])
        except (TypeError, ValueError, KeyError):
            return default

    def clean_protocol(self, protocol):
        """
        A lot of measurement types make use of a protocol value, so we handle
        that here.
        """
        if protocol is not None:
            try:
                return self.PROTOCOL_MAP[protocol]
            except KeyError:
                self._handle_malformation(
                    '"{protocol}" is not a recognised protocol'.format(
                        protocol=protocol
                    )
                )

    def _handle_malformation(self, message):
        if self._on_malformation == self.ACTION_FAIL:
            raise ResultParseError(message)
        elif self._on_malformation == self.ACTION_WARN:
            logging.warning(message)
        self.is_malformed = True

    def _handle_error(self, message):
        if self._on_error == self.ACTION_FAIL:
            raise ResultError(message)
        elif self._on_error == self.ACTION_WARN:
            logging.warning(message)
        self.is_error = True
        self.error_message = message

    def _is_property_name(self, p):
        if not p.startswith("_"):
            if p not in ("keys",):
                if not p.upper() == p:
                    if not callable(getattr(self, p)):
                        return True
        return False


class Result(ParsingDict):
    """
    The parent class for all measurement result classes.  Subclass this to
    handle parsing a new measurement type, or use .get() to let this class
    figure out the type for you.
    """

    def __init__(self, data, *args, **kwargs):

        ParsingDict.__init__(self, **kwargs)

        self.raw_data = data
        if isinstance(data, string):
            self.raw_data = Json.loads(data)

        for key in ("timestamp", "msm_id", "prb_id", "fw", "type"):
            if key not in self.raw_data:
                raise ResultParseError(
                    "This doesn't look like a RIPE Atlas measurement: {}".format(
                        self.raw_data
                    )
                )

        self.created = datetime.fromtimestamp(
            self.raw_data["timestamp"], tz=pytz.UTC)

        self.measurement_id = self.ensure("msm_id", int)
        self.probe_id = self.ensure("prb_id", int)
        self.firmware = self.ensure("fw", int)
        self.origin = self.ensure("from", str)
        self.seconds_since_sync = self.ensure("lts", int)
        self.group_id = self.ensure("group_id", int)
        self.bundle = self.ensure("bundle", int)

        # Handle the weird case where fw=0 and we don't know what to expect
        if self.firmware == 0:
            self._handle_malformation("Unknown firmware: {fw}".format(
                fw=self.firmware)
            )

        if self.seconds_since_sync is not None:
            if self.seconds_since_sync < 0:
                self.seconds_since_sync = None

        if "dnserr" in self.raw_data:
            self._handle_error(self.raw_data["dnserr"])

        if "err" in self.raw_data:
            self._handle_error(self.raw_data["err"])

    def __repr__(self):
        return "Measurement #{measurement}, Probe #{probe}".format(
            measurement=self.measurement_id,
            probe=self.probe_id
        )

    @property
    def created_timestamp(self):
        return timegm(self.created.timetuple())

    @classmethod
    def get(cls, data, **kwargs):
        """
        Call this when you have a JSON result and just want to turn it into the
        appropriate Result subclass.  This is less performant than calling
        PingResult(json_string) directly however, as the JSON has to be parsed
        first to find the type.
        """

        raw_data = data
        if isinstance(data, string):
            raw_data = Json.loads(data)

        try:
            kind = raw_data["type"].lower()
        except KeyError:
            raise ResultParseError("No type value was found in the JSON input")

        if kind == "ping":
            from .ping import PingResult
            return PingResult(raw_data, **kwargs)
        elif kind == "traceroute":
            from .traceroute import TracerouteResult
            return TracerouteResult(raw_data, **kwargs)
        elif kind == "dns":
            from .dns import DnsResult
            return DnsResult(raw_data, **kwargs)
        elif kind == "sslcert":
            from .ssl import SslResult
            return SslResult(raw_data, **kwargs)
        elif kind == "http":
            from .http import HttpResult
            return HttpResult(raw_data, **kwargs)
        elif kind == "ntp":
            from .ntp import NtpResult
            return NtpResult(raw_data, **kwargs)
        elif kind == "wifi":
            from .wifi import WiFiResult
            return WiFiResult(raw_data, **kwargs)

        raise ResultParseError("Unknown type value was found in the JSON input")

    @staticmethod
    def calculate_median(given_list):
        """
        Returns the median of values in the given list.
        """
        median = None

        if not given_list:
            return median

        given_list = sorted(given_list)
        list_length = len(given_list)

        if list_length % 2:
            median = given_list[int(list_length / 2)]
        else:
            median = (given_list[int(list_length / 2)] + given_list[int(list_length / 2) - 1]) / 2.0

        return median

    @property
    def type(self):
        return self.__class__.__name__.replace("Result", "").lower()


__all__ = (
    "Result",
    "ResultParseError",
)
