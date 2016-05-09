"""RPC helper library for building Thrift HTTP and JSON based services.

See the README.md file for more details. This inline doc only contains a very short description,
which assumes a little bit.

If one has service Adder in adder.thrift, the library can be used as:

>> handler = AdderHandler()
>> server = easyrpc.on(handler, adder_service, 'localhost', 10000)
>> server.serve()

on the server. The client side code looks like:

>> client = easyrpc.to(adder_service, 'localhost', 10000)
>> with client.open() as context:
>>   print context.addTwo(10, 20) # will result in 30
>>   print context.addTwo(100, 200)
"""

import BaseHTTPServer

from thrift.protocol import TJSONProtocol
from thrift.server import THttpServer
from thrift.transport import THttpClient


def on(handler, service_class, host, port):
    """Create a Thrift HTTP and JSON based server.

    Args:
      handler: the handler object for the Thrift service.
      service_class (type): the generated module for the service.
      host (str): hostname to listen on.
      port (int): port on hostname to listen on.

    Returns:
      THttpServer: a properly configured thrift HTTP server.
    """

    processor = service_class.Processor(handler)
    pfactory = TJSONProtocol.TJSONProtocolFactory()
    server = THttpServer.THttpServer(
        processor, (host, port), pfactory, server_class=_SilentHTTPServer)
    return server
    

def to(service_class, host, port):
    """Creates a client for a Thrift HTTP and JSON based service.

    The open() method is used to provide contextmanager objects with which calls can be made
    in a garbage collection aware manner.

    Args:
      service_class (type): the generated module for the service.
      host (str): hostname to listen on.
      port (int): port on hostname to listen on.

    Returns:
      A provider of contextmanager objects.
    """

    return _ClientContextProvider(service_class, host, port)


class _SilentHTTPServer(BaseHTTPServer.HTTPServer):
    """Simple extension of the basic HTTPServer which doesn't do any logging."""

    def __init__(self, address, handler):
        class _SilentHandler(handler):
            def log_message(self, format, *args):
                pass

        BaseHTTPServer.HTTPServer.__init__(self, address, _SilentHandler)


class _ClientContextProvider(object):
    """A provider of contextmanager objects which manage connections to a service."""

    def __init__(self, service_class, host, port):
        self._service_class = service_class
        self._host = host
        self._port = port

    def open(self):
        """Produce a contextmanager object for communicating with the service."""

        return _ClientContext(self._service_class, self.address)

    @property
    def address(self):
        return 'http://{}:{}'.format(self._host, self._port)


class _ClientContext(object):
    """Contextmanager for controlling the interaction with a service."""

    def __init__(self, service_class, address):
        self._service_class = service_class
        self._address = address
        self._transport = None

    def __enter__(self):
        self._transport = THttpClient.THttpClient(self._address)
        protocol = TJSONProtocol.TJSONProtocol(self._transport)
        client = self._service_class.Client(protocol)
        self._transport.open()
        return client

    def __exit__(self, type, value, traceback):
        self._transport.close()
        return False
