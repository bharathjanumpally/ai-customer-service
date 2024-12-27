import asyncio
from typing import Dict, Any, Optional
from .queue_manager import QueueManager
from ..models.sentiment_analyzer import SentimentAnalyzer
from ..models.intelligent_router import IntelligentRouter

class Worker:
    def __init__(self, worker_id: int):
        self.worker_id = worker_id
        self.queue_manager = QueueManager()
        self.sentiment_analyzer = SentimentAnalyzer(input_size=100, hidden_size=64, num_classes=3)
        self.router = IntelligentRouter()
        self.running = False
        print(f"Worker {worker_id} initialized")

    async def run(self):
        """Run the worker process"""
        print(f"Worker {self.worker_id} starting...")
        self.running = True
        
        while self.running:
            try:
                # Get task from queue
                task = self.queue_manager.pop_task('tasks')
                if task:
                    print(f"Worker {self.worker_id} processing task: {task.get('id', 'unknown')}")
                    result = await self.process_task(task)
                    
                    # Add worker ID to result
                    result['worker_id'] = self.worker_id
                    
                    # Push result back to queue
                    self.queue_manager.push_task('results', result)
                    print(f"Worker {self.worker_id} completed task: {task.get('id', 'unknown')}")
                await asyncio.sleep(0.1)  # Prevent CPU overload
            except Exception as e:
                print(f"Error in worker {self.worker_id}: {e}")
                continue

    async def process_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Process a single task"""
        task_type = task.get('type')
        data = task.get('data', {})
        
        if task_type == 'sentiment_analysis':
            result = await self.process_sentiment(data)
        elif task_type == 'routing':
            result = await self.process_routing(data)
        else:
            result = {'error': f'Unknown task type: {task_type}'}
            
        return {
            'task_id': task.get('id'),
            'type': task_type,
            'result': result
        }

    async def process_sentiment(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Process sentiment analysis task"""
        text = data.get('text', '')
        # Add your sentiment analysis logic here
        return {'sentiment': 'positive', 'confidence': 0.8}

    async def process_routing(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Process routing task"""
        return self.router.route_request(data)