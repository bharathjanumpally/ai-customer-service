import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
from ..models.sentiment_analyzer import SentimentAnalyzer
import numpy as np

class SentimentDataset(Dataset):
    def __init__(self, texts, labels):
        self.texts = texts
        self.labels = labels
        
    def __len__(self):
        return len(self.texts)
        
    def __getitem__(self, idx):
        return self.texts[idx], self.labels[idx]

def train_sentiment_analyzer(model, train_loader, num_epochs=10):
    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(model.parameters())
    
    for epoch in range(num_epochs):
        total_loss = 0
        for batch_x, batch_y in train_loader:
            # Forward pass
            outputs = model(batch_x)
            loss = criterion(outputs, batch_y)
            
            # Backward pass and optimize
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            
            # Apply paper's gradient descent update
            model.update_weights(batch_x, batch_y)
            
            total_loss += loss.item()
            
        avg_loss = total_loss / len(train_loader)
        print(f'Epoch [{epoch+1}/{num_epochs}], Loss: {avg_loss:.4f}')

def main():
    # Example usage
    input_size = 100
    hidden_size = 64
    num_classes = 3  # positive, negative, neutral
    
    # Create model
    model = SentimentAnalyzer(input_size, hidden_size, num_classes)
    
    # Generate sample data
    num_samples = 1000
    X = torch.randn(num_samples, input_size)
    y = torch.randint(0, num_classes, (num_samples,))
    
    # Create data loader
    dataset = SentimentDataset(X, y)
    train_loader = DataLoader(dataset, batch_size=32, shuffle=True)
    
    # Train model
    train_sentiment_analyzer(model, train_loader)
    
if __name__ == "__main__":
    main()