import torch
import json
from torch.utils.data import Dataset,DataLoader
from NN import neuralnet
import torch.nn as nn
import torch.optim as optim

class chessdataset(Dataset):
 def __init__(self,file):
  self.data=[]
  with open(file,'r') as f:
   for line in f:
    example=json.loads(line)
    board=example['board']
    evaluation=example['evaluation']/10000.0
   self.data.append((board,evaluation))
 def __len__(self):
   return len(self.data)
 def __getitem__(self, index):
  board,evaluation=self.data[index]
  x=torch.tensor(board,dtype=torch.float32)
  y=torch.tensor([evaluation],dtype=torch.float32) 
  return x,y

model=neuralnet()
optimizer = optim.Adam(model.parameters(), lr=0.001)
loss_function = nn.MSELoss()
dataset=chessdataset('training_data.txt')
loader=DataLoader(dataset,batch_size=64,shuffle=True)
epochs=10

for epoch in range(epochs):
  total_loss=0
  total_mae=0
  for x,y_target in loader:
     
   y_pred =model(x)
   
   loss=loss_function(y_pred,y_target)
   mae = torch.abs(y_target - y_pred).mean()

   optimizer.zero_grad()
   loss.backward()
   optimizer.step()
   total_loss += loss.item()
   total_mae += mae.item()

  average_loss = total_loss / len(loader)
  average_mae = total_mae / len(loader)
  print(   f"Epoch {epoch + 1}/{epochs} "
        f"Loss: {average_loss:.4f} "
        f"MAE: {average_mae:.4f} "
        f"Avg engine error: {average_mae * 100:.1f}" )
torch.save(model.state_dict(),'chess_model.pth')

   