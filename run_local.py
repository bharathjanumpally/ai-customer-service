import subprocess
import sys
import time
from pathlib import Path

def check_redis():
    try:
        import redis
        r = redis.Redis(host='localhost', port=6379)
        r.ping()
        print("✓ Redis is running")
        return True
    except:
        print("✗ Redis is not running")
        return False

def main():
    # Check if Redis is running
    if not check_redis():
        print("Please start Redis server first")
        sys.exit(1)

    print("\nStarting AI Customer Service Platform...")
    
    # Start the FastAPI server
    api_process = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "src.distributed.api:app", "--host", "0.0.0.0", "--port", "8000"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    print("✓ API server started at http://localhost:8000")

    # Start worker processes
    worker_processes = []
    for i in range(3):  # Start 3 workers
        worker = subprocess.Popen(
            [sys.executable, "-m", "src.distributed.worker", str(i)],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        worker_processes.append(worker)
    print("✓ Worker processes started")

    print("\nSystem is ready!")
    print("\nAvailable endpoints:")
    print("- Health check: http://localhost:8000/health")
    print("- Submit task: http://localhost:8000/task")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nShutting down...")
        api_process.terminate()
        for worker in worker_processes:
            worker.terminate()

if __name__ == "__main__":
    main()