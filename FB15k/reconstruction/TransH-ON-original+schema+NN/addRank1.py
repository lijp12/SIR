#coding = utf-8

import codecs

f_result_rank = codecs.open('./rankResult.txt', 'r', 'utf-8')
resultRankDic = {}
for line in f_result_rank:
    line = line.strip()
    relation = line.split('\t')[0]
    headEntity = line.split('\t')[1]
    tailEntity = line.split('\t')[2]
    resultRankDic[relation + '\t'+ headEntity + '\t' + tailEntity] = line
f_result_rank.close()

f_hitTest = codecs.open('../../Test/hitTest.txt', 'r', 'utf-8')
f_new_rank_result = codecs.open('./newRankResult.txt', 'w', 'utf-8')
for line in f_hitTest:
    line = line.strip()
    if line not in resultRankDic:
        f_new_rank_result.write(line + '\t' + '1' + '\t' + '1' + '\n')
    else:
        f_new_rank_result.write(resultRankDic[line] + '\n')
f_hitTest.close()
f_new_rank_result.close()