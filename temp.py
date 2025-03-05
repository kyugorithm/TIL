import torch
import torchvision.transforms as transforms
from PIL import Image, ImageDraw, ImageFont
import cv2
import numpy as np
import argparse
import os
import time
import csv
from datetime import datetime
from tqdm import tqdm
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

def preprocess_image(image, img_size=640):
    """
    Preprocess an image for inference.
    
    Args:
        image: PIL Image or numpy array
        img_size: Size to resize the image to
    
    Returns:
        tensor: Preprocessed image tensor
    """
    # Convert numpy array to PIL Image if necessary
    if isinstance(image, np.ndarray):
        image = Image.fromarray(image)
    
    # Define transformations
    transform = transforms.Compose([
        transforms.Resize((img_size, img_size)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])
    
    # Preprocess image
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

def sliding_window_inference(frame, model, window_size=640, stride=640, class_names=None, device='cuda', threshold=0.5):
    """
    Perform sliding window inference on a frame.
    
    Args:
        frame: Input frame as numpy array (H, W, C)
        model: Trained model
        window_size: Size of sliding window
        stride: Stride of sliding window
        class_names: List of class names
        device: Device to run inference on
        threshold: Confidence threshold for detection
        
    Returns:
        detections: List of dictionaries containing detections
    """
    height, width = frame.shape[:2]
    detections = []
    
    # Calculate number of windows in each dimension
    num_windows_h = max(1, (height - window_size + stride) // stride)
    num_windows_w = max(1, (width - window_size + stride) // stride)
    
    # If the image dimensions aren't perfectly divisible by the stride,
    # we need to handle the rightmost and bottommost windows differently
    if width % stride != 0:
        num_windows_w += 1
    if height % stride != 0:
        num_windows_h += 1
    
    # Process each window
    for i in range(num_windows_h):
        for j in range(num_windows_w):
            # Calculate window coordinates
            x = min(j * stride, width - window_size)
            y = min(i * stride, height - window_size)
            
            # Extract window
            window = frame[y:y+window_size, x:x+window_size]
            
            # If window is smaller than expected (at the edges), pad it
            if window.shape[0] != window_size or window.shape[1] != window_size:
                padded_window = np.zeros((window_size, window_size, 3), dtype=np.uint8)
                padded_window[:window.shape[0], :window.shape[1]] = window
                window = padded_window
            
            # Preprocess window
            window_tensor = preprocess_image(window, window_size)
            
            # Predict
            result = predict(model, window_tensor, class_names, device)
            
            # Add coordinates to result
            result['x'] = x
            result['y'] = y
            result['width'] = window_size
            result['height'] = window_size
            
            # Only keep detections for error class (assumed to be class_idx 1) and above threshold
            if result['class_idx'] == 1 and result['confidence'] >= threshold:
                result['window'] = window.copy()  # Store the window for saving
                detections.append(result)
    
    return detections

def process_video(video_path, model, output_dir, window_size=640, stride=640, 
                  class_names=None, device='cuda', threshold=0.5, save_frames=True):
    """
    Process a video file with sliding window inference.
    
    Args:
        video_path: Path to the video file
        model: Trained model
        output_dir: Directory to save results
        window_size: Size of sliding window
        stride: Stride of sliding window
        class_names: List of class names
        device: Device to run inference on
        threshold: Confidence threshold for detection
        save_frames: Whether to save frames with detections
        
    Returns:
        all_detections: List of all detections across the video
    """
    # Create output directories
    os.makedirs(output_dir, exist_ok=True)
    if save_frames:
        frames_dir = os.path.join(output_dir, 'error_frames')
        os.makedirs(frames_dir, exist_ok=True)
    
    # Open video
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise ValueError(f"Could not open video file: {video_path}")
    
    # Get video properties
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    
    print(f"Video properties:")
    print(f"  - Dimensions: {width}x{height}")
    print(f"  - FPS: {fps}")
    print(f"  - Total frames: {total_frames}")
    print(f"  - Duration: {total_frames/fps:.2f} seconds")
    print(f"  - Window size: {window_size}x{window_size}")
    print(f"  - Stride: {stride}")
    
    # Prepare CSV file
    csv_path = os.path.join(output_dir, 'detections.csv')
    csv_file = open(csv_path, 'w', newline='')
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(['frame_number', 'timestamp', 'x', 'y', 'class_name', 'confidence'])
    
    # Process frames
    all_detections = []
    frame_number = 0
    
    try:
        # Use tqdm for progress bar
        with tqdm(total=total_frames, desc="Processing video") as pbar:
            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break
                
                # Calculate timestamp
                timestamp = frame_number / fps
                
                # Convert BGR to RGB (OpenCV uses BGR, but our model expects RGB)
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                
                # Perform sliding window inference
                detections = sliding_window_inference(
                    frame_rgb, model, window_size, stride, class_names, device, threshold
                )
                
                # Process detections
                for detection in detections:
                    # Add frame info
                    detection['frame_number'] = frame_number
                    detection['timestamp'] = timestamp
                    all_detections.append(detection)
                    
                    # Write to CSV
                    csv_writer.writerow([
                        frame_number, 
                        f"{timestamp:.3f}", 
                        detection['x'], 
                        detection['y'], 
                        detection['class_name'], 
                        f"{detection['confidence']:.4f}"
                    ])
                    
                    # Save frame with detection
                    if save_frames:
                        # Convert window back to BGR for saving
                        window = detection['window']
                        
                        # Draw confidence on image
                        window_pil = Image.fromarray(window)
                        draw = ImageDraw.Draw(window_pil)
                        
                        # Try to use a font, fall back to default if not available
                        try:
                            font = ImageFont.truetype("arial.ttf", 20)
                        except IOError:
                            font = ImageFont.load_default()
                            
                        # Draw text with background for better visibility
                        text = f"{detection['class_name']}: {detection['confidence']:.4f}"
                        text_width, text_height = draw.textsize(text, font=font)
                        draw.rectangle(
                            [(0, 0), (text_width + 10, text_height + 10)],
                            fill=(255, 0, 0, 128)
                        )
                        draw.text((5, 5), text, font=font, fill=(255, 255, 255))
                        
                        # Save image
                        output_filename = f"frame_{frame_number}_x{detection['x']}_y{detection['y']}.png"
                        output_path = os.path.join(frames_dir, output_filename)
                        window_pil.save(output_path)
                
                # Update progress bar
                frame_number += 1
                pbar.update(1)
                
    finally:
        # Clean up
        cap.release()
        csv_file.close()
    
    # Print summary
    print(f"\nVideo processing completed:")
    print(f"  - Processed {frame_number} frames")
    print(f"  - Found {len(all_detections)} errors")
    print(f"  - Results saved to {output_dir}")
    if len(all_detections) > 0:
        print(f"  - Error frames saved to {frames_dir}")
    print(f"  - CSV report saved to {csv_path}")
    
    return all_detections

def main():
    """Main function to run video inference"""
    parser = argparse.ArgumentParser(description='Run inference on a video file with sliding windows')
    
    # Model arguments
    parser.add_argument('--model_path', type=str, required=True,
                        help='Path to the trained model file')
    parser.add_argument('--model_type', type=str, default='efficientnet_b0',
                        choices=['efficientnet_b0', 'mobilenet_v3_small'],
                        help='Model architecture type (default: efficientnet_b0)')
    
    # Input arguments
    parser.add_argument('--video', type=str, required=True,
                        help='Path to input video file')
    parser.add_argument('--window_size', type=int, default=640,
                        help='Size of sliding window (default: 640)')
    parser.add_argument('--stride', type=int, default=640,
                        help='Stride of sliding window (default: 640)')
    
    # Output arguments
    parser.add_argument('--output_dir', type=str, default=None,
                        help='Directory to save results (default: based on video filename)')
    parser.add_argument('--threshold', type=float, default=0.5,
                        help='Confidence threshold for detection (default: 0.5)')
    
    # Other arguments
    parser.add_argument('--class_names', type=str, nargs='+', default=['Normal', 'Error'],
                        help='Names of the classes (default: Normal, Error)')
    parser.add_argument('--device', type=str, default='cuda' if torch.cuda.is_available() else 'cpu',
                        help='Device to run inference on (default: cuda if available, else cpu)')
    
    args = parser.parse_args()
    
    # Set default output directory based on video filename if not specified
    if args.output_dir is None:
        video_name = os.path.splitext(os.path.basename(args.video))[0]
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        args.output_dir = f"results_{video_name}_{timestamp}"
    
    # Load model
    print(f"Loading model from {args.model_path}")
    model = load_model(args.model_path, args.model_type, args.device)
    
    # Process video
    process_video(
        video_path=args.video,
        model=model,
        output_dir=args.output_dir,
        window_size=args.window_size,
        stride=args.stride,
        class_names=args.class_names,
        device=args.device,
        threshold=args.threshold
    )

if __name__ == "__main__":
    main()
