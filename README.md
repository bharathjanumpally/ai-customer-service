# AI-Driven Multi-Channel Customer Service Platform

This project implements an AI-driven customer service platform that handles multiple communication channels (voice, chat, email) with features like sentiment analysis, intelligent routing, and distributed processing.

## Features

- Multi-channel support (voice, chat, email)
- Real-time sentiment analysis
- Intelligent request routing
- Distributed processing with Redis
- Performance monitoring and metrics
- Scalable worker architecture

## System Requirements

- Python 3.11 or later
- Redis server
- Virtual environment (venv)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/bharathjanumpally/ai-customer-service.git
cd ai-customer-service
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install numpy==1.24.3 torch==2.1.0 pydantic-settings fastapi uvicorn redis pandas matplotlib seaborn scikit-learn
```

## Running the System

1. Start Redis Server:
```bash
# On Mac
brew services start redis

# On Linux
sudo service redis-server start

# Verify Redis is running
redis-cli ping  # Should return "PONG"
```

2. Start Workers (open multiple terminals):
```bash
# Terminal 1
python start_worker.py 0

# Terminal 2
python start_worker.py 1

# Terminal 3
python start_worker.py 2
```

3. Run the Analysis:
```bash
# In a new terminal
python run_integrated_analysis.py
```

4. Monitor System Status:
```bash
python check_system.py
```

## Project Structure

```
ai-customer-service/
├── src/
│   ├── data/
│   │   └── data_generator.py
│   ├── models/
│   │   ├── sentiment_analyzer.py
│   │   └── intelligent_router.py
│   ├── distributed/
│   │   ├── worker.py
│   │   ├── queue_manager.py
│   │   └── api.py
│   └── utils/
│       └── metrics.py
├── tests/
├── requirements.txt
└── README.md
```

## Key Components

1. **Sentiment Analyzer**: 
   - Implements paper's Softmax Function
   - Uses neural network for sentiment classification
   - Handles real-time text analysis

2. **Intelligent Router**:
   - Routes requests based on multiple factors
   - Implements priority-based routing
   - Handles load balancing

3. **Distributed System**:
   - Redis-based task distribution
   - Multiple worker support
   - Scalable architecture

## Monitoring

To check system status and worker health:
```bash
# Check system status
python check_system.py

# Monitor workers
python check_workers.py
```

## Troubleshooting

1. If Redis connection fails:
   ```bash
   brew services restart redis
   ```

2. If workers aren't starting:
   - Check Redis is running
   - Verify port 6379 is available
   - Check for Python version compatibility

3. Common Issues:
   - Redis connection refused: Start/restart Redis server
   - Import errors: Verify all dependencies are installed
   - Worker not processing: Check Redis queues and worker status

## Reference

Based on the paper: "AI-Driven Multi-Channel Customer Service Optimization Platform" by Bharath Kumar Reddy Janumpally

## License

MIT License

## Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request