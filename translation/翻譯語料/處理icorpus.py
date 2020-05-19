#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re
icorpus_華 = './icorpus/華' 
icorpus_閩 = './icorpus/閩'

with open(icorpus_華, "r") as f:
    華 = f.readlines()

with open(icorpus_閩, "r") as f:
    閩 = f.readlines()
    
for i, l in enumerate(華):
    l = l.replace("-", "")
    if re.match(r'[\u4e00-\u9fff]', l[-2]):
        l = l.replace("\n", " 。\n")
        
    華[i] = l
    
for i, l in enumerate(閩):
    l = l.replace("「", "\"")
    l = l.replace("」", "\"")
    l = l.replace("『", "\'")
    l = l.replace("』", "\'")

    
    l = l.replace("，", ",")
    l = l.replace("。", ".")
    l = l.replace("？", "?")    
    l = l.replace("「", "\"")
    l = l.replace("」", "\"")
    l = l.replace("；", ";")
    l = l.replace("、", ",")
    l = l.replace("！", "!")
    l = l.replace("：", ":")
    
    if re.match(r'[0-9a-zA-z]', l[-2]):
        l= l.replace("\n", " .\n")
    閩[i] = l

out_華 = './tmp/icorpus_華' 
out_閩 = './tmp/icorpus_閩'
with open(out_華, "w") as f:
    print(out_華)
    f.writelines(華)

with open(out_閩, "w") as f:
    print(out_閩)
    f.writelines(閩)
            