#coding = utf-8

import codecs
import numpy as np
f_main_role = codecs.open('../mainRole.txt', 'r', 'utf-8')
relation2primaryKey = {}
for line in f_main_role:
    line = line.strip()
    relation = line.split('\t')[0]
    primaryKeyIndex = int(line.split('\t')[1]) - 1
    relation2primaryKey[relation] = primaryKeyIndex
f_main_role.close()

f_relation_schema = codecs.open('../multi2binary.txt', 'r', 'utf-8')
relation2schema = {}
for line in f_relation_schema:
    line = line.strip()
    relation = line.split('\t')[0]
    schema = int(line.split('\t')[1])
    relation2schema[relation] = schema
f_relation_schema.close()

f_rank_result = codecs.open('./finalRank.txt', 'r', 'utf-8')
primaryKeyDic = {}
for line in f_rank_result:
    line = line.strip()
    relation = line.split('\t')[0]
    entityList = line.split('\t')[1:]
    primaryKey = relation + '\t' + entityList[relation2primaryKey[relation]]
    rank = int(entityList[-1])
    totalRank = float(entityList[-2])
    if primaryKey not in primaryKeyDic:
        primaryKeyDic[primaryKey] = [rank]
        standRank = totalRank
    else:
        primaryKeyDic[primaryKey].append(rank)
f_rank_result.close()

# f_rank_base_primaryKey = codecs.open('./rankBasePrimaryKey.txt', 'w', 'utf-8')
# sumRank = 0
# count = 0
# top10 = 0
# top1 = 0
# for key, rankList in primaryKeyDic.items():
#     count += 1
#     meanRank = np.mean(rankList)
#     sumRank += meanRank
#     if meanRank <= 10:
#         top10 += 1
#         if meanRank <= 1:
#             top1 += 1
#     f_rank_base_primaryKey.write(key + '\t' + str(meanRank) + '\n')
# f_rank_base_primaryKey.close()
# print(sumRank / count)
# print(top10 / count)
# print(top1 / count)

count = 0
sumRank = 0
top1 = 0
top10 = 0
top20 = 0
top30 = 0
top40 = 0
top50 = 0
top100 = 0
for key, rankList in primaryKeyDic.items():
    relation = key.split('\t')[0]
    schema = relation2schema[relation]
    if schema != 0:
        count += 1
        meanRank = np.mean(rankList)
        sumRank += meanRank
        if meanRank <= 100:
            top100 += 1
            if meanRank <= 50:
                top50 += 1
                if meanRank <= 40:
                    top40 += 1
                    if meanRank <= 30:
                        top30 += 1
                        if meanRank <= 20:
                            top20 += 1
                            if meanRank <= 10:
                                top10 += 1
                                if meanRank <= 1:
                                    top1 += 1
print(count)
print(top1 / count * 100)
print(top10 / count * 100)
print(top20 / count * 100)
print(top30 / count * 100)
print(top40 / count * 100)
print(top50 / count * 100)
print(top100 / count * 100)
print(sumRank / count)