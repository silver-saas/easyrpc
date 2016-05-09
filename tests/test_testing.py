from mockito import when
import unittest

import easyrpc


class MockTest(unittest.TestCase):
    def test_mock(self):
        """Client mocking works as a context."""

        client = easyrpc.mock_to()
        when(client.context).addTwo(10, 20).thenReturn(40)

        with client.open() as context:
            self.assertEqual(context.addTwo(10, 20), 40)


if __name__ == '__main__':
    unittest.main()
