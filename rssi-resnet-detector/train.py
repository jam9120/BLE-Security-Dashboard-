import torch
import torch.nn as nn
import torch.optim as optim
from models.resnet_rssi import build_resnet
from utils.dataset_loader import get_data_loaders

# === Config ===
EPOCHS = 10
BATCH_SIZE = 32
NUM_CLASSES = 2  # Change based on your use case
TRAIN_DIR = 'data/train'
VAL_DIR = 'data/val'
TEST_DIR = 'data/test'
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# === Load Data ===
train_loader, val_loader, test_loader = get_data_loaders(TRAIN_DIR, VAL_DIR, TEST_DIR, BATCH_SIZE)

# === Build Model ===
model = build_resnet(NUM_CLASSES).to(DEVICE)
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=1e-4)

# === Training Loop ===
for epoch in range(EPOCHS):
    model.train()
    running_loss = 0.0
    for inputs, labels in train_loader:
        inputs, labels = inputs.to(DEVICE), labels.to(DEVICE)

        optimizer.zero_grad()
        outputs = model(inputs)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()
        running_loss += loss.item()

    print(f"[Epoch {epoch+1}] Loss: {running_loss/len(train_loader):.4f}")
