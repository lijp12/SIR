#coding = utf-8

import codecs

f_train = codecs.open('../JF17k-simple/version1/train.txt', 'r', 'utf-8')
relation2cliqueList = {}
for line in f_train:
    line = line.strip()
    relation = line.split('\t')[0]
    clique = line.split('\t')[1:]
    if relation in relation2cliqueList:
        relation2cliqueList[relation].append(clique)
    else:
        relation2cliqueList[relation] = [clique]
f_train.close()

f_result = codecs.open('./mainRole.txt', 'w', 'utf-8')
for relation, cliqueList in relation2cliqueList.items():
    schema = len(cliqueList[0])
    ind = 0
    roleEntity = []
    while ind < schema:
        roleEntity.append(set())
        ind += 1
    for clique in cliqueList:
        ind = 0
        while ind < schema:
            roleEntity[ind].add(clique[ind])
            ind += 1
    ind = 0
    string = relation
    while ind < schema:
        string += ('\t' + str(len(roleEntity[ind])))
        ind += 1
    f_result.write(string + '\n')
f_result.close()