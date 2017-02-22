#coding = utf-8

import codecs
import random

f_triplet = codecs.open('../../../NNFilt/NNTripletSum.txt', 'r', 'utf-8')
binaryRelation2pairDic = {}
for line in f_triplet:
    line = line.strip()
    relation = line.split('\t')[0]
    head = line.split('\t')[1]
    tail = line.split('\t')[2]
    if relation in binaryRelation2pairDic:
        if head in binaryRelation2pairDic[relation][0]:
            binaryRelation2pairDic[relation][0][head].add(tail)
        else:
            binaryRelation2pairDic[relation][0][head] = set()
            binaryRelation2pairDic[relation][0][head].add(tail)

        if tail in binaryRelation2pairDic[relation][1]:
            binaryRelation2pairDic[relation][1][tail].add(head)
        else:
            binaryRelation2pairDic[relation][1][tail] = set()
            binaryRelation2pairDic[relation][1][tail].add(head)
    else:
        headDic = {}
        headDic[head] = set()
        headDic[head].add(tail)
        tailDic = {}
        tailDic[tail] = set()
        tailDic[tail].add(head)
        binaryRelation2pairDic[relation] = [headDic,tailDic]
f_triplet.close()
print("load triplet over!")

f_mul_binary = codecs.open('../../../instanceReconstruction/multi2binary.txt', 'r', 'utf-8')
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
print("load multi2binary over!")

def getClique(binaryList, cliqueList, foundRoleList, pick_role, binaryRelation2pairDic):
    newCliqueList = []
    index = 0
    for role in foundRoleList:
        if pick_role > role:
            index += 1
        else:
            break
    for clique in cliqueList:
        ind1 = 0
        for entity in clique:
            foundRole = foundRoleList[ind1]
            if foundRole < pick_role:
                comRelation = binaryList[foundRole] + '/' + binaryList[pick_role]
                foundRole = 0
            else:
                comRelation = binaryList[pick_role] + '/' + binaryList[foundRole]
                foundRole = 1
            if comRelation in binaryRelation2pairDic:
                if entity in binaryRelation2pairDic[comRelation][foundRole]:
                    if ind1 == 0:
                        SET = binaryRelation2pairDic[comRelation][foundRole][entity]
                    else:
                        SET = SET & binaryRelation2pairDic[comRelation][foundRole][entity]
                else:
                    SET = set()
            else:
                SET = set()
            ind1 += 1
        for entity in SET:
            newClique = list(clique)
            newClique.insert(index,entity)
            newCliqueList.append(newClique)
    return newCliqueList


def getPair(relation, mainRole, mainEntity, binaryRelation2pairDic):
    pairList = []
    if relation in binaryRelation2pairDic:
        if mainEntity in binaryRelation2pairDic[relation][mainRole]:
            entitySet = binaryRelation2pairDic[relation][mainRole][mainEntity]
        else:
            entitySet = set()
        if mainRole == 0:
            for entity in entitySet:
                pairList.append([mainEntity, entity])
        else:
            for entity in entitySet:
                pairList.append([entity, mainEntity])
    return pairList


def getCliqueList(binaryList, mainEntity, mainRole, binaryRelation2pairDic):
    schema = len(binaryList)

    if schema == 1:
        cliqueList = getPair(binaryList[0], mainRole, mainEntity, binaryRelation2pairDic)
    else:
        foundRoleList = [mainRole]
        roleList = list(range(schema))

        roleList.remove(mainRole)
        pick_role = roleList[random.randint(0, len(roleList) - 1)]

        roleList.remove(pick_role)
        foundRoleList.append(pick_role)
        foundRoleList.sort()

        if mainRole < pick_role:
            relation = binaryList[mainRole] + '/' + binaryList[pick_role]
            cliqueList = getPair(relation, 0, mainEntity, binaryRelation2pairDic)
        else:
            relation = binaryList[pick_role] + '/' + binaryList[mainRole]
            cliqueList = getPair(relation, 1, mainEntity, binaryRelation2pairDic)

        while len(roleList) > 0:
            pick_role = roleList[random.randint(0,len(roleList) - 1)]
            roleList.remove(pick_role)

            cliqueList = getClique(binaryList, cliqueList, foundRoleList, pick_role, binaryRelation2pairDic)
            foundRoleList.append(pick_role)
            print(len(foundRoleList))
            print(len(cliqueList))
            foundRoleList.sort()
    return cliqueList

f_main_role = codecs.open('../../mainRole.txt', 'r', 'utf-8')
relation2MainRole = {}
for line in f_main_role:
    line = line.strip()
    multiRelation = line.split('\t')[0]
    roleIndex = int(line.split('\t')[1])
    relation2MainRole[multiRelation] = roleIndex
f_main_role.close()

f_hit_test = codecs.open('../splitResult/multiRelationMainEntity3.0.txt', 'r', 'utf-8')
testRelationMainEntityDic = {}
for line in f_hit_test:
    line = line.strip()
    testRelationMainEntityDic[line] = 0
f_hit_test.close()
print(len(testRelationMainEntityDic))

f_candidate_clique = codecs.open('../candidateClique/candidateClique3.txt', 'w', 'utf-8')
count = 0
ind = 0
for multiRelationMainEntity in testRelationMainEntityDic.keys():
    ind += 1
    print(ind)
    print(multiRelationMainEntity)
    mainEntity = multiRelationMainEntity.split('\t')[1]
    multiRelation = multiRelationMainEntity.split('\t')[0]
    mainRole = relation2MainRole[multiRelation] - 1
    string = multiRelationMainEntity
    f_candidate_clique.write(string + '\n')
    cliqueList = getCliqueList(mul2binary[multiRelation], mainEntity, mainRole, binaryRelation2pairDic)
    count += (len(cliqueList))
    f_candidate_clique.write(str(len(cliqueList)) + '\n')
    for clique in cliqueList:
        string = ''
        for entity in clique:
            string += (entity + '\t')
        f_candidate_clique.write(string[:-1] + '\n')
f_candidate_clique.close()
print(count)