import pickle
import random
import math
import base64
import sys
import json
import collections
import heapq 


def go(node, first, code ):
    if (node[1] == 0):
        if (first == ''):
            code[node[0]] = '0'
        else:
            code[node[0]] = first
    else:
        go(node[0][0], first+'0', code)
        go(node[0][1], first+'1', code)

def h_enc(text):
    dic = collections.Counter(text)
    tree = []
    count = 0
    code = {}
    for i in sorted(dic):
        tree.append((dic[i], count, (i,0)))
        count += 1
    heapq.heapify(tree)
    while len(tree) > 1:
        count_a, num_a, a = heapq.heappop(tree)
        count_b, num_b, b = heapq.heappop(tree)
        heapq.heappush(tree, (count_a + count_b, count, ((a, b),1)))
        count += 1
    (count_root, num_root, root) = tree[0]
    go(root, '', code)
    return code

def h_dec(code, text):
    decode = {}
    for i in code:
        decode[code[i]] = i
    res = ''
    while(text != ''):    
        for i in decode:
            if text.startswith(i):
                res += decode[i]
                text = text[len(i):]
    return res

def dec(name):
    with open(sys.argv[1], "rb") as file:
        len_en = pickle.load(file) 
        code = pickle.load(file)
        text = pickle.load(file) 
    code = eval(code)
    en = ''
    text= int.from_bytes(text, 'big')
    while (text > 0):
        if (text%2):
            en += '1'
        else:
            en += '0'
        text //= 2 
    en = en[::-1]
    if (len(en) != len_en):
        en = '0'*(len_en - len(en)) + en
    res = h_dec(code, en)
    return res 

def enc(name, ex):
    with open(sys.argv[1], "rb") as file:
        text = pickle.load(file)
    code = h_enc(text)
    res = ""
    #for ch in sorted(code):
    #    print("{}: {}".format(ch, code[ch]))
    for i in text:
        res += code[i]
    len_en = len(res)
    res = int(res, 2)
    res = res.to_bytes((res.bit_length() + 7) // 8, 'big')
    with open(ex, "wb") as file:
        pickle.dump(len_en, file)
        code = str(code)
        pickle.dump(code, file)
        pickle.dump(res, file)

if (sys.argv[2] == "encode"):
    if (sys.argv[1][-4:]!='.bin'):
        print("Неверный формат файла")
    else:
        name = sys.argv[1][:-4] + '.zmh'
        enc(sys.argv[1], name)       
        
if (sys.argv[2] == "decode"):
    if (sys.argv[1][-4:]!='.zmh'):
        print("Неверный формат файла")
    else:
        name = sys.argv[1][:-4] + '.bin'
        res = dec(sys.argv[1])
        with open(name, "wb") as file:
            pickle.dump(res, file)
    