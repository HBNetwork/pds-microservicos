import time
import logging
from queue import Queue
from threading import Thread

from itertools import count, cycle


class Zoo(Thread):
    _ids = count(1)

    def __init__(self, cmd_queue, data, *args,
             log_level=logging.DEBUG, **kwargs):

        super().__init__()
        self.name = f'{self.__class__.__name__.lower()}-{next(self._ids)}'
        self.data = data
        self.log_level = log_level
        self.args = args
        self.kwargs = kwargs

        self.logger = self._init_logging()
        self.cmd_queue = cmd_queue

        self.data_size = len(data)
        self.actual_item = None
        self.iter_cnt = 0
        self.cnt = count(1)
        self.cyc = cycle(self.data)

    def cycle(self):
        item = next(self.cyc)
        if next(self.cnt) % self.data_size == 0:  # new iteration round
            self.iter_cnt += 1
        self.actual_item = f'{item}_{self.iter_cnt}'

    def run(self):
        """
        Run is the main-function in the new thread. Here we overwrite run
        inherited from threading.Thread.
        """
        while True:
            if self.cmd_queue.empty():
                self.cycle()
                self.logger.debug(self.actual_item)
                time.sleep(1)  # optional heartbeat
            else:
                self._get_cmd()
                self.cmd_queue.task_done()  # unblocks prompter

    def stop(self):
        self.logger.info(f'stopping with actual item: {self.actual_item}')
        # do clean up
        raise SystemExit

    def pause(self):
        self.logger.info(f'pausing with actual item: {self.actual_item}')
        self.cmd_queue.task_done()  # unblocks producer joining the queue
        self._get_cmd()  # just wait blockingly until next command

    def resume(self):
        self.logger.info(f'resuming with actual item: {self.actual_item}')

    def report(self):
        self.logger.info(f'reporting with actual item: {self.actual_item}')
        print(f'completed {self.iter_cnt} iterations over data')

    def _init_logging(self):
        fmt = '[%(asctime)s %(levelname)-8s %(threadName)s' \
          ' %(funcName)s()] --- %(message)s'
        logging.basicConfig(format=fmt, level=self.log_level)
        return logging.getLogger()

    def _get_cmd(self):
        cmd = self.cmd_queue.get()
        try:
            self.__class__.__dict__[cmd](self)
        except KeyError:
            print(f'Command `{cmd}` is unknown.')

class Prompter(Thread):
    """Prompt user for command input.
    Runs in a separate thread so the main-thread does not block.
    """
    def __init__(self, cmd_queue):
        super().__init__()
        self.cmd_queue = cmd_queue

    def run(self):
        while True:
            cmd = input('prompt> ')
            self.cmd_queue.put(cmd)
            self.cmd_queue.join()  # blocks until consumer calls task_done()


if __name__ == '__main__':

    data = ['ape', 'bear', 'cat', 'dog', 'elephant', 'frog']

    cmd_queue = Queue()
    prompter = Prompter(cmd_queue=cmd_queue)
    prompter.daemon = True

    zoo = Zoo(cmd_queue=cmd_queue, data=data)

    prompter.start()
    zoo.start()
