import torch
from torch.utils.data import Dataset, DataLoader
from torch.optim import AdamW
from sklearn.model_selection import train_test_split
import numpy as np
from tqdm import tqdm

# 데이터셋 클래스
class EmbeddingDataset(Dataset):
    def __init__(self, embeddings, labels):
        self.embeddings = torch.FloatTensor(embeddings)
        self.labels = torch.LongTensor(labels)
        
    def __len__(self):
        return len(self.labels)
        
    def __getitem__(self, idx):
        return self.embeddings[idx], self.labels[idx]

def train_model(model, train_embeddings, train_labels, val_size=0.2, 
                batch_size=32, epochs=10, lr=2e-5):
    # 데이터 분할
    X_train, X_val, y_train, y_val = train_test_split(
        train_embeddings, train_labels, test_size=val_size
    )
    
    # 데이터로더 생성
    train_dataset = EmbeddingDataset(X_train, y_train)
    val_dataset = EmbeddingDataset(X_val, y_val)
    
    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
    val_loader = DataLoader(val_dataset, batch_size=batch_size)
    
    # 옵티마이저와 손실함수
    optimizer = AdamW(model.parameters(), lr=lr)
    criterion = torch.nn.CrossEntropyLoss()
    
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.to(device)
    
    best_val_acc = 0
    
    for epoch in range(epochs):
        # 학습
        model.train()
        train_loss = 0
        for batch in tqdm(train_loader, desc=f'Epoch {epoch+1}/{epochs}'):
            embeddings, labels = [b.to(device) for b in batch]
            
            optimizer.zero_grad()
            outputs = model(embeddings)
            loss = criterion(outputs, labels)
            
            loss.backward()
            optimizer.step()
            
            train_loss += loss.item()
            
        # 검증
        model.eval()
        val_correct = 0
        val_total = 0
        val_loss = 0
        
        with torch.no_grad():
            for batch in val_loader:
                embeddings, labels = [b.to(device) for b in batch]
                outputs = model(embeddings)
                loss = criterion(outputs, labels)
                
                val_loss += loss.item()
                _, predicted = torch.max(outputs.data, 1)
                val_total += labels.size(0)
                val_correct += (predicted == labels).sum().item()
        
        val_acc = 100 * val_correct / val_total
        
        print(f'Epoch {epoch+1}:')
        print(f'Training Loss: {train_loss/len(train_loader):.4f}')
        print(f'Validation Loss: {val_loss/len(val_loader):.4f}')
        print(f'Validation Accuracy: {val_acc:.2f}%')
        
        # 모델 저장
        if val_acc > best_val_acc:
            best_val_acc = val_acc
            torch.save(model.state_dict(), 'best_model.pth')
            
    return model

# 사용 예시:
if __name__ == "__main__":
    # 데이터 준비 (예시)
    embeddings = np.random.randn(100000, 768)  # BERT 임베딩
    labels = np.random.randint(0, 2, 100000)   # 이진 분류
    
    # 모델 선택
    model = TransformerClassifier()  # 또는 다른 모델
    
    # 학습
    trained_model = train_model(
        model=model,
        train_embeddings=embeddings,
        train_labels=labels,
        batch_size=32,
        epochs=10
    )
