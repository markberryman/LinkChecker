import queue
import threading


class LinkRequester(object):
    """Parallel link processor."""
    def __init__(self, num_worker_threads, work_fn, input_queue, output_queue):
        self._input_queue = input_queue
        self._output_queue = output_queue
        self.num_worker_threads = num_worker_threads
        self.work_fn = work_fn
        self.done = False

    def start(self):
        for i in range(self.num_worker_threads):
            t = threading.Thread(target=self.worker)
            # want non-daemonic threads b/c we don't want these threads
            # to be terminated abruptly; they need to hold up process
            # exit until they complete and can clean up resources (i.e.,
            # making web server connections)            
            t.daemon = False
            t.start()

    def worker(self):
        while (not self.done):
            try:
                # if timeout occurs, we get a Queue.Empty exception
                workRequest = self._input_queue.get(False, 1)
                result = self.work_fn(workRequest)
                self._output_queue.put(result)
                # using the built-in queue work tracking
                # method to indicate work completed by thread
                self._input_queue.task_done()
            except queue.Empty:
                # ignore
                pass            

    def add_work(self, link_request):
        if (link_request is None):
            raise TypeError("link_request can not be None.")

        self._input_queue.put(link_request)

    def get_results(self):
        # block until all items added to the input queue
        # have been "gotten" and marked as being done
        # w/ call to "task_done()"
        self._input_queue.join()

        results = []

        while (self._output_queue.empty() is False):
            results.append(self._output_queue.get())

        return results
