import logging
import threading
import sigterm

from simqclient import SimqClient


__all__ = [
    "SimqServiceProvider",
]
_logger = logging.getLogger(__name__)


class SimqServiceProvider(SimqClient):
    channel = None

    def __init__(self, workers=1, *args, **kwargs):
        self._status = "new"
        self._start_lock = threading.Lock()
        self.workers = workers
        super().__init__(*args, **kwargs)
        self.worker_threads = []

    def start(self):
        with self._start_lock:
            # 已启动、已停止的服务均不允许重新启动
            if self._status != "new":
                return
            self._status = "running"
            for _ in range(self.workers):
                worker_thread = threading.Thread(target=self._main, daemon=True)
                worker_thread.start()
                self.worker_threads.append(worker_thread)

    def wait_forever(self):
        for worker_thread in self.worker_threads:
            worker_thread.join()

    def _main(self):
        while not sigterm.is_stopped():
            try:
                self.main()
            except Exception as error:
                _logger.exception("SimqServiceProvider main loop error: %s", error)

    def main(self):
        while not sigterm.is_stopped():
            task = self.pop(self.channel, timeout=5)
            if task is None:
                continue
            task_id = task.get("id", None)
            if not task_id:
                continue
            # @todo: 任务异常应该如何处理呢？
            result = self.task_handler(task)
            self.ack(self.channel, id=task_id, result=result)

    def task_handler(self, task):
        data = task.get("data", {})
        data = data or {}
        return self.handler(**data)

    def handler(self, **data):
        raise NotImplementedError()
