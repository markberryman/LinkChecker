import threading


class LinkRequester(object):
    """Parallel link processor."""
    def __init__(self, num_worker_threads, work_fn, input_queue, output_queue):
        self._input_queue = input_queue
        self._output_queue = output_queue
        self.num_worker_threads = num_worker_threads
        self.workFn = work_fn

    def start(self):
        for i in range(self.num_worker_threads):
            t = threading.Thread(target=self.worker)
            t.daemon = True
            t.start()

    def worker(self):
        while True:
            workRequest = self._input_queue.get()
            result = self.workFn(workRequest)
            self._output_queue.put(result)
            # using the built-in queue work tracking
            # method to indicate work completed by thread
            self._input_queue.task_done()

    def add_work(self, link_request):
        if (link_request is None):
            raise TypeError("link_request can not be None.")

        self._input_queue.put(link_request)

    def get_results(self):
        # block until all threads indicate being done
        self._input_queue.join()

        results = []

        while (self._output_queue.empty() is False):
            results.append(self._output_queue.get())

        return results
