#coding = utf-8

import codecs
import math

f_main_role = codecs.open('../genMainRole/mainRole.txt', 'r', 'utf-8')
relation2MainRole = {}
for line in f_main_role:
    line = line.strip()
    multiRelation = line.split('\t')[0]
    roleIndex = int(line.split('\t')[1])
    relation2MainRole[multiRelation] = roleIndex
f_main_role.close()

f_hit_test = codecs.open('./hitTest.txt', 'r', 'utf-8')
# testRelationEntityList = []
# testRelationList = []
testRelationMainEntityDic = {}
for line in f_hit_test:
    line = line.strip()
    multiRelation = line.split('\t')[1]
    entityList = line.split('\t')[2:]
    testRelationMainEntityDic[multiRelation + '\t' + entityList[relation2MainRole[multiRelation] - 1]] = 0
    # testRelationList.append(multiRelation)
    # testRelationEntityList.append(entityList)
f_hit_test.close()
print(len(testRelationMainEntityDic))

f_relation_main_entity_other = codecs.open('./splitResult/multiRelationMainEntityOther.txt', 'w', 'utf-8')
ind = 0
for multiRelationMainEntity in testRelationMainEntityDic:
    multiRelation = multiRelationMainEntity.split('\t')[0]
    if ind % 40 == 0:
        f = codecs.open('./splitResult/multiRelationMainEntity' + str(ind/40) + '.txt', 'w', 'utf-8')
    if multiRelation == 'tv.regular_tv_appearance':
        ind += 1
        f.write(multiRelationMainEntity + '\n')
        if ind % 40 == 0:
            f.close()
    else:
        f_relation_main_entity_other.write(multiRelationMainEntity + '\n')
f.close()
f_relation_main_entity_other.close()