import numpy as np
import pandas as pd
from datetime import datetime, timedelta

def generate_customer_interactions(n_samples=1000):
    """Generate synthetic customer interaction data"""
    channels = ['voice', 'chat', 'email']
    sentiments = ['positive', 'negative', 'neutral']
    intents = ['complaint', 'inquiry', 'request']
    
    data = {
        'timestamp': [datetime.now() - timedelta(minutes=x) for x in range(n_samples)],
        'channel': np.random.choice(channels, n_samples),
        'customer_id': np.random.randint(1000, 9999, n_samples),
        'message_length': np.random.normal(100, 30, n_samples),
        'response_time': np.random.exponential(2, n_samples),
        'sentiment': np.random.choice(sentiments, n_samples),
        'intent': np.random.choice(intents, n_samples),
        'satisfaction_score': np.random.normal(4, 1, n_samples).clip(1, 5),
    }
    return pd.DataFrame(data)