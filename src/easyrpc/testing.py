"""Testing helpers for users of easyrpc.

Mocking clients is a little bit tricky, as one would want to mock the object returned in the with
statement, but that is several layers of indirection away. Hence this module.

If one needs a mockable client, the following will suffice:
>> from mockito import when
>> client = easyrpc.mock_to()
>> when(client.context).addTwo(10, 20).thenReturn(30)
"""

import mockito


def mock_to():
    """Creates a mock client."""

    return _MockClientContextProvider()


class _MockClientContextProvider(object):
    def __init__(self):
        self._context_mock = mockito.mock()

    def open(self):
        return _MockClientContext(self._context_mock)

    @property
    def context(self):
        return self._context_mock


class _MockClientContext(object):
    def __init__(self, context_mock):
        self._context_mock = context_mock

    def __enter__(self):
        return self._context_mock

    def __exit__(self, type, value, traceback):
        return False
