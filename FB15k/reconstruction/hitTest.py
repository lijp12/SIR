#coding = utf-8

import codecs

f_triple_sum = codecs.open('../NNFiltPair/testCandidateTriplet.txt', 'r', 'utf-8')
tripletDic = {}
for line in f_triple_sum:
    line = line.strip()
    tripletDic[line] = 0
f_triple_sum.close()

f_test = codecs.open('../FB15k-simple/test.txt', 'r', 'utf-8')
f_hit_test = codecs.open('./hitTest.txt', 'w', 'utf-8')
hit_test = 0
count_test = 0
for line in f_test:
    count_test += 1
    line = line.strip()
    if line in tripletDic:
        hit_test += 1
        f_hit_test.write(line + '\n')
f_hit_test.close()
f_test.close()

print(1.0 * hit_test / count_test)
