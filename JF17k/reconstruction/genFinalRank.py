#coding = utf-8

import codecs
import os

instanceDic = {}
f_final_rank = codecs.open('./finalRank.txt', 'w', 'utf-8')
for file in os.listdir('./rank'):
    f = codecs.open('./rank/' + file, 'r', 'utf-8')
    for line in f:
        line = line.strip()
        f_final_rank.write(line + '\n')
        instance = ''
        for factor in line.split('\t')[:-2]:
            instance += (factor + '\t')
        instanceDic[instance[:-1]] = 0
    f.close()

print(len(instanceDic))

testDic = {}
f_test = codecs.open('../hitTest.txt', 'r','utf-8')
for line in f_test:
    line = line.strip()
    instanceIndex = line.split('\t')[0]
    testDic[line.replace(instanceIndex,'').strip()] = 0
f_test.close()

# print("instance:")
#
# for instance in instanceDic.keys():
#     if instance not in testDic:
#         print(instance)

print("test:")
count = 0
for testInstance in testDic.keys():
    if testInstance not in instanceDic:
        f_final_rank.write(testInstance + '\t' + '0.5' + '\t' + '1' + '\n')
        print(testInstance)
        count += 1
f_final_rank.close()
print(count)