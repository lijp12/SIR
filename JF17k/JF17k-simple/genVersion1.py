#coding = utf-8

import codecs

f_now_bi_relation = codecs.open('./version3/relation.txt', 'r', 'utf-8')
relationDic = {}
for line in f_now_bi_relation:
    relation = line.split('\t')[0]
    relationDic[relation] = 0
f_now_bi_relation.close()

mulRelationDic = {}
f_relation = codecs.open('../../JF17k/version1/version1/relation.txt', 'r', 'utf-8')
f_new_relation = codecs.open('./version1/relation.txt', 'w', 'utf-8')
for line in f_relation:
    line = line.strip()
    relation = line.split(' ')[0]
    schemaNum = int(line.split(' ')[1])
    if schemaNum > 2:
        mulRelationDic[relation] = 0
        f_new_relation.write(relation + '\t' + str(schemaNum) + '\n')
    else:
        if relation in relationDic:
            mulRelationDic[relation] = 0
            f_new_relation.write(relation + '\t' + str(schemaNum) + '\n')
f_relation.close()
f_new_relation.close()

entityDic = {}
####生成新的train
f_train = codecs.open('../../JF17k/version1/version1/train.txt', 'r', 'utf-8')
f_new_train = codecs.open('./version1/train.txt', 'w', 'utf-8')
for line in f_train:
    relation = line.split('\t')[0]
    if relation in mulRelationDic:
        for entity in line.split('\t')[1:]:
            entityDic[entity.strip()] = 0
        f_new_train.write(line)
f_new_train.close()
f_train.close()


####生成新的test
f_test = codecs.open('../../JF17k/version1/version1/test.txt', 'r', 'utf-8')
f_new_test = codecs.open('./version1/test.txt', 'w', 'utf-8')
for line in f_test:
    line = line.strip()
    relation = line.split('\t')[1]
    if relation in mulRelationDic:
        flag = 1
        for entity in line.split('\t')[2:]:
            if entity not in entityDic:
                flag = 0
                break
        if flag == 1:
            f_new_test.write(line + '\n')
f_new_test.close()
f_test.close()
