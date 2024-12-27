from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any
from .load_balancer import LoadBalancer
from .config import settings

app = FastAPI()
load_balancer = LoadBalancer(settings.WORKER_COUNT)

class Task(BaseModel):
    type: str
    data: Dict[str, Any]

@app.post("/task")
async def create_task(task: Task):
    try:
        load_balancer.distribute_task(task.dict())
        return {"status": "Task accepted"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    worker_status = load_balancer.health_check()
    return {
        "status": "healthy" if all(worker_status) else "degraded",
        "worker_status": worker_status
    }

@app.get("/metrics")
async def get_metrics():
    try:
        # Get metrics from Redis
        queue_manager = QueueManager()
        tasks_length = queue_manager.get_queue_length('tasks')
        results_length = queue_manager.get_queue_length('results')
        
        # Calculate metrics
        metrics = {
            'total_interactions': tasks_length + results_length,
            'active_workers': len([w for w in workers if w.running]),
            'avg_response_time': 2.5,  # Example value
            'satisfaction': 4.2,
            'sentiments': {
                'positive': 45,
                'neutral': 30,
                'negative': 25
            },
            'channels': {
                'chat': 40,
                'voice': 30,
                'email': 30
            },
            'response_times': {
                'chat': 2,
                'voice': 1,
                'email': 5
            }
        }
        return metrics
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))