#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Nov  5 16:20:44 2018

@author: qiusisun
"""

import sys
#sys.path.insert(0,'/Library/Frameworks/Python.framework/Versions/3.6/lib/python3.6/site-packages')
import os
import torch
import torch.nn as nn
from torch.autograd import Variable
import torchvision.datasets as dset
import torchvision.transforms as transforms
import torch.nn.functional as F
import torch.optim as optim
import random
import numpy as np
from sklearn.metrics import f1_score
## load mnist dataset

use_cuda = torch.cuda.is_available()

print ('==>>> total trainning batch number: {}'.format(500))
print ('==>>> total testing batch number: {}'.format(100))

## network
class MLPNet(nn.Module):
    def __init__(self):
        super(MLPNet, self).__init__()
        self.fc1 = nn.Linear(21, 10)
        self.fc2 = nn.Linear(10, 2)
    def forward(self, x):
        #x = x.view(-1, 28*28)
        x = self.fc1(x)
        x = F.relu(x)
        x = self.fc2(x)

        return x

    def name(self):
        return "MLP"

xy_x_svm = np.loadtxt('sen_training_19.txt')
xy_y_svm = np.loadtxt('training_class_19.txt')

#1023*21
x_data_svm = Variable(torch.from_numpy(xy_x_svm[:,0:]))
#1023*1
y_data_svm = Variable(torch.from_numpy(xy_y_svm[0:]))

random.seed(5)

## training
model = MLPNet()
#model = svm()
if use_cuda:
    model = model.cuda()

optimizer = optim.SGD(model.parameters(), lr=0.01, momentum=0.9)

criterion = nn.CrossEntropyLoss()
#criterion = nn.MSELoss()

for epoch in range(35):
    # trainning
    ave_loss = 0
    batch_idx = 0

    for batch in range(500):
        ranhi_svm = random.randint(500,1208)
        ranlow_svm = ranhi_svm - 500

        optimizer.zero_grad()
        x, target = x_data_svm[ranlow_svm:ranhi_svm], y_data_svm[ranlow_svm:ranhi_svm]
        out = model(x.float())
        loss = criterion(out, target.long())
        print(loss)
        exit()
        ave_loss = ave_loss * 0.9 + loss.data[0] * 0.1
        loss.backward()
        optimizer.step()
        if (batch_idx+1) % 100 == 0 or (batch_idx+1) == 500:
            print('==>>> epoch: {}, batch index: {}, train loss: {:.6f}'.format(
                epoch, batch_idx+1, ave_loss))
        batch_idx += 1

    # testing
    correct_cnt, ave_loss = 0, 0
    total_cnt = 0
    batch_idx = 0

    for batch in range(100):
        ranhi_svm = random.randint(100,1208)
        ranlow_svm = ranhi_svm - 100

        x, target = x_data_svm[ranlow_svm:ranhi_svm], y_data_svm[ranlow_svm:ranhi_svm]
        #load model
        out = model(x.float())
        loss = criterion(out, target.long())
        _, pred_label = torch.max(out.data, 1)
        target.data = target.data.long()
        #print((pred_label == target.data.long()).sum())

        #exit()
        total_cnt += x.data.size()[0]
        correct_cnt += (pred_label == target.data).sum()
        # smooth average
        ave_loss = ave_loss * 0.9 + loss.data[0] * 0.1

        if(batch_idx+1) % 100 == 0 or (batch_idx+1) == 100:
            print( '==>>> epoch: {}, batch index: {}, test loss: {:.6f}, acc: {:.3f}'.format(
                epoch, batch_idx+1, ave_loss, correct_cnt * 1.0 / total_cnt))


        batch_idx += 1

    #save output file
    if epoch == 49:
        x, target = x_data_svm[0:], y_data_svm[0:]
        out = model(x.float())
        loss = criterion(out, target.long())
        _, pred_label = torch.max(out.data, 1)
        target.data = target.data.long()

        total_cnt += x.data.size()[0]
        #tensor2numpy:numpy array
        final = pred_label.double()
        tensor2numpy = final.numpy()
        correct_cnt += (pred_label == target.data).sum()
        # smooth average
        ave_loss = ave_loss * 0.9 + loss.data[0] * 0.1

        print( '==>>> epoch: {}, test loss: {:.6f}, acc: {:.3f}'.format(
                epoch, ave_loss, correct_cnt * 1.0 / total_cnt))


#np.savetxt('classified_biclf.txt',tensor2numpy)
f1 = f1_score(target.data,pred_label,average='weighted')
print('final f1 score',f1)
torch.save(model.state_dict(), model.name())

