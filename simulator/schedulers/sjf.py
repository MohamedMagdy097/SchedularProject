from simulator.core.pq import PriorityQueue
from simulator.schedulers.scheduler import Scheduler

class SJF(Scheduler):
    """Shortest Job First (SJF) scheduler."""
    def __init__(self, alpha=0.5):
        super(SJF, self).__init__()
        self.alpha = alpha

        # We use a custom PriorityQueue with similar API instead
        self.q = PriorityQueue()

        # Keeps track of all estimates for CPU burst time
        self.tau = {}

    def schedule(self, processes):
        """
        We make use of a heap to keep track of the task with the longest burst
        time left.
        """
        self.tau = {process.id: 0 for process in processes}
        return super(SJF, self).schedule(processes)

    def enqueue_new_jobs(self):
        """
        (OVERRIDE) - Scheduler.enqueue_new_jobs
        We need to override this to make use of our PriorityQueue API instead.
        """
        while self.ordered and self.ordered[0].arrive_time <= self.current_time:
            nxt = self.ordered.popleft()
            self.q.add(nxt, priority=self.tau[nxt.id])

    def perform_schedule(self):

        self.active = self.q.pop() if self.q else None

        if self.active:
            self.tau[self.active.id] = self.predict_next_burst(
                self.tau[self.active.id],
                self.active.burst_time)

        return self.active

    def predict_next_burst(self, current_prediction, current_burst_time):
        """Returns the predicted time of the next burst of the process."""
        return self.alpha * current_burst_time + \
               (1 - self.alpha) * current_prediction
def predict_next_burst(self, current_prediction, current_burst_time):
        """Returns the predicted time of the next burst of the process."""
        return self.alpha * current_burst_time +\
            (1-self.alpha) * current_prediction