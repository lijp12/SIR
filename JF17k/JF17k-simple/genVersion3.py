#coding = utf-8

import codecs

f_relation = codecs.open('../../JF17k/version3/version3/relation.txt', 'r', 'utf-8')
relationList = []
for line in f_relation:
    line = line.strip()
    relation = line.split('\t')[0]
    relationList.append(relation)
f_relation.close()

delRelationList = []
schemaRelationList = []
f_relation_schema = codecs.open('../../JF17k/totalRelationType.txt', 'r', 'utf-8')
for line in f_relation_schema:
    line = line.strip()
    relation = line.split('\t')[0]
    schemaRelationList.append(relation)
    headType = line.split('\t')[1]
    tailType = line.split('\t')[2]
    if (headType == 'common.topic') | (tailType == 'common.topic'):
        delRelationList.append(relation)
f_relation_schema.close()

for relation in (set(relationList) - set(schemaRelationList)):
    delRelationList.append(relation)

#####生成新的relation列表
f_new_relation = codecs.open('./version3/relation.txt', 'w', 'utf-8')
for relation in sorted(set(relationList) - set(delRelationList)):
    f_new_relation.write(relation + '\t' + '2')
    f_new_relation.write('\n')
f_new_relation.close()

for relation in delRelationList:
    print(relation)

entityDic = {}
####生成新的train
f_train = codecs.open('../../JF17k/version3/version3/train.txt', 'r', 'utf-8')
f_new_train = codecs.open('./version3/train.txt', 'w', 'utf-8')
for line in f_train:
    relation = line.split('\t')[0]
    if relation in delRelationList:
        continue
    else:
        entityDic[line.split('\t')[1].strip()] = 0
        entityDic[line.split('\t')[2].strip()] = 0
        f_new_train.write(line)
f_new_train.close()
f_train.close()

###生成新的entity列表
f_new_entity = codecs.open('./version3/entity.txt', 'w', 'utf-8')
for entity in entityDic.keys():
    entity = entity.strip()
    f_new_entity.write(entity + '\n')
f_new_entity.close()


####生成新的test
f_test = codecs.open('../../JF17k/version3/version3/test.txt', 'r', 'utf-8')
f_new_test = codecs.open('./version3/test.txt', 'w', 'utf-8')
for line in f_test:
    relation = line.split('\t')[1]
    head = line.split('\t')[2].strip()
    tail = line.split('\t')[3].strip()
    if relation in delRelationList:
        continue
    else:
        if (head in entityDic) & (tail in entityDic):
            f_new_test.write(line)
f_new_test.close()
f_test.close()



