import asyncio
import uvicorn
from typing import List
import multiprocessing
from .worker import Worker
from .config import settings
from .api import app

def start_worker(worker_id: int):
    """Start a worker process"""
    worker = Worker(worker_id)
    worker.run()

def start_distributed_system():
    """Start the distributed system"""
    # Start worker processes
    processes: List[multiprocessing.Process] = []
    for i in range(settings.WORKER_COUNT):
        p = multiprocessing.Process(target=start_worker, args=(i,))
        p.start()
        processes.append(p)
    
    # Start API server
    uvicorn.run(
        app,
        host=settings.SERVICE_HOST,
        port=settings.SERVICE_PORT
    )
    
    # Wait for workers to complete
    for p in processes:
        p.join()

if __name__ == "__main__":
    start_distributed_system()