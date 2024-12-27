class PerformanceMetrics:
    def __init__(self):
        self.metrics = {}
        
    def calculate_metrics(self, data):
        self.metrics = {
            'average_response_time': data['response_time'].mean(),
            'customer_satisfaction': data['satisfaction_score'].mean(),
            'system_uptime': 99.98,  # Simulated value
            'accuracy': data['satisfaction_score'].apply(lambda x: 1 if x >= 4 else 0).mean() * 100
        }
        return self.metrics