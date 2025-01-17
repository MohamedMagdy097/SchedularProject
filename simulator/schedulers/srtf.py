from simulator.core.pq import PriorityQueue
from simulator.schedulers.scheduler import Scheduler

class SRTF(Scheduler):
    """
    Shortest Remaining Time First (SRTF) scheduler.

    Think of this as a Shortest Job First (SJF) but pre-emptive.
    """

    def __init__(self):
        super(SRTF, self).__init__()

        # Ready queue
        self.q = PriorityQueue()

    def perform_schedule(self):
        """
        We perform scheduling in either of the two scenarios:
        1. A task completes its execution
        2. A shorter task has arrived in the ready queue.
        """
        if self.active and self.active.burst_time == 0:
            self.active = None

        if self.q and self.q.peek().burst_time < (self.active.burst_time if self.active else float('inf')):
            if self.active:
                self.q.add(self.active, priority=self.active.burst_time)
            self.active = self.q.pop()

        return self.active

    def enqueue_new_jobs(self):
        """
        (OVERRIDE) - Scheduler.enqueue_new_jobs

        We need to override this to make use of our PriorityQueue API instead.
        """
        while self.ordered and self.ordered[0].arrive_time == self.current_time:
            nxt = self.ordered.popleft()
            self.q.add(nxt, priority=nxt.burst_time)

    def timer_interrupt(self):
        """
        (OVERRIDE) - Scheduler.timer_interrupt

        We need to set a timer interrupt when a task of lower burst time comes
        in to the ready queue as well.
        """
        default = super(SRTF, self).timer_interrupt()
        if self.q and self.active:
            shorter = self.q.peek().burst_time < self.active.burst_time
        else:
            shorter = False

        return default or shorter