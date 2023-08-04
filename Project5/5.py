from SM3 import sm3_hash
from math import ceil, log2
import random

def CreateTree():
    data = []
    for i in range(100):
        data.append(random.randint(1, 100))
    tree=[[sm3_hash(str(hex(i)[2:])) for i in data]]
    for i in range(ceil(log2(len(tree[0])) + 1)-1):
        h = [sm3_hash("1"+tree[i][j*2]+ tree[i][j*2+1]) for j in range(int(len(tree[i])/2))]
        if len(tree[i]) % 2 != 0:
            h.append(tree[i][-1])
        tree.append(h)
    return tree

def exist_prove(tree,node):
    alist = []
    if sm3_hash(node) in tree[0]:
        d = tree[0].index(sm3_hash(node))
    else:
        print("Illegal nodes")
    temp = d
    for i in range(ceil(log2(len(tree[0])) + 1)-1):
        if temp % 2 == 0:alist.append(['l',tree[i][temp + 1]])
        else:
            alist.append(['r',tree[i][temp - 1]])
        temp = int(temp / 2)
    h0 = sm3_hash(node)
    for i in alist:
        if i[0] == 'l':h0 = sm3_hash('1' + h0 + i[1])
        else:
            h0 = sm3_hash('1' + i[1] + h0)
    if h0 == tree[-1][0]:
        print(node,"exist in tree")
    else:
        print("Not exist")

tree=CreateTree()
exist_prove(tree,'1')











