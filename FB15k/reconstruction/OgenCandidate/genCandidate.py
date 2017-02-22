#coding = utf-8

import codecs

f_entity = codecs.open('../../FB15k-simple/entity.txt', 'r', 'utf-8')
entityList = []
for line in f_entity:
    entity = line.strip()
    entityList.append(entity)
f_entity.close()

f_main_role = codecs.open('../../genMainRole/mainRole.txt', 'r', 'utf-8')
relation2role = {}
for line in f_main_role:
    line = line.strip()
    relation = line.split('\t')[0]
    roleIndex = int(line.split('\t')[1]) - 1
    relation2role[relation] = roleIndex
f_main_role.close()

f_test = codecs.open('../genTest.txt', 'r', 'utf-8')
f_complex = codecs.open('./candidateTriplet.txt', 'w', 'utf-8')
for line in f_test:
    line = line.strip()
    relation = line.split('\t')[0]
    mainEntity = line.split('\t')[1]
    mainRole = relation2role[relation]
    if mainRole == 0:
        for entity in entityList:
            f_complex.write(relation + '\t' + mainEntity + '\t' + entity + '\n')
    else:
        for entity in entityList:
            f_complex.write(relation + '\t' + entity + '\t' + mainEntity + '\n')
f_complex.close()
f_test.close()
