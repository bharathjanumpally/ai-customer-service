# API Documentation

## Overview
The AI Customer Service Platform provides RESTful APIs for task management, worker coordination, and system monitoring.

## Base URL
```
http://localhost:8000
```

## Authentication
```python
headers = {
    'Authorization': 'Bearer <your_token>',
    'Content-Type': 'application/json'
}
```

## API Endpoints

### 1. Task Management

#### Submit Task
```http
POST /task
```

Request Body:
```json
{
    "type": "sentiment_analysis",
    "data": {
        "text": "Great customer service experience!",
        "channel": "chat",
        "customer_id": "CUST123",
        "priority": "high"
    }
}
```

Response:
```json
{
    "task_id": "task_1234567890",
    "status": "accepted",
    "queue_position": 1,
    "estimated_process_time": "2s"
}
```

#### Get Task Status
```http
GET /task/{task_id}
```

Response:
```json
{
    "task_id": "task_1234567890",
    "status": "completed",
    "result": {
        "sentiment": "positive",
        "confidence": 0.95,
        "processing_time": "1.5s"
    }
}
```

### 2. Worker Management

#### Get Worker Status
```http
GET /workers
```

Response:
```json
{
    "total_workers": 3,
    "active_workers": 2,
    "workers": [
        {
            "id": 0,
            "status": "active",
            "tasks_processed": 150,
            "uptime": "2h 30m",
            "current_load": 0.75
        },
        {
            "id": 1,
            "status": "active",
            "tasks_processed": 140,
            "uptime": "2h 30m",
            "current_load": 0.65
        },
        {
            "id": 2,
            "status": "idle",
            "tasks_processed": 130,
            "uptime": "2h 30m",
            "current_load": 0.0
        }
    ]
}
```

#### Start Worker
```http
POST /workers
```

Request Body:
```json
{
    "worker_id": 3,
    "config": {
        "max_tasks": 100,
        "timeout": 30
    }
}
```

Response:
```json
{
    "worker_id": 3,
    "status": "started",
    "endpoint": "ws://localhost:8000/worker/3"
}
```

### 3. System Monitoring

#### System Health
```http
GET /health
```

Response:
```json
{
    "status": "healthy",
    "components": {
        "redis": {
            "status": "up",
            "latency": "2ms"
        },
        "workers": {
            "active": 3,
            "total": 3
        },
        "queues": {
            "tasks": {
                "length": 10,
                "processing_rate": "50/sec"
            },
            "results": {
                "length": 5,
                "processing_rate": "45/sec"
            }
        }
    },
    "metrics": {
        "cpu_usage": "45%",
        "memory_usage": "60%",
        "average_response_time": "100ms"
    }
}
```

#### Performance Metrics
```http
GET /metrics
```

Response:
```json
{
    "response_times": {
        "p50": 100,
        "p95": 200,
        "p99": 300
    },
    "throughput": {
        "requests_per_second": 50,
        "tasks_processed": 1000
    },
    "error_rates": {
        "total": 0.01,
        "by_type": {
            "timeout": 0.005,
            "processing": 0.003,
            "validation": 0.002
        }
    }
}
```

### 4. Channel Management

#### Channel Status
```http
GET /channels
```

Response:
```json
{
    "channels": {
        "chat": {
            "status": "active",
            "current_load": 45,
            "response_time": "2s"
        },
        "voice": {
            "status": "active",
            "current_load": 30,
            "response_time": "1s"
        },
        "email": {
            "status": "active",
            "current_load": 25,
            "response_time": "5m"
        }
    }
}
```

## WebSocket API

### Worker Connection
```javascript
const ws = new WebSocket('ws://localhost:8000/worker/{worker_id}');

ws.onmessage = (event) => {
    const task = JSON.parse(event.data);
    // Process task
};
```

### Task Updates
```javascript
const ws = new WebSocket('ws://localhost:8000/tasks/updates');

ws.onmessage = (event) => {
    const update = JSON.parse(event.data);
    console.log('Task Update:', update);
};
```

## Error Handling

### Error Response Format
```json
{
    "error": {
        "code": "ERROR_CODE",
        "message": "Human readable error message",
        "details": {
            "field": "Additional error context"
        }
    }
}
```

### Common Error Codes
- `TASK_NOT_FOUND`: Task ID doesn't exist
- `WORKER_OFFLINE`: Worker is not available
- `QUEUE_FULL`: System at capacity
- `INVALID_INPUT`: Request validation failed
- `UNAUTHORIZED`: Authentication failed

## Rate Limiting

Headers:
```http
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1640995200
```

## Example Usage

### Python
```python
import requests

def submit_task(text):
    response = requests.post(
        'http://localhost:8000/task',
        json={
            'type': 'sentiment_analysis',
            'data': {
                'text': text,
                'channel': 'chat'
            }
        }
    )
    return response.json()

# Submit task
result = submit_task("Great service!")
print(result)
```

### Node.js
```javascript
const axios = require('axios');

async function submitTask(text) {
    const response = await axios.post('http://localhost:8000/task', {
        type: 'sentiment_analysis',
        data: {
            text: text,
            channel: 'chat'
        }
    });
    return response.data;
}

// Submit task
submitTask("Great service!")
    .then(console.log)
    .catch(console.error);
```

## Best Practices

1. Task Submission:
   - Include task priority
   - Set appropriate timeouts
   - Handle rate limits

2. Error Handling:
   - Implement exponential backoff
   - Validate inputs
   - Handle all error responses

3. Monitoring:
   - Regular health checks
   - Monitor rate limits
   - Track error rates

4. Performance:
   - Use WebSocket for real-time updates
   - Batch requests when possible
   - Implement caching