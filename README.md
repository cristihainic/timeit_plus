This is intended as decorator version of the built-in `timeit` Python module.

Extras include sending emails when time thresholds are exceeded and capability of using your own `logger.Logger()` instance to log messages.

Built with Django in mind, but can be used with Python in general.

Usage:

```python
from timeit_plus import tplus

@tplus()
def foo(bar):
    return bar
```

Optional keyword arguments you can pass to the `tplus()` decorator:

- `max_time`: TBC
- `email_config`: TBC
- `logger`: TBC

This README is still wip, check out decorator docstring for more info.