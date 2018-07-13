import time
import random

from multiprocessing.pool import ThreadPool
from multiprocessing import Lock


class TaskPool:

    def __init__(self, workers):
        self._n_started = 0
        self.workers = workers if workers > 1 else 1
        self.running = [None for _ in range(0, workers)]
        self.mutex = Lock()
        self._guard_mutex = Lock()
        self.pool = ThreadPool(processes=self.workers)

    def _is_full(self):
        return self._n_started == self.workers

    def _task_entered(self):
        self._guard_mutex.acquire()
        self._n_started += 1
        self._guard_mutex.release()

    def _task_exited(self):
        self._guard_mutex.acquire()
        self._n_started -= 1
        self._guard_mutex.release()

    def _run_task(self, fn, args):
        self._task_entered()

        fn(args)

        self._task_exited()

    def run_task(self, fn, args):

        # don't overflow the task runner with tasks
        while self._is_full():
            time.sleep(random.randint(5, 15) / 10.0)

        # apply task
        self.pool.apply_async(TaskPool._run_task, (self, fn, args))


