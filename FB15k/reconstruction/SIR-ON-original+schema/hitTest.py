#coding = utf-8

import codecs

f_candidate = codecs.open('./candidateTriplet.txt', 'r', 'utf-8')
candidateDic ={}
for line in f_candidate:
    line = line.strip()
    candidateDic[line] = 0
f_candidate.close()

f_test = codecs.open('../../FB15k-simple/test.txt', 'r', 'utf-8')
f_hit_test = codecs.open('./hitTest.txt', 'w', 'utf-8')
for line in f_test:
    line = line.strip()
    if line in candidateDic:
        f_hit_test.write(line + '\n')
f_hit_test.close()
f_test.close()