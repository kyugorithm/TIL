import torch
import torchvision.transforms as transforms
from PIL import Image
import argparse
import os
import time
import glob
from model_definition import BinaryClassifier

def load_model(model_path, model_type='efficientnet_b0', device='cuda'):
    """
    Load a trained model for inference.
    
    Args:
        model_path: Path to the saved model
        model_type: Type of model architecture
        device: Device to run inference on
    
    Returns:
        model: Loaded model
    """
    # Check if model is a JIT model
    if model_path.endswith('.pt'):
        try:
            # Try loading as JIT model first
            model = torch.jit.load(model_path, map_location=device)
            print("Loaded JIT optimized model")
        except:
            # If that fails, load as regular model
            model = BinaryClassifier(model_name=model_type, pretrained=False)
            model.load_state_dict(torch.load(model_path, map_location=device))
            print(f"Loaded {model_type} model from state dict")
    
    model.to(device)
    model.eval()
    return model

def preprocess_image(image_path, img_size=640):
    """
    Preprocess an image for inference.
    
    Args:
        image_path: Path to the image
        img_size: Size to resize the image to
    
    Returns:
        tensor: Preprocessed image tensor
    """
    # Define transformations
    transform = transforms.Compose([
        transforms.Resize((img_size, img_size)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])
    
    # Load and preprocess image
    image = Image.open(image_path).convert('RGB')
    tensor = transform(image).unsqueeze(0)  # Add batch dimension
    
    return tensor

def predict(model, image_tensor, class_names=None, device='cuda'):
    """
    Make a prediction for an image.
    
    Args:
        model: Trained model
        image_tensor: Preprocessed image tensor
        class_names: List of class names
        device: Device to run inference on
    
    Returns:
        prediction: Class index
        confidence: Prediction confidence
    """
    # Move tensor to device
    image_tensor = image_tensor.to(device)
    
    # Perform inference
    with torch.no_grad():
        start_time = time.time()
        outputs = model(image_tensor)
        inference_time = (time.time() - start_time) * 1000  # Convert to milliseconds
        
        # Get predictions
        probabilities = torch.nn.functional.softmax(outputs, dim=1)
        confidence, prediction = torch.max(probabilities, 1)
    
    # Convert to Python types
    prediction = prediction.item()
    confidence = confidence.item()
    
    # Map to class name if provided
    if class_names is not None and prediction < len(class_names):
        prediction_name = class_names[prediction]
    else:
        prediction_name = f"Class {prediction}"
    
    return {
        'class_idx': prediction,
        'class_name': prediction_name,
        'confidence': confidence,
        'inference_time_ms': inference_time
    }
