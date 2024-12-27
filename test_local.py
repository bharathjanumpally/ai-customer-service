import requests
import json
import time

def test_system():
    # Test health endpoint
    try:
        health_response = requests.get("http://localhost:8000/health")
        print("\nHealth Check Response:", health_response.json())
    except Exception as e:
        print("Error checking health:", e)
        return

    # Test task submission
    test_tasks = [
        {
            "type": "sentiment_analysis",
            "data": {"text": "I love this product, it's amazing!"}
        },
        {
            "type": "routing",
            "data": {"channel": "email", "priority": "high"}
        }
    ]

    print("\nSubmitting test tasks...")
    for task in test_tasks:
        try:
            response = requests.post(
                "http://localhost:8000/task",
                json=task
            )
            print(f"\nTask Response ({task['type']}):", response.json())
        except Exception as e:
            print(f"Error submitting {task['type']} task:", e)

if __name__ == "__main__":
    test_system()