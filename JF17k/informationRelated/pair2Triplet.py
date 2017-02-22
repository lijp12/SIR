#coding = utf-8

import codecs
import os

pair2relation = {}
for file in os.listdir('../SchemaFiltPair/tripletFinal'):
    f = codecs.open('../SchemaFiltPair/tripletFinal/' + file, 'r', 'utf-8')
    for line in f:
        line = line.strip()
        relation = line.split('\t')[0]
        head = line.split('\t')[1]
        tail = line.split('\t')[2]
        if head + '\t' + tail in pair2relation:
            pair2relation[head + '\t' + tail].append(relation)
        else:
            pair2relation[head + '\t' + tail] = [relation]
    f.close()

f_pair = codecs.open('../NNFilt/NNFiltPair.txt', 'r', 'utf-8')
f_triplet = codecs.open('./tripletResult.txt', 'w', 'utf-8')
for line in f_pair:
    line = line.strip()
    head = line.split('\t')[0]
    tail = line.split('\t')[1]
    string = head + '\t' + tail
    if string in pair2relation:
        for relation in pair2relation[string]:
            f_triplet.write(relation + '\t' + string)
f_pair.close()
f_triplet.close()

