import torch
import torch.nn as nn
import torch.optim as optim
import time
import copy
import numpy as np
from tqdm import tqdm

def train_model(model, train_loader, val_loader, criterion, optimizer, scheduler=None, 
                device='cuda', num_epochs=10, early_stopping_patience=5, save_path='model.pt'):
    """
    Train a PyTorch model with early stopping.
    
    Args:
        model: PyTorch model to train
        train_loader: DataLoader for training data
        val_loader: DataLoader for validation data
        criterion: Loss function
        optimizer: Optimizer
        scheduler: Learning rate scheduler (optional)
        device: Device to train on ('cuda' or 'cpu')
        num_epochs: Maximum number of epochs to train for
        early_stopping_patience: Number of epochs to wait for improvement before stopping
        save_path: Path to save the best model to
    
    Returns:
        model: The trained model
        history: Dictionary containing training history
    """
    # Move model to device
    model = model.to(device)
    
    # Initialize variables for early stopping
    best_model_weights = copy.deepcopy(model.state_dict())
    best_acc = 0.0
    epochs_no_improve = 0
    
    # Initialize history dictionary to store metrics
    history = {
        'train_loss': [],
        'val_loss': [],
        'train_acc': [],
        'val_acc': []
    }
    
    # Track total training time
    start_time = time.time()
    
    print(f"Starting training on {device}...")
    
    for epoch in range(num_epochs):
        print(f'Epoch {epoch+1}/{num_epochs}')
        print('-' * 10)
        
        # Training phase
        model.train()
        running_loss = 0.0
        running_corrects = 0
        
        # Wrap train_loader with tqdm for progress bar
        train_bar = tqdm(train_loader, desc="Training")
        
        for inputs, labels in train_bar:
            inputs = inputs.to(device)
            labels = labels.to(device)
            
            # Zero the parameter gradients
            optimizer.zero_grad()
            
            # Forward pass
            with torch.set_grad_enabled(True):
                outputs = model(inputs)
                _, preds = torch.max(outputs, 1)
                loss = criterion(outputs, labels)
                
                # Backward pass + optimize
                loss.backward()
                optimizer.step()
            
            # Statistics
            running_loss += loss.item() * inputs.size(0)
            running_corrects += torch.sum(preds == labels.data)
            
            # Update progress bar
            train_bar.set_postfix(loss=loss.item())
        
        if scheduler is not None:
            scheduler.step()
        
        epoch_loss = running_loss / len(train_loader.dataset)
        epoch_acc = running_corrects.double() / len(train_loader.dataset)
        
        print(f'Train Loss: {epoch_loss:.4f} Acc: {epoch_acc:.4f}')
        
        history['train_loss'].append(epoch_loss)
        history['train_acc'].append(epoch_acc.item())
        
        # Validation phase
        model.eval()
        running_loss = 0.0
        running_corrects = 0
        
        # Wrap val_loader with tqdm for progress bar
        val_bar = tqdm(val_loader, desc="Validation")
        
        with torch.no_grad():
            for inputs, labels in val_bar:
                inputs = inputs.to(device)
                labels = labels.to(device)
                
                # Forward pass
                outputs = model(inputs)
                _, preds = torch.max(outputs, 1)
                loss = criterion(outputs, labels)
                
                # Statistics
                running_loss += loss.item() * inputs.size(0)
                running_corrects += torch.sum(preds == labels.data)
                
                # Update progress bar
                val_bar.set_postfix(loss=loss.item())
        
        epoch_loss = running_loss / len(val_loader.dataset)
        epoch_acc = running_corrects.double() / len(val_loader.dataset)
        
        print(f'Val Loss: {epoch_loss:.4f} Acc: {epoch_acc:.4f}')
        
        history['val_loss'].append(epoch_loss)
        history['val_acc'].append(epoch_acc.item())
        
        # Check if this is the best model so far
        if epoch_acc > best_acc:
            best_acc = epoch_acc
            best_model_weights = copy.deepcopy(model.state_dict())
            epochs_no_improve = 0
            
            # Save the best model
            torch.save(best_model_weights, save_path)
            print(f"Best model saved with accuracy: {best_acc:.4f}")
        else:
            epochs_no_improve += 1
            print(f"No improvement for {epochs_no_improve} epochs")
        
        # Early stopping check
        if epochs_no_improve >= early_stopping_patience:
            print(f"Early stopping triggered after {epoch+1} epochs")
            break
    
    # Calculate total training time
    total_time = time.time() - start_time
    print(f'Training completed in {total_time // 60:.0f}m {total_time % 60:.0f}s')
    print(f'Best validation accuracy: {best_acc:.4f}')
    
    # Load best model weights
    model.load_state_dict(best_model_weights)
    
    return model, history


def evaluate_model(model, test_loader, device='cuda'):
    """
    Evaluate a trained model on a test set.
    
    Args:
        model: Trained PyTorch model
        test_loader: DataLoader for test data
        device: Device to evaluate on
    
    Returns:
        accuracy: Accuracy on test set
        predictions: List of predictions
        true_labels: List of true labels
    """
    model.eval()
    model = model.to(device)
    
    all_preds = []
    all_labels = []
    correct = 0
    total = 0
    
    with torch.no_grad():
        for inputs, labels in tqdm(test_loader, desc="Evaluating"):
            inputs = inputs.to(device)
            labels = labels.to(device)
            
            outputs = model(inputs)
            _, preds = torch.max(outputs, 1)
            
            total += labels.size(0)
            correct += (preds == labels).sum().item()
            
            all_preds.extend(preds.cpu().numpy())
            all_labels.extend(labels.cpu().numpy())
    
    accuracy = correct / total
    print(f'Test Accuracy: {accuracy:.4f}')
    
    return accuracy, all_preds, all_labels
