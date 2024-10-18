# WithNoException
Python with block that ignores exceptions

# Usage

```python
from no_exception import NoException


def no_exception():
    with NoException():
        raise Exception()
    print("Hi")


def exception():
    raise Exception()
    print("Hi")


no_exception()  # Hi
exception()  # Exception is raised
```