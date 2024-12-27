import numpy as np
from sklearn.ensemble import RandomForestClassifier
from typing import Dict, Any

class IntelligentRouter:
    """
    Intelligent routing system that determines the best path for customer queries
    based on multiple factors as specified in the paper:
    - Channel type (voice, chat, email)
    - Query intent
    - Priority level
    - Current agent availability
    - Customer history
    """
    
    def __init__(self):
        self.model = RandomForestClassifier(n_estimators=100)
        self.route_priorities = {
            'high': 3,
            'medium': 2,
            'low': 1
        }
        
    def preprocess_features(self, data: Dict[str, Any]) -> np.ndarray:
        """
        Process input features for routing decision
        """
        # Convert channel to numeric
        channel_map = {'voice': 0, 'chat': 1, 'email': 2}
        channel = channel_map.get(data.get('channel', 'email'))
        
        # Get priority numeric value
        priority = self.route_priorities.get(data.get('priority', 'low'))
        
        # Convert type to numeric
        type_map = {'complaint': 3, 'inquiry': 2, 'support': 2, 'feedback': 1}
        query_type = type_map.get(data.get('type', 'inquiry'))
        
        # Combine features
        features = np.array([
            channel,
            priority,
            query_type,
            data.get('customer_history_length', 0),
            data.get('agent_availability', 1.0)
        ]).reshape(1, -1)
        
        return features
    
    def train(self, X, y):
        """Train the routing model"""
        self.model.fit(X, y)
    
    def route_request(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Route a customer request to appropriate handler
        Returns routing decision including:
        - Assigned agent/department
        - Priority level
        - Estimated response time
        """
        features = self.preprocess_features(data)
        route_decision = self.model.predict(features)[0]
        
        # Map routing decision to actual handler
        routing_map = {
            0: "general_support",
            1: "technical_support",
            2: "customer_service",
            3: "priority_support",
            4: "automated_response"
        }
        
        # Calculate estimated response time based on priority
        priority = data.get('priority', 'low')
        est_response_time = {
            'high': '15 minutes',
            'medium': '1 hour',
            'low': '24 hours'
        }.get(priority)
        
        return {
            'assigned_to': routing_map.get(route_decision, "general_support"),
            'priority': priority,
            'estimated_response_time': est_response_time,
            'channel': data.get('channel'),
            'routing_confidence': float(max(self.model.predict_proba(features)[0]))
        }
    
    def update_routing_model(self, feedback: Dict[str, Any]):
        """Update routing model based on feedback"""
        if feedback.get('was_correct_routing', True):
            # Potentially implement online learning here
            pass