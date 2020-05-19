#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re
import json

# ===== 華 =====#
words = {}
with open('華', 'r') as f:
    for line in f:
        line = re.split('[ \n\t\r ]', line)
        line = list(filter(None, line))
        for word in line:
            words[word] = words.get(word, 0) + 1

words = sorted(words.items(), key=lambda d: d[1], reverse=True)
words = [word for word, count in words if count >= 3]
words = ['<PAD>', '<BOS>', '<EOS>', '<UNK>'] + words

word2int_cn, int2word_cn = {}, {}
for Index, word in enumerate(words):
    word2int_cn[word] = Index
    int2word_cn[Index] = word
    
with open("../data/word2int_華.json", "w") as f:
    json.dump(word2int_cn, f, ensure_ascii=False)

with open("../data/int2word_華.json", "w") as f:
    json.dump(int2word_cn, f, ensure_ascii=False)
    
# ===== 閩 =====#

words = {}
with open('閩', 'r') as f:
    for line in f:
        line = re.split('[ \n\t\r ]', line)
        line = list(filter(None, line))
        for word in line:
            words[word] = words.get(word, 0) + 1

words = sorted(words.items(), key=lambda d: d[1], reverse=True)
words = [word for word, count in words if count >= 3]
words = ['<PAD>', '<BOS>', '<EOS>', '<UNK>'] + words

word2int_cn, int2word_cn = {}, {}
for Index, word in enumerate(words):
    word2int_cn[word] = Index
    int2word_cn[Index] = word
    
with open("../data/word2int_閩.json", "w") as f:
    json.dump(word2int_cn, f, ensure_ascii=False)

with open("../data/int2word_閩.json", "w") as f:
    json.dump(int2word_cn, f, ensure_ascii=False)
    