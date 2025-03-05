import torch
import torch.nn as nn
import torchvision.models as models

class BinaryClassifier(nn.Module):
    def __init__(self, model_name='efficientnet_b0', pretrained=True):
        """
        Initialize a binary classifier based on a pretrained model.
        
        Args:
            model_name (str): Name of the base model to use ('efficientnet_b0' or 'mobilenet_v3_small')
            pretrained (bool): Whether to use pretrained weights
        """
        super(BinaryClassifier, self).__init__()
        
        # Select base model
        if model_name == 'efficientnet_b0':
            # Load pretrained EfficientNet B0
            weights = models.EfficientNet_B0_Weights.IMAGENET1K_V1 if pretrained else None
            self.base_model = models.efficientnet_b0(weights=weights)
            num_features = self.base_model.classifier[1].in_features
            # Replace classifier with a binary classifier
            self.base_model.classifier = nn.Sequential(
                nn.Dropout(p=0.2, inplace=True),
                nn.Linear(num_features, 2)
            )
        
        elif model_name == 'mobilenet_v3_small':
            # Load pretrained MobileNetV3 Small
            weights = models.MobileNet_V3_Small_Weights.IMAGENET1K_V1 if pretrained else None
            self.base_model = models.mobilenet_v3_small(weights=weights)
            num_features = self.base_model.classifier[3].in_features
            # Replace classifier with a binary classifier
            self.base_model.classifier[3] = nn.Linear(num_features, 2)
        
        else:
            raise ValueError(f"Unsupported model: {model_name}")
    
    def forward(self, x):
        """Forward pass through the network"""
        return self.base_model(x)
    
    def save_model(self, path):
        """Save the model weights to a file"""
        torch.save(self.state_dict(), path)
    
    @classmethod
    def load_model(cls, path, model_name='efficientnet_b0'):
        """
        Load a model from saved weights
        
        Args:
            path (str): Path to the saved model weights
            model_name (str): Name of the base model used
            
        Returns:
            BinaryClassifier: Loaded model
        """
        model = cls(model_name=model_name, pretrained=False)
        model.load_state_dict(torch.load(path))
        return model
