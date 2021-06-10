# win10notify

A library to create Windows 10 Toast Notifications

# Example usage

```python
from win10notify import Notifier


test = Notifier()
test.notify(
    title="Title",
    msg="This is an example notification.",
    imgpath=r"..\\icon.ico",
    appid="python",
)
```