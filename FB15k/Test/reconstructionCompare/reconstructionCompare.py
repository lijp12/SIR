#coding = utf-8

import codecs

f_hit_test = codecs.open('../../Reconstruction/hitTest.txt', 'r', 'utf-8')
hitTestList = {}
for line in f_hit_test:
    line = line.strip()
    hitTestList[line] = 0
f_hit_test.close()

f_hit_test_rank = codecs.open('./hitTestRankBaseAll.txt', 'w', 'utf-8')
f_not_hit_test_rank = codecs.open('./noeHitTestBaseAll.txt', 'w', 'utf-8')
f_all_rank = codecs.open('../../Reconstruction/Orank/rankResult.txt', 'r', 'utf-8')
for line in f_all_rank:
    line = line.strip()
    triplet = line.split('\t')[0] + '\t' + line.split('\t')[1] + '\t' + line.split('\t')[2]
    if triplet in hitTestList:
        f_hit_test_rank.write(line + '\n')
    else:
        f_not_hit_test_rank.write(line + '\n')
f_all_rank.close()
f_not_hit_test_rank.close()
f_hit_test_rank.close()