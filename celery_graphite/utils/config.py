import argparse
import runpy

from .extract import extract


def parse_config():
    parser = argparse.ArgumentParser(description='Celery graphite monitor.')

    parser.add_argument(
        '--config',
        help='Config file. Must be valid python module.'
    )

    parser.add_argument(
        '--broker',
        help='Celery broker url. (e.g. redis://localhost:6379/0)',
    )

    parser.add_argument(
        '--graphite',
        help='Graphite server url for pushing metrics.',
    )

    parser.add_argument(
        '--graphite-port',
        help='Graphite server port for pushing metrics.',
        type=int,
        default=2004
    )

    parser.add_argument(
        '--graphite-retention',
        help='Number of metrics for store before batch pushing.',
        default=50,
        type=int
    )

    parser.add_argument(
        '--graphite-http-url',
        help='Graphite http url for pushing exception events.'
    )

    parser.add_argument(
        '--freq',
        help='Frequency for capturing metrics.',
        default=5,
        type=int
    )

    parser.add_argument(
        '--graphite-prefix',
        help='Prefix for graphite path.',
        default=None
    )

    parser.add_argument(
        '--verbose-exception',
        help='Export exception more verbose with args and kwargs.',
        action='store_true'
    )

    parser.add_argument(
        '--graphite-tag',
        help='Additional tag added to graphite events.'
    )

    parser.add_argument(
        '--verbose', '-v',
        help='Verbosity level.',
        action='count',
        default=1
    )

    args = parser.parse_args()

    config = {
        'graphite': args.graphite,
        'graphite_port': args.graphite_port,
        'graphite_http_url': args.graphite_http_url,
        'graphite_retention': args.graphite_retention,
        'graphite_tag': args.graphite_tag,
        'graphite_prefix': args.graphite_prefix,
        'freq': args.freq,
        'verbose_exception': args.verbose_exception,
        'broker': args.broker,
        'verbose_level': 70 - (10*args.verbose) if args.verbose > 0 else 0
    }

    if args.config:
        globals_dict = runpy.run_path(args.config)
        extract(config, globals_dict)

    if (
            not config['graphite'] or
            not config['broker']
    ):
        parser.print_help()
        exit(-1)

    return config
