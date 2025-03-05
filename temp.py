import os
import torch
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms
from PIL import Image
import numpy as np
from sklearn.model_selection import train_test_split

class ImageClassificationDataset(Dataset):
    def __init__(self, image_paths, labels, transform=None):
        """
        Custom dataset for image classification.
        
        Args:
            image_paths (list): List of paths to images
            labels (list): List of labels corresponding to image_paths
            transform (callable, optional): Optional transform to be applied to images
        """
        self.image_paths = image_paths
        self.labels = labels
        self.transform = transform
    
    def __len__(self):
        return len(self.image_paths)
    
    def __getitem__(self, idx):
        # Load image
        img_path = self.image_paths[idx]
        image = Image.open(img_path).convert('RGB')
        
        # Apply transformations
        if self.transform:
            image = self.transform(image)
        
        # Get label
        label = self.labels[idx]
        
        return image, label

def create_dataloaders(data_dir, batch_size=32, img_size=640, test_size=0.2, random_state=42):
    """
    Create train and validation dataloaders from a directory structure.
    
    Args:
        data_dir (str): Root directory containing class subdirectories
        batch_size (int): Batch size for dataloaders
        img_size (int): Size to resize images to
        test_size (float): Proportion of data to use for validation
        random_state (int): Random seed for reproducibility
    
    Returns:
        tuple: (train_loader, val_loader, class_names)
    """
    # Get class names from directory structure
    class_names = [d for d in os.listdir(data_dir) if os.path.isdir(os.path.join(data_dir, d))]
    class_names.sort()  # Ensure consistent ordering
    
    # Create class to index mapping
    class_to_idx = {cls_name: i for i, cls_name in enumerate(class_names)}
    
    # Collect all image paths and labels
    image_paths = []
    labels = []
    
    for class_name in class_names:
        class_dir = os.path.join(data_dir, class_name)
        class_idx = class_to_idx[class_name]
        
        # Get all image files in the class directory
        for img_name in os.listdir(class_dir):
            if img_name.lower().endswith(('.png', '.jpg', '.jpeg')):
                img_path = os.path.join(class_dir, img_name)
                image_paths.append(img_path)
                labels.append(class_idx)
    
    # Split into train and validation sets
    train_paths, val_paths, train_labels, val_labels = train_test_split(
        image_paths, labels, test_size=test_size, random_state=random_state, stratify=labels
    )
    
    # Define transforms
    # Training transforms with data augmentation
    train_transform = transforms.Compose([
        transforms.Resize((img_size, img_size)),
        transforms.RandomHorizontalFlip(),
        transforms.RandomRotation(10),
        transforms.ColorJitter(brightness=0.1, contrast=0.1),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])
    
    # Validation transforms (no augmentation)
    val_transform = transforms.Compose([
        transforms.Resize((img_size, img_size)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])
    
    # Create datasets
    train_dataset = ImageClassificationDataset(train_paths, train_labels, transform=train_transform)
    val_dataset = ImageClassificationDataset(val_paths, val_labels, transform=val_transform)
    
    # Create dataloaders
    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True, num_workers=4, pin_memory=True)
    val_loader = DataLoader(val_dataset, batch_size=batch_size, shuffle=False, num_workers=4, pin_memory=True)
    
    print(f"Dataset created with {len(train_dataset)} training samples and {len(val_dataset)} validation samples")
    print(f"Class distribution - Training: {np.bincount(train_labels)}, Validation: {np.bincount(val_labels)}")
    
    return train_loader, val_loader, class_names
