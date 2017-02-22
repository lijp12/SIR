#coding = utf-8

import codecs
import os

f_NN_triplet = codecs.open('./NNTripletSum.txt', 'w', 'utf-8')
pairDic = {}
for file in os.listdir('./NNTripletFinal'):
    f = codecs.open('./NNTripletFinal/' + file, 'r', 'utf-8')
    for line in f:
		line = line.strip()
		head = line.split('\t')[1]
		tail = line.split('\t')[2]
		pairDic[head + '\t' + tail] = 0
		f_NN_triplet.write(line + '\n')
    f.close()
f_NN_triplet.close()

f_NN_pair = codecs.open('./NNFiltPairSum.txt', 'w', 'utf-8')
for key in pairDic.keys():
	f_NN_pair.write(key + '\n')
f_NN_pair.close()