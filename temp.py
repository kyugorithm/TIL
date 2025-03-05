import os
import torch
import torch.nn as nn
import torch.optim as optim
import argparse
import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import confusion_matrix, classification_report
import seaborn as sns

# Import the modules we created
from model_definition import BinaryClassifier
from dataset_implementation import create_dataloaders
from training_pipeline import train_model, evaluate_model
from model_optimization import optimize_model_for_inference, benchmark_inference_speed

def parse_args():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description='Train a binary image classifier')
    
    # Data arguments
    parser.add_argument('--data_dir', type=str, required=True,
                        help='Directory containing class subdirectories')
    parser.add_argument('--img_size', type=int, default=640,
                        help='Size to resize images to (default: 640)')
    
    # Model arguments
    parser.add_argument('--model', type=str, default='efficientnet_b0',
                        choices=['efficientnet_b0', 'mobilenet_v3_small'],
                        help='Model architecture to use (default: efficientnet_b0)')
    parser.add_argument('--pretrained', action='store_true',
                        help='Use pretrained weights (default: True)')
    
    # Training arguments
    parser.add_argument('--batch_size', type=int, default=32,
                        help='Batch size for training (default: 32)')
    parser.add_argument('--epochs', type=int, default=20,
                        help='Maximum number of epochs to train for (default: 20)')
    parser.add_argument('--lr', type=float, default=0.001,
                        help='Learning rate (default: 0.001)')
    parser.add_argument('--patience', type=int, default=5,
                        help='Early stopping patience (default: 5)')
    parser.add_argument('--device', type=str, default='cuda' if torch.cuda.is_available() else 'cpu',
                        help='Device to train on (default: cuda if available, else cpu)')
    
    # Output arguments
    parser.add_argument('--output_dir', type=str, default='output',
                        help='Directory to save model and results (default: output)')
    
    args = parser.parse_args()
    return args

def plot_training_history(history, save_path=None):
    """Plot training history"""
    plt.figure(figsize=(12, 4))
    
    # Plot training & validation accuracy
    plt.subplot(1, 2, 1)
    plt.plot(history['train_acc'], label='Train')
    plt.plot(history['val_acc'], label='Validation')
    plt.title('Model Accuracy')
    plt.xlabel('Epoch')
    plt.ylabel('Accuracy')
    plt.legend()
    
    # Plot training & validation loss
    plt.subplot(1, 2, 2)
    plt.plot(history['train_loss'], label='Train')
    plt.plot(history['val_loss'], label='Validation')
    plt.title('Model Loss')
    plt.xlabel('Epoch')
    plt.ylabel('Loss')
    plt.legend()
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path)
        print(f"Training history plot saved to {save_path}")
    
    plt.show()

def plot_confusion_matrix(true_labels, predictions, class_names, save_path=None):
    """Plot confusion matrix"""
    cm = confusion_matrix(true_labels, predictions)
    
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
                xticklabels=class_names, yticklabels=class_names)
    plt.title('Confusion Matrix')
    plt.ylabel('True Label')
    plt.xlabel('Predicted Label')
    
    if save_path:
        plt.savefig(save_path)
        print(f"Confusion matrix plot saved to {save_path}")
    
    plt.show()

def main():
    """Main function to run the training pipeline"""
    # Parse arguments
    args = parse_args()
    
    # Create output directory if it doesn't exist
    os.makedirs(args.output_dir, exist_ok=True)
    
    # Set random seeds for reproducibility
    torch.manual_seed(42)
    torch.cuda.manual_seed(42)
    np.random.seed(42)
    
    # Create dataloaders
    print(f"Creating dataloaders from {args.data_dir}")
    train_loader, val_loader, class_names = create_dataloaders(
        args.data_dir,
        batch_size=args.batch_size,
        img_size=args.img_size
    )
    
    # Create model
    print(f"Creating {args.model} model")
    model = BinaryClassifier(
        model_name=args.model,
        pretrained=args.pretrained
    )
    
    # Define loss function and optimizer
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=args.lr)
    
    # Learning rate scheduler
    scheduler = optim.lr_scheduler.ReduceLROnPlateau(
        optimizer, mode='max', factor=0.1, patience=3, verbose=True
    )
    
    # Train model
    model_save_path = os.path.join(args.output_dir, 'best_model.pt')
    model, history = train_model(
        model,
        train_loader,
        val_loader,
        criterion,
        optimizer,
        scheduler=scheduler,
        device=args.device,
        num_epochs=args.epochs,
        early_stopping_patience=args.patience,
        save_path=model_save_path
    )
    
    # Plot training history
    history_plot_path = os.path.join(args.output_dir, 'training_history.png')
    plot_training_history(history, save_path=history_plot_path)
    
    # Evaluate model on validation set
    print("Evaluating model on validation set")
    accuracy, predictions, true_labels = evaluate_model(
        model,
        val_loader,
        device=args.device
    )
    
    # Plot confusion matrix
    cm_plot_path = os.path.join(args.output_dir, 'confusion_matrix.png')
    plot_confusion_matrix(true_labels, predictions, class_names, save_path=cm_plot_path)
    
    # Print classification report
    print("\nClassification Report:")
    print(classification_report(true_labels, predictions, target_names=class_names))
    
    # Optimize model for inference
    print("Optimizing model for inference")
    
    # Get a sample input
    for inputs, _ in val_loader:
        sample_input = inputs[:1].to(args.device)  # Take first batch and first sample
        break
    
    # Optimize and save model
    optimized_model_path = os.path.join(args.output_dir, 'optimized_model.pt')
    optimized_model = optimize_model_for_inference(
        model,
        sample_input,
        save_path=optimized_model_path
    )
    
    # Benchmark inference speed
    print("Benchmarking inference speed")
    benchmark_inference_speed(
        model,
        input_size=(1, 3, args.img_size, args.img_size),
        device=args.device
    )
    
    print(f"Training and evaluation completed. Results saved to {args.output_dir}")

if __name__ == "__main__":
    main()
