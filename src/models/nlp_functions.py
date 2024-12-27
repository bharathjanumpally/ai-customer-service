import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np

class SoftmaxClassifier:
    def __init__(self, input_dim, num_classes, learning_rate=0.01):
        """
        Implementation of Softmax Classification as per paper:
        P(y|x) = exp(θ_y^T φ(x)) / Σ(exp(θ_{y'}^T φ(x)))
        
        Args:
            input_dim: Dimension of input features φ(x)
            num_classes: Number of output classes
            learning_rate: Learning rate η for gradient descent
        """
        self.input_dim = input_dim
        self.num_classes = num_classes
        self.learning_rate = learning_rate
        # Initialize θ parameters
        self.theta = np.random.randn(num_classes, input_dim) * 0.01
        
    def softmax(self, x):
        """
        Compute softmax probabilities:
        P(y|x) = exp(θ_y^T φ(x)) / Σ(exp(θ_{y'}^T φ(x)))
        """
        # Compute logits: θ_y^T φ(x)
        logits = np.dot(self.theta, x)
        # Subtract max for numerical stability
        logits = logits - np.max(logits, axis=0, keepdims=True)
        exp_logits = np.exp(logits)
        # Compute softmax probabilities
        probabilities = exp_logits / np.sum(exp_logits, axis=0, keepdims=True)
        return probabilities
        
    def gradient_descent_update(self, x, y):
        """
        Implement gradient descent update rule:
        w_{t+1} = w_t - η ∇_w L(w)
        
        Args:
            x: Input features φ(x)
            y: True class label
        """
        # Forward pass to get probabilities
        probs = self.softmax(x)
        
        # Compute gradient of loss with respect to θ
        gradient = np.zeros_like(self.theta)
        for i in range(self.num_classes):
            indicator = 1 if i == y else 0
            gradient[i] = (probs[i] - indicator) * x
            
        # Update rule: w_{t+1} = w_t - η ∇_w L(w)
        self.theta = self.theta - self.learning_rate * gradient
        
    def predict(self, x):
        """Predict class with highest probability"""
        probs = self.softmax(x)
        return np.argmax(probs)