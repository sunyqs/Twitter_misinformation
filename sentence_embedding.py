#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Nov  5 16:20:10 2018

@author: qiusisun
"""

#sentence embedding for reason.txt
from random import randint
import numpy as np
import torch
from models import InferSent
import pickle
from sklearn import preprocessing
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.autograd import Variable


#load text
class net(nn.Module):
    def __init__(self):
        super(net, self).__init__()
        self.fc1 = nn.Linear(4096, 300)
    def forward(self, x):
        #x = x.view(-1, 28*28)
        x = self.fc1(x)
        return x

sentences = []
with open('final_text.txt') as f:
    for line in f:
        sentences.append(line.strip())

V = 1
MODEL_PATH = 'encoder/infersent%s.pkl' % V
params_model = {'bsize': 64, 'word_emb_dim': 300, 'enc_lstm_dim': 2048,
                'pool_type': 'max', 'dpout_model': 0.0, 'version': V}

model = InferSent(params_model)
model.load_state_dict(torch.load(MODEL_PATH))
W2V_PATH = 'final_text_vectors.txt'
model.set_w2v_path(W2V_PATH)
model.build_vocab(sentences, tokenize=True)#build_vocab_k_words(K=100000)

embeddings = model.encode(sentences, tokenize=True)#(sentences, bsize=168, tokenize=False, verbose=True)
print('nb sentences encoded : {0}'.format(len(embeddings)))

sen_vec = preprocessing.normalize(embeddings)
sen_vec = Variable(torch.from_numpy(sen_vec))
#sen_vec = nn.Linear(4096,300)
model = net()
n = (1,300)
nparray = np.zeros(n)
for i in sen_vec:
    out = model(i)
    out = out.data.numpy()
    #print(out)
    nparray = np.append(nparray,[out],axis = 0)
nparray = np.delete(nparray,0,axis=0)
    #out = model(i)
#print(len(trans_model[0]))
#print(len(trans_model))
#exit()


'''
for i in sentences:
    embedding = model.encode([i])
    #print(len(embedding[0]))
    normalized = preprocessing.normalize(embedding)
    sen_vec.append(normalized)
print(sen_vec)
exit()
m = (1,4096)
nparray = np.zeros(m) #initialization
for i in sen_vec:
    nparray = np.append(nparray,[i],axis=0)
nparray = np.delete(nparray,0,axis=0)
#print(type(nparray[0]))
#for i in nparray:
#    print(i)
'''
np.savetxt('final_sen_text.txt',nparray)
'''
thefile = open('sen_text.txt', 'w')
for item in sen_vec:
  thefile.write("%s\n" % item)
'''
#print(embedding)
#print(vector)