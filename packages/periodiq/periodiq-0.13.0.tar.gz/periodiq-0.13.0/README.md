# Simple Scheduler for Dramatiq Task Queue

[dramatiq](https://dramatiq.io) task queue is great but lacks a scheduler. This
project fills the gap.


## Features

- Cron-like scheduling.
- Single process.
- Fast and simple implementation.
- Easy on resources using SIGALRM.
- No dependencies except dramatiq ones.
- CLI consistent with dramatiq.
- Skip outdated message.


## Installation

periodiq is licensed under LGPL 3.0+. Please see [COPYING] and [COPYING.LESSER]
for licensing details.

[COPYING]: https://gitlab.com/bersace/periodiq/-/bloc/master/COPYING
[COPYING.LESSER]: https://gitlab.com/bersace/periodiq/-/bloc/master/COPYING.LESSER

``` console
$ pip install periodiq
```

Declare periodic tasks like this:

``` python
# filename: app.py

import dramatiq
from periodiq import PeriodiqMiddleware, cron

broker.add_middleware(PeriodiqMiddleware(skip_delay=30))

@dramatiq.actor(periodic=cron('0 * * * *'))
def hourly():
    # Do something each hour…
    ...
```

Then, run scheduler with:

``` console
$ periodiq -v app
[INFO] Starting Periodiq, a simple scheduler for Dramatiq.
[INFO] Registered periodic actors:
[INFO]
[INFO]     m h dom mon dow          module:actor@queue
[INFO]     ------------------------ ------------------
[INFO]     0 * * * *                app:hourly@default
[INFO]
...
```


## Support

If you need help or found a bug, consider [opening a GitLab
issue](https://gitlab.com/bersace/periodiq/issues/new) on the project. French
and English spoken.
