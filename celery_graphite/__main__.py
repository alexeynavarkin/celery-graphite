import logging

from celery import Celery

from .celery_camera import CeleryCamera
from .graphite_pusher import GraphitePusher
from .utils.config import parse_config


logger = logging.getLogger('CeleryGraphiteMain')


def main():
    config = parse_config()

    logging.basicConfig(
            level=config['verbose_level'],
            format='%(asctime)s %(levelname)s: %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

    celery_app = Celery(broker=config['broker'])
    state = celery_app.events.State()

    graphite_pusher = GraphitePusher(
        host=config['graphite'],
        port=config['graphite_port'],
        prefix=config['graphite_prefix'],
        http_url=config['graphite_http_url'],
        retention=config['graphite_retention'],
        tag=config['graphite_tag']
    )

    try:
        with celery_app.connection() as connection:
            recv = celery_app.events.Receiver(
                connection,
                handlers={
                    '*': state.event
                }
            )

            with CeleryCamera(
                    pusher=graphite_pusher,
                    state=state,
                    freq=config['freq'],
                    verbose_exception=config['verbose_exception']
            ):
                recv.capture(limit=None, timeout=None)
    except KeyboardInterrupt:
        logger.info('Got SIGINT, gracefully pushing metrics and shutting down.')
        graphite_pusher.push()


if __name__ == '__main__':
    main()
