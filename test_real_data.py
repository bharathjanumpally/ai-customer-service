import requests
import json
import time
import pandas as pd
import random
from datetime import datetime, timedelta

def generate_realistic_customer_data():
    # Common customer service scenarios
    scenarios = [
        {
            "type": "complaint",
            "messages": [
                "My order hasn't arrived yet and it's been 5 days",
                "I received a damaged product",
                "The quality is not what I expected",
                "I was charged twice for my order",
                "The product doesn't match the description"
            ],
            "priority": "high"
        },
        {
            "type": "inquiry",
            "messages": [
                "What's the status of my order?",
                "Do you ship internationally?",
                "How long does delivery usually take?",
                "Are there any ongoing promotions?",
                "What's your return policy?"
            ],
            "priority": "medium"
        },
        {
            "type": "support",
            "messages": [
                "How do I reset my password?",
                "The app keeps crashing",
                "I can't login to my account",
                "Where do I find my order history?",
                "How do I update my shipping address?"
            ],
            "priority": "medium"
        },
        {
            "type": "feedback",
            "messages": [
                "Great service, very helpful support team!",
                "The product exceeded my expectations",
                "Quick delivery and perfect packaging",
                "Very dissatisfied with the quality",
                "Amazing customer support experience"
            ],
            "priority": "low"
        }
    ]

    channels = ['email', 'chat', 'voice']
    
    # Generate 20 realistic interactions
    interactions = []
    
    for _ in range(20):
        scenario = random.choice(scenarios)
        channel = random.choice(channels)
        timestamp = datetime.now() - timedelta(minutes=random.randint(1, 60))
        
        interaction = {
            "timestamp": timestamp.strftime("%Y-%m-%d %H:%M:%S"),
            "channel": channel,
            "type": scenario["type"],
            "message": random.choice(scenario["messages"]),
            "priority": scenario["priority"],
            "customer_id": f"CUST-{random.randint(1000, 9999)}"
        }
        interactions.append(interaction)
    
    return interactions

def process_customer_interactions():
    interactions = generate_realistic_customer_data()
    
    print("\nProcessing customer service interactions...")
    print(f"Total interactions to process: {len(interactions)}")
    
    success_count = 0
    sentiment_results = []
    routing_results = []
    
    for interaction in interactions:
        # Submit for sentiment analysis
        sentiment_task = {
            "type": "sentiment_analysis",
            "data": {"text": interaction["message"]}
        }
        
        # Submit for routing
        routing_task = {
            "type": "routing",
            "data": {
                "channel": interaction["channel"],
                "type": interaction["type"],
                "priority": interaction["priority"]
            }
        }
        
        try:
            # Send tasks to API
            sentiment_response = requests.post(
                "http://localhost:8000/task",
                json=sentiment_task
            )
            routing_response = requests.post(
                "http://localhost:8000/task",
                json=routing_task
            )
            
            if sentiment_response.status_code == 200 and routing_response.status_code == 200:
                success_count += 1
                print(f"\nProcessed interaction {success_count}:")
                print(f"Channel: {interaction['channel']}")
                print(f"Type: {interaction['type']}")
                print(f"Message: {interaction['message']}")
                print(f"Priority: {interaction['priority']}")
                print("-" * 50)
        
        except Exception as e:
            print(f"Error processing interaction: {e}")
    
    print(f"\nSuccessfully processed {success_count} out of {len(interactions)} interactions")
    
    # Calculate statistics
    stats = pd.DataFrame(interactions)
    print("\nInteraction Statistics:")
    print("\nChannel Distribution:")
    print(stats['channel'].value_counts())
    print("\nType Distribution:")
    print(stats['type'].value_counts())
    print("\nPriority Distribution:")
    print(stats['priority'].value_counts())

if __name__ == "__main__":
    # Check if system is healthy
    try:
        health_response = requests.get("http://localhost:8000/health")
        if health_response.status_code == 200:
            print("System is healthy, starting interaction processing...")
            process_customer_interactions()
        else:
            print("System health check failed. Please ensure the service is running.")
    except Exception as e:
        print(f"Error connecting to the service: {e}")
        print("Please ensure the service is running (python run_local.py)")