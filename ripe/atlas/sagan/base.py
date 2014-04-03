import arrow
import logging

try:
    import ujson as json
except ImportError:
    import json

class ResultParseError(Exception):
    pass


class ValidationMixin(object):
    """
    A handy container for methods we use for validation in the various result
    classes.
    """

    PROTOCOL_ICMP = 1
    PROTOCOL_UDP  = 2
    PROTOCOL_TCP  = 3
    PROTOCOL_MAP = {
        "ICMP": PROTOCOL_ICMP,
        "UDP":  PROTOCOL_UDP,
        "TCP":  PROTOCOL_TCP
    }

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
                raise ResultParseError(
                    '"{protocol}" is not a recognised protocol'.format(
                        protocol=protocol
                    )
                )


class Result(ValidationMixin, object):
    """
    The parent class for all measurement result classes.  Subclass this to
    handle parsing a new measurement type, or use .get() to let this class
    figure out the type for you.
    """

    ERROR_IGNORE = 1
    ERROR_WARN   = 2
    ERROR_FAIL   = 3

    def __init__(self, data, on_error=ERROR_WARN):

        self._on_error = on_error

        self.raw_data = data
        if isinstance(data, basestring):
            self.raw_data = json.loads(data)

        self.created        = arrow.get(self.raw_data["timestamp"])
        self.measurement_id = self.raw_data["msm_id"]
        self.probe_id       = self.raw_data["prb_id"]
        self.firmware       = self.ensure("fw", int)
        self.origin         = self.ensure("from", str)
        self.is_error       = False

        # Handle the weird case where fw=0 and we don't know what to expect
        if self.firmware == 0:
            self._handle_error("Unknown firmware: {fw}".format(
                fw=self.firmware)
            )

        if "dnserr" in self.raw_data:
            self._handle_error("Error found: {err}".format(
                err=self.raw_data["dnserr"]
            ))

    def __repr__(self):
        return "Measurement #{measurement}, Probe #{probe}".format(
            measurement=self.measurement_id,
            probe=self.probe_id
        )

    @property
    def created_timestamp(self):
        return self.created.timestamp


    @classmethod
    def get(cls, json_string, **kwargs):
        """
        Call this when you have a JSON result and just want to turn it into the
        appropriate Result subclass.  This is less performant than calling
        PingResult(json_string) directly however, as the JSON has to be parsed
        first to find the type.
        """

        raw_data = json.loads(json_string)
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

        raise ResultParseError("Unknown type value was found in the JSON input")

    def _handle_error(self, message):
        if self._on_error == self.ERROR_FAIL:
            raise ResultParseError(message)
        elif self._on_error == self.ERROR_WARN:
            logging.warning(message)
        self.is_error = True


__all__ = (
    "Result",
    "ResultParseError",
)
