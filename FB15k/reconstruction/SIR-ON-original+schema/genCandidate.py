#coding = utf-8

import codecs

f_main_role = codecs.open('../../genMainRole/mainRole.txt', 'r', 'utf-8')
relation2role = {}
for line in f_main_role:
    line = line.strip()
    relation = line.split('\t')[0]
    mainRole = int(line.split('\t')[1]) - 1
    relation2role[relation] = mainRole
f_main_role.close()
print(len(relation2role))
print("load mainRole over")

f_entity = codecs.open('../../FB15k-simple/entity.txt', 'r', 'utf-8')
entityList = []
for line in f_entity:
    line = line.strip()
    entityList.append(line)
f_entity.close()
print(len(entityList))
print("load entity over")

f_relation_type = codecs.open('../../FB15k-simple/Type/relation-schema-simple.txt', 'r', 'utf-8')
relation2type = {}
for line in f_relation_type:
    line = line.strip()
    relation = line.split('\t')[0]
    headType = line.split('\t')[1]
    tailType = line.split('\t')[2]
    relation2type[relation] = [headType, tailType]
f_relation_type.close()
print(len(relation2type))
print("load relationSchema over")

f_entity_type = codecs.open('../../FB15k-simple/Type/entityTypeSimple.txt', 'r', 'utf-8')
relation2entity = {}
for line in f_entity_type:
    line = line.strip()
    entity = line.split('\t')[1]
    typeSet = set(line.split('\t')[2:])
    for relation, typeList in relation2type.items():
        headType = set()
        headType.add(typeList[0])
        tailType = set()
        tailType.add(typeList[1])
        if relation not in relation2entity:
            relation2entity[relation] = [[],[]]
        if len(headType & typeSet) == 1:
            relation2entity[relation][0].append(entity)
        if len(tailType & typeSet) == 1:
            relation2entity[relation][1].append(entity)
f_entity_type.close()
print("load entityType over")

f_test = codecs.open('../../FB15k-simple/test.txt', 'r', 'utf-8')
f_candidate = codecs.open('./candidateTriplet.txt', 'w', 'utf-8')
for line in f_test:
    line = line.strip()
    relation = line.split('\t')[0]
    head = line.split('\t')[1]
    tail = line.split('\t')[2]
    mainRole = relation2role[relation]
    if mainRole == 0:
        for entity  in relation2entity[relation][1]:
            f_candidate.write(relation + '\t' + head + '\t' + entity + '\n')
    else:
        for entity in relation2entity[relation][0]:
            f_candidate.write(relation + '\t' + entity + '\t' + tail + '\n')
f_candidate.close()
f_test.close()
print("generate candidate over")