import asyncio
import sys
from src.distributed.worker import Worker
import redis

async def start_single_worker(worker_id: int):
    try:
        # Test Redis connection first
        redis_client = redis.Redis(host='localhost', port=6379)
        redis_client.ping()  # Will raise error if Redis is not running
        print(f"✓ Successfully connected to Redis")

        print(f"\nInitializing worker {worker_id}...")
        worker = Worker(worker_id)
        
        print(f"✓ Worker {worker_id} initialized")
        print(f"✓ Watching queues: tasks, results")
        print(f"\nWorker {worker_id} is now running and waiting for tasks...")
        print("(Press CTRL+C to stop the worker)")
        
        await worker.run()
    except redis.ConnectionError:
        print("✗ Error: Could not connect to Redis. Is Redis running?")
        print("Start Redis with: brew services start redis")
        sys.exit(1)
    except Exception as e:
        print(f"✗ Error starting worker {worker_id}: {e}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python start_worker.py <worker_id>")
        print("Example: python start_worker.py 0")
        sys.exit(1)
        
    worker_id = int(sys.argv[1])
    print(f"\n=== Starting Worker {worker_id} ===")
    
    try:
        asyncio.run(start_single_worker(worker_id))
    except KeyboardInterrupt:
        print(f"\n\nWorker {worker_id} shutting down...")