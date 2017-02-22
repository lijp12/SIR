#coding = utf-8

import codecs


def getCliqueList(cliqueList,ind,binaryList,binaryRelation2pairDic):
    newCliqueList = []
    print(ind)
    count = 0
    for clique in cliqueList:
        ind1 = 0
        while(ind1 < ind):
            relation = binaryList[ind1] + '/' + binaryList[ind]
            if relation in binaryRelation2pairDic:
                if clique[ind1] in binaryRelation2pairDic[relation]:
                    if ind1 == 0:
                        SET = binaryRelation2pairDic[relation][clique[ind1]]
                    else:
                        SET = SET & binaryRelation2pairDic[relation][clique[ind1]]
                    ind1 += 1
                else:
                    SET = set()
                    break
            else:
                SET = set()
                break
        if len(SET) > 0:
            for entity in SET:
                newClique = list(clique)
                newClique.append(entity)
                newCliqueList.append(newClique)
                count += 1
    print(count)
    return newCliqueList

def getPair(relation,binaryRelation2pairDic):
    pairList = []
    if relation in binaryRelation2pairDic:
        for key,tailSet in binaryRelation2pairDic[relation].items():
            for tail in tailSet:
                pairList.append([key,tail])
    return pairList

def getClique(binaryList, binaryRelation2pairDic):
    schema = len(binaryList)
    print(schema)
    if schema == 1:
        relation = binaryList[0]
        cliqueList = getPair(relation, binaryRelation2pairDic)
        return cliqueList
    else:
        ind = 2
        relation = binaryList[0] + '/' + binaryList[1]
        cliqueList = getPair(relation, binaryRelation2pairDic)
        while (ind < schema):
            cliqueList = getCliqueList(cliqueList, ind, binaryList,binaryRelation2pairDic)
            ind += 1
        return cliqueList


f_triplet = codecs.open('../NNFilt/NNTripletSum.txt', 'r', 'utf-8')
#f_triplet = codecs.open('./tripletResult.txt', 'r', 'utf-8')
binaryRelation2pairDic = {}
for line in f_triplet:
    line = line.strip()
    relation = line.split('\t')[0]
    head = line.split('\t')[1]
    tail = line.split('\t')[2]
    if relation in binaryRelation2pairDic:
        if head in binaryRelation2pairDic[relation]:
            binaryRelation2pairDic[relation][head].add(tail)
        else:
            binaryRelation2pairDic[relation][head] = set()
            binaryRelation2pairDic[relation][head].add(tail)
    else:
        binaryRelation2pairDic[relation] = {}
        binaryRelation2pairDic[relation][head] = set()
        binaryRelation2pairDic[relation][head].add(tail)
f_triplet.close()
print("load triplet over!")

f_mul_binary = codecs.open('./multi2binary.txt', 'r', 'utf-8')
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

stringList = []
for multiRelation,binaryList in mul2binary.items():
    print(multiRelation)
    cliqueList = getClique(binaryList, binaryRelation2pairDic)
    for clique in cliqueList:
        string = multiRelation
        for entity in clique:
            string += ('\t' + entity)
        stringList.append(string)

f_result = codecs.open('./instanceResult.txt', 'w', 'utf-8')
for string in set(stringList):
    f_result.write(string + '\n')
f_result.close()
