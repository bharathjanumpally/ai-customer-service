import redis
import json
from typing import Dict, Any, Optional

class QueueManager:
    def __init__(self):
        try:
            self.redis_client = redis.Redis(
                host='localhost',
                port=6379,
                decode_responses=True
            )
            # Test connection
            self.redis_client.ping()
            print("Successfully connected to Redis")
        except Exception as e:
            print(f"Error connecting to Redis: {e}")
            raise
    
    def push_task(self, queue_name: str, task: Dict[str, Any]) -> int:
        """
        Push a task to the specified queue
        Returns the length of the queue after pushing
        """
        try:
            result = self.redis_client.lpush(queue_name, json.dumps(task))
            print(f"Task pushed to queue {queue_name}: {task.get('id', 'unknown')}")
            return result
        except Exception as e:
            print(f"Error pushing to queue: {e}")
            raise
    
    def pop_task(self, queue_name: str) -> Optional[Dict[str, Any]]:
        """
        Pop a task from the specified queue
        Returns None if no task is available
        """
        try:
            task = self.redis_client.brpop(queue_name, timeout=1)
            if task:
                print(f"Task popped from queue {queue_name}")
                return json.loads(task[1])
            return None
        except Exception as e:
            print(f"Error popping from queue: {e}")
            return None

    def get_queue_length(self, queue_name: str) -> int:
        """Get the current length of the queue"""
        try:
            return self.redis_client.llen(queue_name)
        except Exception as e:
            print(f"Error getting queue length: {e}")
            return 0