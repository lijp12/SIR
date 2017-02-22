#coding = utf-8

import codecs
import os

f_triplet_sum = codecs.open('./candidateTriplet.txt', 'w', 'utf-8')
for file in os.listdir('./NNTripletFinal0.5'):
    print(file)
    f = codecs.open('./NNTripletFinal0.5/' + file, 'r', 'utf-8')
    for line in f:
        f_triplet_sum.write(line)
    f.close()
f_triplet_sum.close()