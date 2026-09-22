import torch 
import torch.nn as nn
import torch.optim as optim
class neuralnet(nn.Module):
 def __init__(self):
  super().__init__()
  self.layers=nn.Sequential(nn.Linear(837,512),nn.ReLU(),nn.Linear(512,126),nn.ReLU(),nn.Linear(126,1))
 def __call__(self,x):
  return self.forward(x)
 def forward(self,x):
  return self.layers(x)


"""model=neuralnet()
loss_function = nn.MSELoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

loss=loss_function(prediction,target)
optimizer.zero_grad()
loss.backward()
optimizer.step()"""
