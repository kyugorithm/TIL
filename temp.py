import torch
import torch.nn as nn
import torch.nn.functional as F

# 1. 기본적인 Feed-forward Neural Network
class BasicFFN(nn.Module):
    def __init__(self, input_dim=768, hidden_dims=[512, 256], num_classes=2, dropout_rate=0.1):
        super().__init__()
        layers = []
        prev_dim = input_dim
        
        for hidden_dim in hidden_dims:
            layers.extend([
                nn.Linear(prev_dim, hidden_dim),
                nn.ReLU(),
                nn.BatchNorm1d(hidden_dim),
                nn.Dropout(dropout_rate)
            ])
            prev_dim = hidden_dim
            
        self.layers = nn.Sequential(*layers)
        self.classifier = nn.Linear(prev_dim, num_classes)
        
    def forward(self, x):
        # x shape: (batch_size, 768)
        x = self.layers(x)
        return self.classifier(x)

# 2. Transformer Encoder 기반 분류기
class TransformerClassifier(nn.Module):
    def __init__(self, input_dim=768, num_classes=2, nhead=8, num_layers=2):
        super().__init__()
        
        # 임베딩을 시퀀스처럼 다루기 위해 재구성
        self.input_reshape = nn.Linear(input_dim, input_dim)
        
        encoder_layer = nn.TransformerEncoderLayer(
            d_model=input_dim,
            nhead=nhead,
            dim_feedforward=input_dim*4,
            dropout=0.1,
            batch_first=True
        )
        self.transformer = nn.TransformerEncoder(encoder_layer, num_layers=num_layers)
        self.classifier = nn.Linear(input_dim, num_classes)
        
    def forward(self, x):
        # x shape: (batch_size, 768)
        x = x.unsqueeze(1)  # (batch_size, 1, 768)
        x = self.transformer(x)
        x = x.squeeze(1)    # (batch_size, 768)
        return self.classifier(x)

# 3. Multi-Scale Feature Fusion 분류기
class MultiScaleClassifier(nn.Module):
    def __init__(self, input_dim=768, num_classes=2):
        super().__init__()
        
        # 다양한 스케일의 특징 추출
        self.scale1 = nn.Sequential(
            nn.Linear(input_dim, input_dim//2),
            nn.ReLU(),
            nn.BatchNorm1d(input_dim//2)
        )
        
        self.scale2 = nn.Sequential(
            nn.Linear(input_dim, input_dim//4),
            nn.ReLU(),
            nn.BatchNorm1d(input_dim//4)
        )
        
        # 어텐션 기반 특징 융합
        self.attention = nn.MultiheadAttention(
            embed_dim=input_dim//2,
            num_heads=4,
            batch_first=True
        )
        
        total_features = input_dim//2 + input_dim//4
        self.classifier = nn.Sequential(
            nn.Linear(total_features, num_classes)
        )
        
    def forward(self, x):
        # x shape: (batch_size, 768)
        s1 = self.scale1(x)  # (batch_size, 384)
        s2 = self.scale2(x)  # (batch_size, 192)
        
        # 특징 연결
        combined = torch.cat([s1, s2], dim=1)
        return self.classifier(combined)

# 4. Residual Dense Network
class ResidualDenseClassifier(nn.Module):
    def __init__(self, input_dim=768, growth_rate=128, num_layers=4, num_classes=2):
        super().__init__()
        
        self.layers = nn.ModuleList()
        current_dim = input_dim
        
        for _ in range(num_layers):
            self.layers.append(nn.Sequential(
                nn.Linear(current_dim, growth_rate),
                nn.ReLU(),
                nn.BatchNorm1d(growth_rate)
            ))
            current_dim += growth_rate
            
        self.classifier = nn.Linear(current_dim, num_classes)
        
    def forward(self, x):
        features = [x]
        
        for layer in self.layers:
            out = layer(torch.cat(features, dim=1))
            features.append(out)
            
        return self.classifier(torch.cat(features, dim=1))
