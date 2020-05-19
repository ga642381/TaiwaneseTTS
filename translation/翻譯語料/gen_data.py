#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import random
tmp_dir = './tmp'
template = '{}_{}'
data_types = ['icorpus', 'TGB']

out_train = '../data/training.txt'
out_test = '../data/testing.txt'
out_val = '../data/validation.txt'

# ===================================== #
華 = []
閩 = []
for d in data_types:
    file = tmp_dir + "/" + template.format(d, '華')
    with open(file, 'r') as f:
        華 +=  f.readlines()
    
    file = tmp_dir + "/" + template.format(d, '閩')
    with open(file, 'r') as f:
        閩 +=  f.readlines()

out_華 = './華'
out_閩 = './閩'
with open(out_華, "w") as f:
    print(out_華)
    f.writelines(華)

with open(out_閩, "w") as f:
    print(out_閩)
    f.writelines(閩)
    
# =============== Split ================ #
華閩 = []
for index in range(len(華)):
    l = 華[index] + ' \t' + 閩[index]
    l = l.replace('\n', '')
    l = l + " \n"
    華閩.append(l)

SEED = 40666888
random.seed(SEED)
random.shuffle(華閩)

train_len = 100000
test_len = 10000
val_len = 2748

train_華閩 = 華閩[:train_len]
test_華閩 = 華閩[train_len:train_len + test_len]
val_華閩 = 華閩[train_len + test_len :]

with open(out_train, "w") as f:
    print(out_train)
    f.writelines(train_華閩)

with open(out_test, "w") as f:
    print(out_test)
    f.writelines(test_華閩)
    
with open(out_val, "w") as f:
    print(out_val)
    f.writelines(val_華閩)

























