from celery import states as task_states
from celery.events.snapshot import Polaroid
from celery.events.state import State


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

    @staticmethod
    def _extract_task_name(name):
        return name.split('.')[-1]

    def _process_tasks(self, state: State, timestamp):
        tasks = self._get_dict(state)
        for task in state.tasks.values():

            if not task.name:
                logger.info('Ignoring task without task-received event captured.')
                continue

            tasks[task.name][task.state] += 1
            if task.state == task_states.FAILURE:
                logger.info(f'Adding exception event {task.exception}.')
                data = task.info() if self._verbose_exception else task.exception
                self._pusher.add_event(
                    what='Exception',
                    tags=['task-failure'],
                    when=timestamp,
                    data=data
                )

        for task, states in tasks.items():
            for state, amount in states.items():
                task_name = self._extract_task_name(task)
                logger.debug(f'Adding metrics for {task_name}.{state} - {amount}.')
                self._pusher.add(timestamp, amount, ['tasks', 'by_name', task_name, state])

    def _process_workers(self, state: State, timestamp):
        for worker_name, worker_state in state.workers.items():
            self._pusher.add(
                timestamp,
                worker_state.active,
                ['workers', 'by_name', worker_name, 'active']
            )

        workers_alive = 0
        for _ in state.alive_workers():
            workers_alive += 1

        logger.info(f'Adding metrics workers.alive {workers_alive}.')
        self._pusher.add(timestamp, workers_alive, ['workers', 'alive'])

    def on_shutter(self, state):
        timestamp = time.time()
        self._process_tasks(state, timestamp)
        self._process_workers(state, timestamp)
