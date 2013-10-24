import threading


class PLinkRequester(object):
    """Parallel link processor."""
    def __init__(self, num_worker_threads, workFn, inputQueue, outputQueue):
        self.inputQueue = inputQueue
        self.outputQueue = outputQueue
        self.num_worker_threads = num_worker_threads
        self.workFn = workFn

    def start(self):
        for i in range(self.num_worker_threads):
            t = threading.Thread(target=self.worker)
            t.daemon = True
            t.start()

    def worker(self):
        while True:
            workRequest = self.inputQueue.get()
            result = self.workFn(workRequest)
            self.outputQueue.put(result)
            # using the built-in queue work tracking
            # method to indicate work completed by thread
            self.inputQueue.task_done()

    def add_work(self, link_request):
        if (link_request is None):
            raise TypeError("link_request can not be None.")

        self.inputQueue.put(link_request)

    def get_results(self):
        # block until all threads indicate being done
        self.inputQueue.join()

        results = []

        while (self.outputQueue.empty() is False):
            results.append(self.outputQueue.get())

        return results
