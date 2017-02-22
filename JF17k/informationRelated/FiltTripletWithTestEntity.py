#coding = utf-8

import codecs

f_test_entity = codecs.open('../JF17k-simple/version1/test.txt', 'r', 'utf-8')
entityDic = {}
for line in f_test_entity:
    line = line.strip()
    entityList = line.split('\t')[2:]
    for entity in entityList:
        entityDic[entity] = 0
f_test_entity.close()

f_triplet = codecs.open('../NNFilt/NNTripletSum.txt', 'r', 'utf-8')
f_new_triplet = codecs.open('./FiltNNTripletSum.txt', 'w', 'utf-8')
for line in f_triplet:
    line = line.strip()
    head = line.split('\t')[1]
    tail = line.split('\t')[2]
    if (head in entityDic) & (tail in entityDic):
        f_new_triplet.write(line + '\n')
f_new_triplet.close()
f_triplet.close()