import torch
import torch.nn as nn
import torch.nn.functional as F
from .nlp_functions import SoftmaxClassifier
import numpy as np

class SentimentAnalyzer(nn.Module):
    def __init__(self, input_size, hidden_size, num_classes):
        super(SentimentAnalyzer, self).__init__()
        self.layer1 = nn.Linear(input_size, hidden_size)
        self.layer2 = nn.Linear(hidden_size, hidden_size)
        self.layer3 = nn.Linear(hidden_size, num_classes)
        
        # Add softmax classifier from paper
        self.softmax_classifier = SoftmaxClassifier(hidden_size, num_classes)
        
    def feature_extraction(self, x):
        """Extract features φ(x) as per paper notation"""
        x = F.relu(self.layer1(x))
        x = F.relu(self.layer2(x))
        return x
        
    def forward(self, x):
        # Extract features φ(x)
        features = self.feature_extraction(x)
        
        # Apply final linear layer
        logits = self.layer3(features)
        
        # Use paper's softmax implementation
        if self.training:
            # During training, use manual softmax for gradient descent updates
            features_np = features.detach().numpy()
            probs_np = self.softmax_classifier.softmax(features_np.T)
            return torch.from_numpy(probs_np.T).float()
        else:
            # During inference, use PyTorch's softmax
            return F.softmax(logits, dim=1)
            
    def update_weights(self, x, y):
        """
        Implement paper's gradient descent update
        """
        # Extract features
        features = self.feature_extraction(x)
        features_np = features.detach().numpy()
        
        # Update softmax classifier weights using paper's update rule
        for i in range(len(y)):
            self.softmax_classifier.gradient_descent_update(
                features_np[i],
                y[i].item()
            )