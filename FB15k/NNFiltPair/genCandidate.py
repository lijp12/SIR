#incoding = utf-8

import codecs

f_relation_role = codecs.open('../genMainRole/mainRole.txt', 'r', 'utf-8')
relation2role = {}
for line in f_relation_role:
    line = line.strip()
    relation = line.split('\t')[0]
    role = int(line.split('\t')[1]) - 1
    relation2role[relation] = role
f_relation_role.close()
print("load mainRole over")

f_test = codecs.open('../FB15k-simple/test.txt', 'r', 'utf-8')
relationMainEntityDic = {}
for line in f_test:
    line = line.strip()
    relation = line.split('\t')[0]
    mainEntity = line.split('\t')[1 + relation2role[relation]]
    relationMainEntityDic[relation + '\t' + mainEntity] = 0
f_test.close()
print("load test over")

f_NN_candidate = codecs.open('./candidateTriplet.txt', 'r', 'utf-8')
f_new_candidate  = codecs.open('./testCandidateTriplet.txt', 'w', 'utf-8')
count = 0
for line in f_NN_candidate:
    count += 1
    line = line.strip()
    relation = line.split('\t')[0]
    mainEntity = line.split('\t')[1 + relation2role[relation]]
    if relation + '\t' + mainEntity  in relationMainEntityDic:
        f_new_candidate.write(line + '\n')
f_new_candidate.close()
f_NN_candidate.close()