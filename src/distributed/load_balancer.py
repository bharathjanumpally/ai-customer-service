from typing import List
import random
from .queue_manager import QueueManager

class LoadBalancer:
    def __init__(self, worker_count: int):
        self.worker_count = worker_count
        self.queue_manager = QueueManager()
        
    def distribute_task(self, task):
        """Distribute task using round-robin strategy"""
        queue_lengths = [
            self.queue_manager.get_queue_length(f'worker_{i}')
            for i in range(self.worker_count)
        ]
        
        # Select worker with shortest queue
        target_worker = queue_lengths.index(min(queue_lengths))
        self.queue_manager.push_task(f'worker_{target_worker}', task)
        
    def health_check(self) -> List[bool]:
        """Check health of all workers"""
        return [
            self.queue_manager.get_queue_length(f'worker_{i}') < 1000
            for i in range(self.worker_count)
        ]