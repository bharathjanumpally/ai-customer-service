import asyncio
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import threading
import time
import torch
from typing import Dict, Any

# Project imports
from src.models.sentiment_analyzer import SentimentAnalyzer
from src.models.intelligent_router import IntelligentRouter
from src.distributed.worker import Worker
from src.distributed.main import start_distributed_system
from src.distributed.queue_manager import QueueManager

class IntegratedAnalysis:
    def __init__(self):
        self.sentiment_analyzer = SentimentAnalyzer(input_size=100, hidden_size=64, num_classes=3)
        self.router = IntelligentRouter()
        self.queue_manager = QueueManager()
        
    async def start_system(self):
        """Start the distributed system with explicit worker initialization"""
        print("Starting distributed system...")
        
        # Initialize workers
        self.workers = []
        for worker_id in range(3):  # Start 3 workers
            try:
                worker = Worker(worker_id)
                self.workers.append(worker)
                print(f"Initialized worker {worker_id}")
            except Exception as e:
                print(f"Error initializing worker {worker_id}: {e}")
        
        # Start workers in separate threads
        self.worker_threads = []
        for worker in self.workers:
            thread = threading.Thread(target=worker.run)
            thread.daemon = True
            thread.start()
            self.worker_threads.append(thread)
            print(f"Started worker thread for worker {worker.worker_id}")
        
        # Wait for workers to initialize
        await asyncio.sleep(2)
        
        # Verify workers are running
        print("\nVerifying worker status:")
        for worker in self.workers:
            print(f"Worker {worker.worker_id} is running: {worker.running}")
        
    def generate_channel_data(self, channel_type: str, n_samples: int) -> pd.DataFrame:
        """Generate data for specific channel with all required fields"""
        # Common customer messages for each channel
        message_templates = {
            'voice': [
                "I need help with my account",
                "There's a problem with my service",
                "I'd like to upgrade my plan",
                "I'm having technical difficulties",
                "Can you explain my bill?"
            ],
            'chat': [
                "How do I reset my password?",
                "Where can I find my order status?",
                "I need help with the website",
                "Can you help with product selection?",
                "I have a question about shipping"
            ],
            'email': [
                "Following up on my previous request",
                "Request for documentation",
                "Feedback on recent service",
                "Account modification request",
                "General inquiry about services"
            ]
        }
        
        # Generate base data
        data = {
            'timestamp': [datetime.now() - timedelta(minutes=x) for x in range(n_samples)],
            'channel': [channel_type] * n_samples,
            'message': np.random.choice(message_templates[channel_type], n_samples),
            'customer_id': [f'CUST-{i:04d}' for i in range(n_samples)],
            'priority': np.random.choice(['high', 'medium', 'low'], n_samples),
            'type': np.random.choice(['inquiry', 'complaint', 'support', 'feedback'], n_samples),
            'response_time': np.random.exponential(2, n_samples),
            'satisfaction_score': np.random.normal(4, 1, n_samples).clip(1, 5),
            'customer_history_length': np.random.randint(0, 10, n_samples),
            'agent_availability': np.random.uniform(0.5, 1.0, n_samples)
        }
        
        return pd.DataFrame(data)

    
    async def process_interaction(self, interaction: Dict[str, Any]):
        """Process single interaction through the system with debug info"""
        try:
            # Create sentiment analysis task with unique ID
            task_id = f"task_{time.time()}_{interaction['customer_id']}"
            sentiment_task = {
                "id": f"{task_id}_sentiment",
                "type": "sentiment_analysis",
                "data": {
                    "text": interaction['message'],
                    "channel": interaction['channel']
                }
            }
            
            print(f"Submitting sentiment task: {sentiment_task['id']}")
            self.queue_manager.push_task('tasks', sentiment_task)
            
            # Create routing task
            routing_task = {
                "id": f"{task_id}_routing",
                "type": "routing",
                "data": {
                    "channel": interaction['channel'],
                    "priority": interaction['priority'],
                    "type": interaction['type'],
                    "customer_history_length": interaction['customer_history_length'],
                    "agent_availability": interaction['agent_availability']
                }
            }
            
            print(f"Submitting routing task: {routing_task['id']}")
            self.queue_manager.push_task('tasks', routing_task)
            
            # Wait for results with debug info
            print(f"Waiting for sentiment result: {sentiment_task['id']}")
            sentiment_result = await self.wait_for_result('results')
            if sentiment_result is None:
                print(f"Timeout waiting for sentiment result: {sentiment_task['id']}")
                sentiment_result = {"error": "timeout"}
                
            print(f"Waiting for routing result: {routing_task['id']}")
            routing_result = await self.wait_for_result('results')
            if routing_result is None:
                print(f"Timeout waiting for routing result: {routing_task['id']}")
                routing_result = {"error": "timeout"}
            
            return {
                'sentiment_result': sentiment_result,
                'routing_result': routing_result,
                'original_interaction': interaction
            }
        except Exception as e:
            print(f"Error in process_interaction: {e}")
            return {
                'error': str(e),
                'original_interaction': interaction
            }
        
    async def wait_for_result(self, queue_name: str, timeout: int = 30):
        """Wait for result from queue with timeout and debugging"""
        start_time = time.time()
        while time.time() - start_time < timeout:
            result = self.queue_manager.pop_task(queue_name)
            if result:
                print(f"Received result from queue {queue_name}")
                return result
            await asyncio.sleep(0.1)
            if (time.time() - start_time) % 5 == 0:  # Log every 5 seconds
                print(f"Still waiting for result... ({int(time.time() - start_time)}s)")
        return None

    def analyze_results(self, results: list) -> Dict[str, Any]:
        """Analyze processing results"""
        metrics = {
            'sentiment_distribution': {},
            'routing_distribution': {},
            'response_times': [],
            'channel_performance': {},
            'routing_accuracy': 0.0
        }
        
        for result in results:
            if 'sentiment_result' in result:
                sentiment = result['sentiment_result'].get('sentiment', 'unknown')
                metrics['sentiment_distribution'][sentiment] = \
                    metrics['sentiment_distribution'].get(sentiment, 0) + 1
            
            if 'routing_result' in result:
                route = result['routing_result'].get('assigned_to', 'unknown')
                metrics['routing_distribution'][route] = \
                    metrics['routing_distribution'].get(route, 0) + 1
                
            # Channel specific metrics
            channel = result['original_interaction']['channel']
            if channel not in metrics['channel_performance']:
                metrics['channel_performance'][channel] = {
                    'total_interactions': 0,
                    'avg_response_time': 0.0,
                    'satisfaction_score': 0.0
                }
            
            channel_metrics = metrics['channel_performance'][channel]
            channel_metrics['total_interactions'] += 1
            
        return metrics

    def create_visualizations(self, data: pd.DataFrame, metrics: Dict[str, Any]):
        """Create comprehensive visualizations"""
        plt.style.use('seaborn')
        fig = plt.figure(figsize=(20, 15))
        
        # 1. Sentiment Distribution
        plt.subplot(3, 2, 1)
        sentiment_df = pd.DataFrame(list(metrics['sentiment_distribution'].items()),
                                  columns=['Sentiment', 'Count'])
        sns.barplot(x='Sentiment', y='Count', data=sentiment_df)
        plt.title('Sentiment Distribution Across Channels')
        
        # 2. Routing Distribution
        plt.subplot(3, 2, 2)
        routing_df = pd.DataFrame(list(metrics['routing_distribution'].items()),
                                columns=['Route', 'Count'])
        sns.barplot(x='Route', y='Count', data=routing_df)
        plt.title('Routing Distribution')
        plt.xticks(rotation=45)
        
        # 3. Channel Performance
        plt.subplot(3, 2, 3)
        channel_df = pd.DataFrame(metrics['channel_performance']).T
        channel_df['total_interactions'].plot(kind='bar')
        plt.title('Interactions by Channel')
        
        # 4. Response Time Distribution
        plt.subplot(3, 2, 4)
        sns.boxplot(x='channel', y='response_time', data=data)
        plt.title('Response Time by Channel')
        
        # 5. System Performance Over Time
        plt.subplot(3, 2, (5, 6))
        data['hour'] = pd.to_datetime(data['timestamp']).dt.hour
        hourly_metrics = data.groupby('hour')['satisfaction_score'].mean()
        plt.plot(hourly_metrics.index, hourly_metrics.values, marker='o')
        plt.title('System Performance by Hour')
        plt.xlabel('Hour of Day')
        plt.ylabel('Average Satisfaction Score')
        
        plt.tight_layout()
        plt.savefig('integrated_analysis_results.png')
        print("\nVisualization saved as 'integrated_analysis_results.png'")
        return fig

async def main():
    # Initialize analysis
    analysis = IntegratedAnalysis()
    
    # Start distributed system
    await analysis.start_system()

        # Verify system health
    print("\nChecking system health...")
    queue_length = analysis.queue_manager.get_queue_length('tasks')
    worker_count = len([w for w in analysis.workers if w.running])
    print(f"Active workers: {worker_count}")
    print(f"Current queue length: {queue_length}")

    if worker_count == 0:
        print("No workers running. Please check worker initialization.")
        return
    
    print("\nGenerating channel data...")
    # Generate larger samples
    voice_data = analysis.generate_channel_data('voice', 10)  # Increased from 10
    chat_data = analysis.generate_channel_data('chat', 10)    # Increased from 10
    email_data = analysis.generate_channel_data('email', 10)  # Increased from 10
    
    all_data = pd.concat([voice_data, chat_data, email_data])
    print(f"Total interactions to process: {len(all_data)}")
    
    print("\nProcessing interactions through the system...")
    results = []
    batch_size = 100  # Process in batches of 100
    
    # Process in batches
    for i in range(0, len(all_data), batch_size):
        batch = all_data.iloc[i:i+batch_size]
        batch_results = []
        
        for _, interaction in batch.iterrows():
            try:
                result = await analysis.process_interaction(interaction.to_dict())
                batch_results.append(result)
                if len(results) % 100 == 0:  # Print progress every 100 interactions
                    print(f"Processed {len(results)}/{len(all_data)} interactions...")
            except Exception as e:
                print(f"Error processing interaction: {e}")
                continue
        
        results.extend(batch_results)
        
        # Add a small delay between batches to prevent overloading
        await asyncio.sleep(0.1)
    
    print(f"\nSuccessfully processed {len(results)} interactions")
    
    # Analyze results
    print("\nAnalyzing results...")
    metrics = analysis.analyze_results(results)
    
    # Create visualizations
    print("\nCreating visualizations...")
    analysis.create_visualizations(all_data, metrics)
    
    print("\nAnalysis complete. Results saved to 'integrated_analysis_results.png'")
    return all_data, results, metrics

if __name__ == "__main__":
    asyncio.run(main())