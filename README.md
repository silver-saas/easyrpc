# EasyRPC [![Build Status](https://travis-ci.org/silver-saas/easyrpc.svg?branch=master)](https://travis-ci.org/silver-saas/easyrpc) [![Coverage Status](https://coveralls.io/repos/github/silver-saas/easyrpc/badge.svg?branch=master)](https://coveralls.io/github/silver-saas/easyrpc?branch=master)

RPC helper library for building Thrift HTTP and JSON based services.

Suppose one has the following Thrift+ service.

```thrift
package easyrpc.tests.adder

service Service {
  i32 addTwo(1: i32 a, 2: i32 b);
  i32 addThree(1: i32 a, 2: i32 b, 3: i32 c);
}
```

The service gets packaged as `thriftgen_easyrpc_tests_adder`. The server-side handler is

```python
class AdderHandler(object):
    def addTwo(self, a, b):
        return a + b

    def addThree(self, a, b, c):
        return a + b + c
```

The server can then be created via:


```python
import easyrpc
import thriftgen_easyrpc_tests_adder.Service as adder_service

handler = AdderHandler()
server = easyrpc.on(handler, adder_service, 'localhost', 10000)
server.serve()
```

The client side code looks like:

```python
import easyrpc
import thriftgen_easyrpc_tests_adder.Service as adder_service

client = easyrpc.to(adder_service, 'localhost', 10000)

with client.open() as context:
  print context.addTwo(10, 20) # will result in 30
  print context.addTwo(100, 200)

with client.open() as context:
  print context.addThree(1000, 2000, 3)
```

## Testing ##
Mocking clients is a little bit tricky, as one would want to mock the object returned in the with
statement, but that is several layers of indirection away. Hence this module.

If one needs a mockable client, the following will suffice:

```python
from mockito import when
client = easyrpc.mock_to()
when(client.context).addTwo(10, 20).thenReturn(30)
```
