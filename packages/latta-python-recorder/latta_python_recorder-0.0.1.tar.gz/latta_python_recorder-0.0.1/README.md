# Latta Vanilla Python recorder


Usage is very simple, all you have to do is to provide an api key

```py

from latta import Latta

latta = Latta('api-key')

@latta.wrap
def divide(x, y):
    return x / y
```

Alternatively user can wrap more stuff while still assigning snapshots to just one instance.

Latta is typed like this `Latta(api_key: str, instance_id: Optional[str]=None, options: Optional[LattaOptions]=None)`

User can also specify extra options, for now just device type, the rest of options we collect Latta takes automatically on its own.