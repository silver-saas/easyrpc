import logging
import multiprocessing
import os
import portpicker
import signal
import unittest

from thrift.server import THttpServer

import easyrpc
import thriftgen_easyrpc_tests_adder.Service as adder_service


class AdderHandler(object):
    def addTwo(self, a, b):
        return a + b

    def addThree(self, a, b, c):
        return a + b + c


class OnTest(unittest.TestCase):
    def test_on(self):
        """Construct a server."""

        handler = AdderHandler()
        server = easyrpc.on(handler, adder_service, 'localhost', portpicker.pick_unused_port())
        self.assertIsInstance(server, THttpServer.THttpServer)

    def test_silent_request(self):
        """Call log_message once on the silent request handler for coverage's sake."""

        handler = AdderHandler()
        server = easyrpc.on(handler, adder_service, 'localhost', portpicker.pick_unused_port())

        class _DumbHandler(server.httpd.RequestHandlerClass):
            def __init__(self):
                pass

        http_request_handler = _DumbHandler()
        http_request_handler.log_message('unused')


class ToTest(unittest.TestCase):
    def test_to_looks_alright(self):
        """Construct a client."""

        client = easyrpc.to(adder_service, 'localhost', 10000)
        self.assertTrue(hasattr(client, 'open'))

    def test_server_address(self):
        """Server address is constructed correctly."""

        client = easyrpc.to(adder_service, 'localhost', 10000)
        self.assertEqual(client.address, 'http://localhost:10000')

    def test_client_provides_context(self):
        """The open method for a client produces a context."""

        client = easyrpc.to(adder_service, 'localhost', 10000)
        client_context = client.open()

        self.assertTrue(hasattr(client_context, '__enter__'))
        self.assertTrue(hasattr(client_context, '__exit__'))


class EndToEndTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        def start_server(port):
            signal.signal(signal.SIGTERM, lambda signum, frame: os._exit(0))

            logging.disable(logging.CRITICAL)

            handler = AdderHandler()
            server = easyrpc.on(handler, adder_service, 'localhost', port)
            server.serve()

        cls._server_port = portpicker.pick_unused_port()
        cls._server_p = multiprocessing.Process(target=start_server, args=(cls._server_port,))
        cls._server_p.start()

    @classmethod
    def tearDownClass(cls):
        cls._server_p.terminate()
        cls._server_p.join()

    def test_one_call(self):
        """Make one real RPC to the test adder service."""

        client = easyrpc.to(adder_service, 'localhost', EndToEndTest._server_port)

        with client.open() as client_context:
            self.assertEqual(client_context.addTwo(10, 20), 30)

    def test_two_calls(self):
        """Make two separate and real RPCs to the test adder service in different context."""

        client = easyrpc.to(adder_service, 'localhost', EndToEndTest._server_port)

        with client.open() as client_context:
            self.assertEqual(client_context.addTwo(10, 20), 30)

        with client.open() as client_context:
            self.assertEqual(client_context.addThree(10, 20, 30), 60)

    def test_two_calls_same_context(self):
        """Make two separate and real RPCs to the test adder service in the same context."""

        client = easyrpc.to(adder_service, 'localhost', EndToEndTest._server_port)

        with client.open() as client_context:
            self.assertEqual(client_context.addTwo(10, 20), 30)
            self.assertEqual(client_context.addThree(10, 20, 30), 60)


if __name__ == '__main__':
    unittest.main()
