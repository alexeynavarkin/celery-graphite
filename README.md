# Celery Graphite

Utility for pushing celery metrics into graphite

#### Avaliable metrics:

Number of tasks in each state
```
[prefix.]taskname.TASK_STATE = count
```

Number of workers alive
```
[prefix.]workers.alive = count
```

#### Events

Also if ```graphite-http-url``` provided task-failed events
will be pushed as graphite events with only exception name by default
or if ```verbose-exception``` specified complete task info provided.
Be aware of long exception args and kwargs.

#### Usage:

```
usage: celery_graphite [-h] [--config CONFIG] [--broker BROKER]
                       [--graphite GRAPHITE] [--graphite-port GRAPHITE_PORT]
                       [--graphite-retention GRAPHITE_RETENTION]
                       [--graphite-http-url GRAPHITE_HTTP_URL] [--freq FREQ]
                       [--graphite-prefix GRAPHITE_PREFIX]
                       [--verbose-exception] [--graphite-tag GRAPHITE_TAG]
                       [--verbose]

Celery graphite monitor.

optional arguments:
  -h, --help            show this help message and exit
  --config CONFIG       Config file. Must be valid python module.
  --broker BROKER       Celery broker url. (e.g. redis://localhost:6379/0)
  --graphite GRAPHITE   Graphite server url for pushing metrics.
  --graphite-port GRAPHITE_PORT
                        Graphite server port for pushing metrics.
  --graphite-retention GRAPHITE_RETENTION
                        Number of metrics for store before batch pushing.
  --graphite-http-url GRAPHITE_HTTP_URL
                        Graphite http url for pushing exception events.
  --freq FREQ           Frequency for capturing metrics.
  --graphite-prefix GRAPHITE_PREFIX
                        Prefix for graphite path.
  --verbose-exception   Export exception more verbose with args and kwargs.
  --graphite-tag GRAPHITE_TAG
                        Additional tag added to graphite events.
  --verbose, -v         Verbosity level.
```

or any config parameter can be set via variable in file passed to --config parameter.
Should valid python module. 