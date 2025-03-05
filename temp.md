# Binary Image Classification Model

A PyTorch-based solution for binary image classification, specifically designed to distinguish between normal images and images with error patterns (small horizontal rectangular boxes).

## Project Overview

This project implements a complete pipeline for training, optimizing, and deploying a lightweight and efficient binary image classifier using pretrained models from PyTorch's torchvision library. The solution includes:

- Custom dataset loading and preprocessing
- Model definition and training pipeline
- Model optimization for inference efficiency
- Evaluation and visualization tools
- Inference script for deployment

## Requirements

- Python 3.7+
- PyTorch 1.10+ with CUDA support (recommended)
- torchvision
- Pillow
- numpy
- scikit-learn
- matplotlib
- seaborn
- tqdm

Install dependencies:

```bash
pip install torch torchvision tqdm numpy scikit-learn matplotlib seaborn Pillow
```

## Project Structure

```
binary-classifier/
├── model_definition.py        # Model architecture
├── dataset_implementation.py  # Dataset and dataloader implementation
├── training_pipeline.py       # Training and evaluation functions
├── model_optimization.py      # Model quantization and optimization
├── main.py                    # Main training script
├── inference.py               # Inference script
├── output/                    # Directory for training outputs
│   ├── best_model.pt          # Best model from training
│   ├── optimized_model.pt     # Optimized model for inference
│   ├── training_history.png   # Training metrics plot
│   └── confusion_matrix.png   # Confusion matrix visualization
└── README.md                  # This documentation
```

## Dataset Preparation

Organize your dataset in the following directory structure:

```
data/
├── Normal/           # Class 1: Normal images
│   ├── img001.jpg
│   ├── img002.jpg
│   └── ...
└── Error/            # Class 2: Error images with small horizontal rectangular boxes
    ├── img001.jpg
    ├── img002.jpg
    └── ...
```

## Usage Instructions

### Training

To train the model:

```bash
python main.py --data_dir path/to/data --model efficientnet_b0 --pretrained --batch_size 32 --epochs 20 --output_dir output
```

Key arguments:
- `--data_dir`: Directory containing class subdirectories
- `--model`: Model architecture (`efficientnet_b0` or `mobilenet_v3_small`)
- `--pretrained`: Use pretrained weights
- `--batch_size`: Batch size for training
- `--epochs`: Maximum number of epochs to train
- `--lr`: Learning rate
- `--patience`: Early stopping patience
- `--device`: Device to train on (cuda/cpu)
- `--output_dir`: Directory to save output files

### Inference

To run inference on new images:

```bash
python inference.py --model_path output/optimized_model.pt --input path/to/image_or_directory --output_dir predictions
```

Key arguments:
- `--model_path`: Path to the trained model file
- `--model_type`: Model architecture type
- `--input`: Path to input image or directory of images
- `--img_size`: Image size for model input
- `--class_names`: Names of the classes (default: "Normal", "Error")
- `--output_dir`: Directory to save prediction results
- `--device`: Device to run inference on

## Model Selection

This project supports two pretrained model architectures:

1. **EfficientNet B0** (default)
   - Balanced performance and efficiency
   - Good accuracy with moderate parameter count
   - Suitable for most deployment scenarios

2. **MobileNetV3 Small**
   - Extremely lightweight and fast
   - Lower parameter count for mobile deployments
   - Sacrifices some accuracy for speed

To use MobileNetV3 Small:

```bash
python main.py --data_dir path/to/data --model mobilenet_v3_small --pretrained
```

## Model Optimization

The `model_optimization.py` script provides functions to:

1. Trace and serialize the model with TorchScript
2. Quantize the model to reduce size and improve inference speed
3. Benchmark inference performance

These optimizations are automatically applied when training with `main.py` and the optimized model is saved to `output/optimized_model.pt`.

## Performance Evaluation

The training script produces:
- Training/validation accuracy and loss curves
- Confusion matrix visualization
- Classification report with precision, recall, and F1-score
- Inference speed benchmarks

## Customization

To adapt this solution for other binary classification tasks:

1. Modify `create_dataloaders()` in `dataset_implementation.py` if your data structure is different
2. Adjust preprocessing transforms based on your specific image characteristics
3. Tune hyperparameters like learning rate, batch size, and image size to match your dataset
4. For deployment to resource-constrained environments, consider using `mobilenet_v3_small`

## Troubleshooting

- **Out of memory errors**: Reduce batch size or image size
- **Slow training**: Ensure CUDA is available and properly configured
- **Poor performance**: Try different learning rates, increase training epochs, or add more data augmentation
- **Overfitting**: Increase regularization, reduce model complexity, or add more training data
