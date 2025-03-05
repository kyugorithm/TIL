import torch
import torch.quantization
import time
import numpy as np

def optimize_model_for_inference(model, sample_input, save_path='optimized_model.pt'):
    """
    Optimize a trained model for inference using TorchScript and quantization.
    
    Args:
        model: Trained PyTorch model
        sample_input: A sample input tensor to trace the model
        save_path: Path to save the optimized model
    
    Returns:
        optimized_model: The optimized model
    """
    # Set model to evaluation mode
    model.eval()
    
    # Step 1: Convert to TorchScript via tracing
    print("Converting model to TorchScript...")
    traced_model = torch.jit.trace(model, sample_input)
    
    # Step 2: Quantize the model to reduce size and improve inference speed
    print("Quantizing model...")
    quantized_model = torch.quantization.quantize_dynamic(
        model,  # The original model
        {torch.nn.Linear},  # Specify which layers to quantize
        dtype=torch.qint8  # The target dtype for quantized weights
    )
    
    # Save the quantized model
    print(f"Saving optimized model to {save_path}")
    torch.jit.save(traced_model, save_path)
    
    return quantized_model

def benchmark_inference_speed(model, input_size=(1, 3, 640, 640), device='cuda', num_runs=100):
    """
    Benchmark inference speed of a model.
    
    Args:
        model: PyTorch model to benchmark
        input_size: Size of input tensor
        device: Device to run inference on
        num_runs: Number of inference runs to average over
    
    Returns:
        avg_time: Average inference time in milliseconds
    """
    model.eval()
    model.to(device)
    
    # Create random input tensor
    dummy_input = torch.randn(input_size, device=device)
    
    # Warm-up runs
    for _ in range(10):
        _ = model(dummy_input)
    
    # Synchronize before timing
    if device == 'cuda':
        torch.cuda.synchronize()
    
    # Measure inference time
    start_time = time.time()
    
    for _ in range(num_runs):
        _ = model(dummy_input)
        if device == 'cuda':
            torch.cuda.synchronize()
    
    end_time = time.time()
    
    # Calculate average inference time
    avg_time = (end_time - start_time) * 1000 / num_runs  # Convert to milliseconds
    
    print(f"Average inference time: {avg_time:.2f} ms ({1000/avg_time:.2f} FPS)")
    
    # Get model size
    model_size = get_model_size(model)
    print(f"Model size: {model_size:.2f} MB")
    
    return avg_time

def get_model_size(model):
    """
    Get the size of a PyTorch model in megabytes.
    
    Args:
        model: PyTorch model
    
    Returns:
        size_mb: Size of the model in megabytes
    """
    torch.save(model.state_dict(), "temp_model.pt")
    size_bytes = os.path.getsize("temp_model.pt")
    os.remove("temp_model.pt")
    
    size_mb = size_bytes / (1024 * 1024)
    return size_mb
