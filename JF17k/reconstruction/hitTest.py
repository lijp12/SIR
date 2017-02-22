#coding = utf-8

import codecs
import time

def is_include(entityList, binaryList, tripletDic):
    schema = len(entityList)
    if schema == 2:
        triplet = binaryList[0] + '\t' + entityList[0] + '\t' + entityList[1]
        if triplet in tripletDic:
            return 1
        else:
            return 0
    else:
        ind1 = 0
        start_time = time.time()
        while ind1 < schema - 1:
            ind2 = ind1 + 1
            while ind2 < schema:
                relation = binaryList[ind1] + '/' + binaryList[ind2]
                triplet = relation + '\t' + entityList[ind1] + '\t' + entityList[ind2]
                if triplet not in tripletDic:
                    return 0
                ind2 += 1
            ind1 += 1
        print(time.time() - start_time)
        return 1

f_triple_sum = codecs.open('../NNFilt/NNTripletSum.txt', 'r', 'utf-8')
tripletDic = {}
for line in f_triple_sum:
    line = line.strip()
    tripletDic[line] = 0
f_triple_sum.close()
print("load NNTripletSum over")

f_mul_binary = codecs.open('../informationRelated/multi2binary.txt', 'r', 'utf-8')
mul2binary = {}
for line in f_mul_binary:
    line = line.strip()
    multiRelation = line.split('\t')[0]
    schemaNum = int(line.split('\t')[1])
    if schemaNum == 2:
        mul2binary[multiRelation] = [multiRelation]
    else:
        relationList = line.split('\t')[2:]
        mul2binary[multiRelation] = relationList
f_mul_binary.close()
print("load multi2binary over")

f_train = codecs.open('../JF17k-simple/version1/train.txt', 'r', 'utf-8')
hit_train = 0
count_train = 0
for line in f_train:
    count_train += 1
    print(count_train)
    line = line.strip()
    relation = line.split('\t')[0]
    entityList = line.split('\t')[1:]
    binaryList = mul2binary[relation]
    ok = is_include(entityList, binaryList, tripletDic)
    print(ok)
    if ok == 1:
        hit_train += 1
f_train.close()


f_test = codecs.open('../JF17k-simple/version1/test.txt', 'r', 'utf-8')
f_hit_test = codecs.open('./hitTest.txt', 'w', 'utf-8')
hit_test = 0
count_test = 0
for line in f_test:
    count_test += 1
    print(count_test)
    line = line.strip()
    relation = line.split('\t')[1]
    entityList = line.split('\t')[2:]
    binaryList = mul2binary[relation]
    if is_include(entityList, binaryList, tripletDic) == 1:
        hit_test += 1
        f_hit_test.write(line + '\n')
f_hit_test.close()
f_test.close()

print(1.0 * hit_train / count_train)
print(1.0 * hit_test / count_test)
