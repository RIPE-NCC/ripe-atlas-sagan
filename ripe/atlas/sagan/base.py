import arrow
import logging

# Try to use ujson if it's available
try:
    import ujson as json
except ImportError:
    logging.warning(
        "Use of the default json module is discouraged.  Instead, consider "
        "using ujson, a much faster parser."
    )
    import json

# Hack for Python2/3
try:
    compat_basestring = basestring  # Python2
except NameError:
    compat_basestring = str  # Python3


class ResultParseError(Exception):
    pass


class ResultError(Exception):
    pass


class DictionaryLikeMixin(object):
    """
    Python 2.x and 3.x handle the creation of dictionary-like objects
    differently.  If we write it this way, it works for both.
    """

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

    @staticmethod
    def _is_property_name(p):
        if not p.startswith("_"):
            if p not in ("keys",):
                if not p.upper() == p:
                    return True
        return False


class ValidationMixin(DictionaryLikeMixin):
    """
    A handy container for methods we use for validation in the various result
    classes.
    """

    ACTION_IGNORE = 1
    ACTION_WARN   = 2
    ACTION_FAIL   = 3

    PROTOCOL_ICMP = "ICMP"
    PROTOCOL_UDP  = "UDP"
    PROTOCOL_TCP  = "TCP"
    PROTOCOL_MAP = {
        "ICMP": PROTOCOL_ICMP,
        "I":    PROTOCOL_ICMP,
        "UDP":  PROTOCOL_UDP,
        "U":    PROTOCOL_UDP,
        "TCP":  PROTOCOL_TCP,
        "T":    PROTOCOL_TCP,
    }

    def __init__(self, **kwargs):

        DictionaryLikeMixin.__init__(self)

        self._on_error     = kwargs.pop("on_error", self.ACTION_WARN)
        self.is_error      = False
        self.error_message = None

        self._on_malformation = kwargs.pop("on_malformation", self.ACTION_WARN)
        self.is_malformed     = False

    def ensure(self, key, kind, default=None):
        try:
            if kind == "datetime":
                return arrow.get(self.raw_data[key])
            return kind(self.raw_data[key])
        except (TypeError, ValueError, KeyError, arrow.parser.ParserError):
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


class Result(ValidationMixin):
    """
    The parent class for all measurement result classes.  Subclass this to
    handle parsing a new measurement type, or use .get() to let this class
    figure out the type for you.
    """

    def __init__(self, data, *args, **kwargs):

        ValidationMixin.__init__(self, **kwargs)

        self.raw_data = data
        if isinstance(data, compat_basestring):
            self.raw_data = json.loads(data)

        for key in ("timestamp", "msm_id", "prb_id", "fw", "type"):
            if key not in self.raw_data:
                raise ResultParseError(
                    "This does not look like a RIPE Atlas measurement: {raw_data}".format(
                        raw_data=self.raw_data
                    )
                )

        self.created            = arrow.get(self.raw_data["timestamp"])
        self.measurement_id     = self.ensure("msm_id", int)
        self.probe_id           = self.ensure("prb_id", int)
        self.firmware           = self.ensure("fw",     int)
        self.origin             = self.ensure("from",   str)
        self.seconds_since_sync = self.ensure("lts",    int)

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
        return self.created.timestamp


    @classmethod
    def get(cls, data, **kwargs):
        """
        Call this when you have a JSON result and just want to turn it into the
        appropriate Result subclass.  This is less performant than calling
        PingResult(json_string) directly however, as the JSON has to be parsed
        first to find the type.
        """

        raw_data = data
        if isinstance(data, compat_basestring):
            raw_data = json.loads(data)

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

        raise ResultParseError("Unknown type value was found in the JSON input")

    def calculate_median(self, given_list):
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


__all__ = (
    "Result",
    "ResultParseError",
)
