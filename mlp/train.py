import os
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader

os.environ["CUDA_VISIBLE_DEVICES"] = "1"  
# Detect GPU
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Using device: {device}")

# 🔹 Step 1: Define Dataset Loader
class WordMappingDataset(Dataset):
    def __init__(self, data_path, vocab=None):
        self.word_pairs = []
        self.vocab = vocab or {}

        # Read dataset
        with open(data_path, "r") as f:
            for line in f:
                src, tgt = line.strip().split("\t")
                self.word_pairs.append((src, tgt))

        # Build vocab only for training data
        if vocab is None:
            unique_words = set([w for pair in self.word_pairs for w in pair])
            self.vocab = {word: idx for idx, word in enumerate(unique_words)}
        
        self.index_to_word = {idx: word for word, idx in self.vocab.items()}
        self.data = [(self.vocab[src], self.vocab[tgt]) for src, tgt in self.word_pairs]

    def __len__(self):
        return len(self.data)

    def __getitem__(self, index):
        return torch.tensor(self.data[index][0], device=device), torch.tensor(self.data[index][1], device=device)

# 🔹 Step 2: Define MLP Model
class MLPWordMapper(nn.Module):
    def __init__(self, vocab_size, embedding_dim=50, hidden_dim=100):
        super(MLPWordMapper, self).__init__()
        self.embedding = nn.Embedding(vocab_size, embedding_dim)
        self.fc1 = nn.Linear(embedding_dim, hidden_dim)
        self.relu = nn.ReLU()
        self.fc2 = nn.Linear(hidden_dim, vocab_size)  # Predicts word index

    def forward(self, x):
        x = self.embedding(x)
        x = self.fc1(x)
        x = self.relu(x)
        x = self.fc2(x)
        return x

# 🔹 Step 3: Training Function
def train_model(train_path, dev_path, test_path, epochs=20, batch_size=4, lr=0.01):
    # Load train dataset and create vocab
    train_dataset = WordMappingDataset(train_path)
    vocab = train_dataset.vocab  # Use the same vocab for all sets
    vocab_size = len(vocab)

    # Load dev and test datasets using the same vocab
    dev_dataset = WordMappingDataset(dev_path, vocab)
    test_dataset = WordMappingDataset(test_path, vocab)

    # Dataloaders
    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
    dev_loader = DataLoader(dev_dataset, batch_size=batch_size, shuffle=False)
    test_loader = DataLoader(test_dataset, batch_size=batch_size, shuffle=False)

    # Model, loss, optimizer (Move to GPU)
    model = MLPWordMapper(vocab_size).to(device)
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=lr)

    best_dev_loss = float("inf")
    for epoch in range(epochs):
        model.train()
        total_train_loss = 0

        for src, tgt in train_loader:
            optimizer.zero_grad()
            output = model(src)
            loss = criterion(output, tgt)
            loss.backward()
            optimizer.step()
            total_train_loss += loss.item()

        # Evaluate on dev set
        model.eval()
        total_dev_loss = 0
        with torch.no_grad():
            for src, tgt in dev_loader:
                output = model(src)
                loss = criterion(output, tgt)
                total_dev_loss += loss.item()

        print(f"Epoch [{epoch+1}/{epochs}], Train Loss: {total_train_loss:.4f}, Dev Loss: {total_dev_loss:.4f}")

        # Save best model
        if total_dev_loss < best_dev_loss:
            best_dev_loss = total_dev_loss
            torch.save(model.state_dict(), "mlp_word_mapper_best.pth")
            print("✅ New best model saved!")

    print("Training complete!")

    # 🔹 Step 4: Evaluate on Test Set
    model.load_state_dict(torch.load("mlp_word_mapper_best.pth"))
    model.eval()

    correct = 0
    total = 0
    with torch.no_grad():
        for src, tgt in test_loader:
            output = model(src)
            predicted = torch.argmax(output, dim=1)
            correct += (predicted == tgt).sum().item()
            total += tgt.size(0)

    print(f"Test Accuracy: {100 * correct / total:.2f}%")

    # Save final model & vocab
    torch.save(model.state_dict(), "mlp_word_mapper_final.pth")
    torch.save(vocab, "vocab.pth")

# Run training
train_model("data/train.tsv", "data/dev.tsv", "data/test.tsv")
