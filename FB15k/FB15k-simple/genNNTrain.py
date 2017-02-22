#codding = utf-8

import codecs
import random

pairSum = {}
trainPair = []
testPair = []
f_train = codecs.open('./train.txt', 'r', 'utf-8')
for line in f_train:
    line = line.strip()
    head = line.split('\t')[1]
    tail = line.split('\t')[2]
    pairSum[head + '\t' + tail] = 0
    trainPair.append([head,tail])
f_train.close()
f_test = codecs.open('./test.txt', 'r', 'utf-8')
for line in f_test:
    line = line.strip()
    head = line.split('\t')[1]
    tail = line.split('\t')[2]
    pairSum[head + '\t' + tail] = 0
    testPair.append([head,tail])
f_test.close()
f_valid = codecs.open('./valid.txt', 'r', 'utf-8')
for line in f_valid:
    line = line.strip()
    head = line.split('\t')[1]
    tail = line.split('\t')[2]
    pairSum[head + '\t' + tail] = 0
f_valid.close()

f_entity = codecs.open('./entity.txt', 'r', 'utf-8')
entityList = []
entity2Index = {}
ind = 0
for line in f_entity:
    entity = line.strip()
    entityList.append(entity)
    entity2Index[entity] = ind
    ind += 1
f_entity.close()

f_pos_train = codecs.open('./result/train_data_1.txt', 'w', 'utf-8')
f_neg_train = codecs.open('./result/train_data_0.txt', 'w', 'utf-8')
for entityPair in trainPair:
    string = str(entity2Index[entityPair[0]]) + ' '+ str(entity2Index[entityPair[1]]) + ' ' + '1' + '\n'
    f_pos_train.write(string)
    negativePair = [entityPair[0],entityPair[1]]
    negativePair[random.randint(0,1)] = entityList[random.randint(0,len(entityList) - 1)]
    while negativePair[0] + '\t' + negativePair[1] in pairSum:
        negativePair = [entityPair[0], entityPair[1]]
        negativePair[random.randint(0, 1)] = entityList[random.randint(0, len(entityList) - 1)]
    string = str(entity2Index[negativePair[0]]) + ' ' + str(entity2Index[negativePair[1]]) + ' ' + '0' + '\n'
    f_neg_train.write(string)
f_pos_train.close()
f_neg_train.close()

f_negatice_test = codecs.open('./result/test_data_0.txt', 'w', 'utf-8')
f_positive_test = codecs.open('./result/test_data_1.txt', 'w', 'utf-8')
for entityPair in testPair:
    string = str(entity2Index[entityPair[0]]) + ' ' + str(entity2Index[entityPair[1]]) + '\t' + '1' + '\n'
    f_positive_test.write(string)

    negativePair = [entityPair[0], entityPair[1]]
    negativePair[random.randint(0, 1)] = entityList[random.randint(0, len(entityList) - 1)]
    while negativePair[0] + '\t' + negativePair[1] in pairSum:
        negativePair = [entityPair[0], entityPair[1]]
        negativePair[random.randint(0, 1)] = entityList[random.randint(0, len(entityList) - 1)]
    string = str(entity2Index[negativePair[0]]) + ' ' + str(entity2Index[negativePair[1]]) + '\t' + '0' + '\n'
    f_negatice_test.write(string)
f_negatice_test.close()
f_positive_test.close()