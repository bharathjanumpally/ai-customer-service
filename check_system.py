import redis
import json
from datetime import datetime

def check_system():
    try:
        # Connect to Redis
        redis_client = redis.Redis(
            host='localhost', 
            port=6379, 
            decode_responses=True
        )
        
        # Test Redis connection
        redis_client.ping()
        print("✓ Redis is running")
        
        # Check queues
        print("\nQueue Status:")
        print(f"Tasks queue size: {redis_client.llen('tasks')}")
        print(f"Results queue size: {redis_client.llen('results')}")
        
        # Check last 10 activities
        print("\nRecent Activities:")
        recent_tasks = redis_client.lrange('tasks', 0, 9)
        recent_results = redis_client.lrange('results', 0, 9)
        
        if recent_tasks:
            print("\nRecent Tasks:")
            for task in recent_tasks:
                try:
                    task_data = json.loads(task)
                    print(f"- Task ID: {task_data.get('id', 'unknown')}")
                except:
                    continue
                    
        if recent_results:
            print("\nRecent Results:")
            for result in recent_results:
                try:
                    result_data = json.loads(result)
                    print(f"- Worker {result_data.get('worker_id', 'unknown')}: "
                          f"Task {result_data.get('task_id', 'unknown')}")
                except:
                    continue
                    
    except redis.ConnectionError:
        print("✗ Redis is not running")
        print("Start Redis with: brew services start redis")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    print(f"\n=== System Status Check ({datetime.now().strftime('%Y-%m-%d %H:%M:%S')}) ===")
    check_system()