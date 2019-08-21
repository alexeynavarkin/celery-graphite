from celery import states as task_states
from celery.events.snapshot import Polaroid

from copy import deepcopy

import logging

import time


"""
Format for storing tasks data.

tasks = {
    'task_name': {
        'PENDING' : 0,
        'SUCCESS' : 10
    }
}
"""


logger = logging.getLogger('CeleryCamera')


class CeleryCamera(Polaroid):
    clear_after = True

    STATES_DICT = {key: 0 for key in task_states.ALL_STATES}

    def __init__(self, pusher, verbose_exception=False, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._dict = None
        self._pusher = pusher
        self._verbose_exception = verbose_exception

    def _get_dict(self, state):
        if not self._dict or len(self._dict) != len(state.task_types()):
            self._dict = {
                key: self.STATES_DICT.copy() for key in state.task_types()
            }
        return deepcopy(self._dict)

    def _process_tasks(self, state, timestamp):
        tasks = self._get_dict(state)
        for task in state.tasks.values():

            if not task.name:
                logger.info('Ignoring task without task-received event captured.')
                continue

            tasks[task.name][task.state] += 1
            if task.state == task_states.FAILURE:
                data = task.info() if self._verbose_exception else task.exception
                self._pusher.add_event(
                    what='Exception',
                    tags=['task-failure'],
                    when=timestamp,
                    data=data
                )

        for task, states in tasks.items():
            for state, amount in states.items():
                self._pusher.add(timestamp, amount, [task, state])

    def _process_workers(self, state, timestamp):
        workers_alive = 0
        for _ in state.alive_workers():
            workers_alive += 1
        self._pusher.add(timestamp, workers_alive, ['workers', 'alive'])

    def on_shutter(self, state):
        timestamp = time.time()
        self._process_tasks(state, timestamp)
        self._process_workers(state, timestamp)
