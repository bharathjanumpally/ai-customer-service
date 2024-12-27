from src.data.data_generator import generate_customer_interactions
from src.models.sentiment_analyzer import SentimentAnalyzer
from src.models.intelligent_router import IntelligentRouter
from src.utils.metrics import PerformanceMetrics
from src.distributed.main import start_distributed_system
import asyncio
import threading

class CustomerServicePlatform:
    def __init__(self):
        self.data = None
        self.sentiment_analyzer = SentimentAnalyzer(10, 64, 3)
        self.router = IntelligentRouter()
        self.metrics = PerformanceMetrics()
        
    def ingest_data(self, n_samples):
        self.data = generate_customer_interactions(n_samples)
        return self.data
        
    def process_data(self):
        return self.metrics.calculate_metrics(self.data)

def run_experiment(distributed=False):
    if distributed:
        # Start distributed system in a separate thread
        dist_thread = threading.Thread(target=start_distributed_system)
        dist_thread.start()
    
    platform = CustomerServicePlatform()
    print("Generating customer interaction data...")
    data = platform.ingest_data(1000)
    print("\nProcessing data and calculating metrics...")
    metrics = platform.process_data()
    
    if distributed:
        print("\nDistributed system is running. Use API endpoints for task submission.")
        print("Health check: http://localhost:8000/health")
        print("Submit tasks: http://localhost:8000/task")
    
    return platform, metrics

if __name__ == "__main__":
    platform, metrics = run_experiment(distributed=True)