from .base import Result, ParsingDict

class Response(ParsingDict):

    def __init__(self, data, **kwargs):

        ParsingDict.__init__(self, **kwargs)

        self.raw_data = data
        self.af = self.ensure("af", int)
        self.body_size = self.ensure("bsize", int)
        self.head_size = self.ensure("hsize", int)
        self.destination_address = self.ensure("dst_addr", str)
        self.source_address = self.ensure("src_addr", str)
        self.code = self.ensure("res", int)
        self.response_time = self.ensure("rt", float)
        self.version = self.ensure("ver", str)

        if not self.destination_address:
            self.destination_address = self.ensure(
                "addr", str, self.destination_address)

        if not self.source_address:
            self.source_address = self.ensure(
                "srcaddr", str, self.source_address)

        if not self.code:
            self._handle_malformation("No response code available")

        error = self.ensure("err", str)
        if error:
            self._handle_error(error)


class HttpResult(Result):

    METHOD_GET = "GET"
    METHOD_POST = "POST"
    METHOD_PUT = "PUT"
    METHOD_DELETE = "DELETE"
    METHOD_HEAD = "HEAD"
    METHODS = {
        METHOD_GET: "GET",
        METHOD_POST: "POST",
        METHOD_PUT: "PUT",
        METHOD_DELETE: "DELETE",
        METHOD_HEAD: "HEAD"
    }

    def __init__(self, data, **kwargs):

        Result.__init__(self, data, **kwargs)

        self.uri = self.ensure("uri", str)
        self.method = None

        self.responses = []

        if "result" not in self.raw_data:
            self._handle_malformation("No result value found")
            return

        if isinstance(self.raw_data["result"], list):

            # All modern results

            for response in self.raw_data["result"]:
                self.responses.append(Response(response, **kwargs))

            if self.responses:
                method = self.raw_data["result"][0].get(
                    "method",
                    self.raw_data["result"][0].get("mode")  # Firmware == 4300
                )
                if method:
                    method = method.replace("4", "").replace("6", "")
                    if method in self.METHODS.keys():
                        self.method = self.METHODS[method]

        else:

            # Firmware <= 1

            response = self.raw_data["result"].split(" ")
            self.method = response[0].replace("4", "").replace("6", "")
            self.responses.append(Response({
                "dst_addr": response[1],
                "rt": float(response[2]) * 1000,
                "res": int(response[3]),
                "hsize": int(response[4]),
                "bsize": int(response[5]),
            }))


__all__ = (
    "HttpResult"
)
