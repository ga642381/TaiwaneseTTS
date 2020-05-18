#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re
TGB_華 = "./TGB/TGB_華語"
TGB_閩 = "./TGB/TGB_閩南語"

SYMBOLS = ['~', "'", '+', '[',
           '\\', '@', '^', '{', 
            '-', '"', '*', '|', 
            '&', '<', '`', '}',
            '_', '=', ']',  '>', 
            '#', '$', '/', '...',''
            '』', '『 ']
            
with open(TGB_華, "r") as f:
    華 = f.readlines()

with open(TGB_閩, "r") as f:
    閩 = f.readlines()

def to_pingin(閩):
    閩_tmp = []
    for i, l in enumerate(閩):
        tokens = l.split()
        join_elms = []
        for t in tokens:
            if "｜" in t:
                token = t.split("｜") # len == 2
                left = token[0] # e5-人
                right = token[-1] # -lang5
                left_tmp = re.findall(r'[\u4e00-\u9fff]+',left) # find中文字
                right_tmp = right.split("-") #找取代的拼音
                while "" in right_tmp:
                    right_tmp.remove("")
                for i, chi in enumerate(left_tmp):
                    left = left.replace(chi, right_tmp[i])
                join_elms.append(left)
                
            else:
                join_elms.append(t)        
        l = " ".join(join_elms)
        l = l + "\n"
        閩_tmp.append(l)
    return 閩_tmp

閩_tmp = to_pingin(閩)

華_ = []
閩_ = []
to_remove_lines = []
to_remove_index = []
k = 0
##=============== 華 ===============##
for i, l in enumerate(華) :
    for s in SYMBOLS:
        if s in l:
           to_remove_lines.append(l) 
           to_remove_index.append(i)
           
    if "《 TGB 通訊 》" in l:
        to_remove_lines.append(l)
        to_remove_index.append(i)     
        
    if len(l) <= 2:
        to_remove_lines.append(l)
        to_remove_index.append(i)        
        
    l = l.replace("“","「")
    l = l.replace("”","」")
    
    if ("「 " in l) and ("」 " not in l):
        l = l.replace("「 ", "")
    
    if  ("」 " in l) and ("「 " not in l):
        l = l.replace("」 ", "")     
        
    if  ("」 " in l) and ("「 " in l):
        if l.index("」") < l.index("「"):
            l = l.replace("「 ", "")
            l = l.replace("」 ", "")
            
    if l[-2] == "," or l[-2] == "，":
        l = l[:-2] +  "。\n"
    
    華_.append(l)
    
##=============== 閩 ===============##
K_ = 0
for i, l in enumerate(閩_tmp) :
    l = l.replace("“","「")
    l = l.replace("”","」")    

    if ("「 " in l) and ("」 " not in l):
        l = l.replace("「 ", "")
    
    if  ("」 " in l) and ("「 " not in l):
        l = l.replace("」 ", "")     
        
    if  ("」 " in l) and ("「 " in l):
        if l.index("」") < l.index("「"):
            l = l.replace("「 ", "")
            l = l.replace("」 ", "")
            
    l = l.replace("，", ",")
    l = l.replace("。", ".")
    l = l.replace("？", "?")    
    l = l.replace("「", "\"")
    l = l.replace("」", "\"")
    l = l.replace("；", ";")
    l = l.replace("、", ",")
    l = l.replace("！", "!")
    if l[-2] == "," or l[-2] == "，":
        l = l[:-2] +  ".\n"
    閩_.append(l)
    
閩_ =  [j for i, j in enumerate(閩_) if i not in to_remove_index]
華_ =  [j for i, j in enumerate(華_) if i not in to_remove_index]

with open("./TGB_華", "w") as f:
    f.writelines(華_)

with open("./TGB_閩", "w") as f:
    f.writelines(閩_)
            
            
            
            
            
            