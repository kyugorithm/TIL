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

def main():
    """Main function to run inference on images"""
    parser = argparse.ArgumentParser(description='Run inference with a trained model')
    
    # Model arguments
    parser.add_argument('--model_path', type=str, required=True,
                        help='Path to the trained model file')
    parser.add_argument('--model_type', type=str, default='efficientnet_b0',
                        choices=['efficientnet_b0', 'mobilenet_v3_small'],
                        help='Model architecture type (default: efficientnet_b0)')
    
    # Input arguments
    parser.add_argument('--input', type=str, required=True,
                        help='Path to input image or directory of images')
    parser.add_argument('--img_size', type=int, default=640,
                        help='Image size for model input (default: 640)')
    
    # Output arguments
    parser.add_argument('--output_dir', type=str, default=None,
                        help='Directory to save prediction results (optional)')
    
    # Other arguments
    parser.add_argument('--class_names', type=str, nargs='+', default=['Normal', 'Error'],
                        help='Names of the classes (default: Normal, Error)')
    parser.add_argument('--device', type=str, default='cuda' if torch.cuda.is_available() else 'cpu',
                        help='Device to run inference on (default: cuda if available, else cpu)')
    
    args = parser.parse_args()
    
    # Load model
    print(f"Loading model from {args.model_path}")
    model = load_model(args.model_path, args.model_type, args.device)
    
    # Prepare input paths
    if os.path.isdir(args.input):
        # If input is a directory, get all image files
        image_paths = []
        for ext in ['*.jpg', '*.jpeg', '*.png']:
            image_paths.extend(glob.glob(os.path.join(args.input, ext)))
        print(f"Found {len(image_paths)} images in directory {args.input}")
    else:
        # If input is a single file
        image_paths = [args.input]
        print(f"Using single image: {args.input}")
    
    # Create output directory if specified
    if args.output_dir:
        os.makedirs(args.output_dir, exist_ok=True)
    
    # Process each image
    results = []
    
    for image_path in image_paths:
        print(f"Processing {image_path}")
        
        # Preprocess image
        image_tensor = preprocess_image(image_path, args.img_size)
        
        # Make prediction
        result = predict(model, image_tensor, args.class_names, args.device)
        
        # Add file path to result
        result['image_path'] = image_path
        results.append(result)
        
        # Print result
        print(f"Prediction: {result['class_name']}, Confidence: {result['confidence']:.4f}, "
              f"Time: {result['inference_time_ms']:.2f} ms")
        
    # Calculate average inference time
    avg_time = sum(r['inference_time_ms'] for r in results) / len(results)
    print(f"\nAverage inference time: {avg_time:.2f} ms ({1000/avg_time:.2f} FPS)")
    
    # Save results if output directory is specified
    if args.output_dir:
        import csv
        import json
        
        # Save as CSV
        csv_path = os.path.join(args.output_dir, 'predictions.csv')
        with open(csv_path, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=['image_path', 'class_idx', 'class_name', 'confidence', 'inference_time_ms'])
            writer.writeheader()
            writer.writerows(results)
        
        # Save as JSON
        json_path = os.path.join(args.output_dir, 'predictions.json')
        with open(json_path, 'w') as f:
            json.dump(results, f, indent=4)
        
        print(f"Results saved to {csv_path} and {json_path}")

if __name__ == "__main__":
    main()
