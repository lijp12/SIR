#coding = utf-8

import codecs

f_relation1 = codecs.open('../JF17k-simple/version1/relation.txt', 'r', 'utf-8')
schemaDic = {}
multi2binaryDic = {}
relation1List = []
for line in f_relation1:
	line = line.strip()
	relation = line.split('\t')[0]
	schemaDic[relation] = int(line.split('\t')[1])
	multi2binaryDic[relation] = []
	relation1List.append(relation)
f_relation1.close()
print(len(multi2binaryDic))

f_relation3 = codecs.open('../JF17k-simple/version3/relation.txt', 'r', 'utf-8')
#relation3List = []
for line in f_relation3:
	line = line.strip()
	relation  = line.split('\t')[0]
	#relation3List.append(relation)
	if '/' in relation:
		length = len(relation.split('/')[0].split('.')[-1]) + 1
		multi2binaryDic[relation.split('/')[0][:-length]].append(relation)
	else:
		multi2binaryDic[relation].append(relation)
f_relation3.close()

f_multi2binary = codecs.open('./multi2binary.txt', 'w', 'utf-8')	
for relation3,comRelationList in multi2binaryDic.items():
	f_multi2binary.write(relation3 + '\t' + str(schemaDic[relation3]))
	if len(comRelationList) == 1:
		f_multi2binary.write('\n')
		continue
	else:
		binaryRelationDic = {}
		for comRelation in comRelationList:
			role1 = comRelation.split('/')[0]
			role2 = comRelation.split('/')[1]
			binaryRelationDic[role1] = 0
			binaryRelationDic[role2] = 0
		for comRelation in comRelationList:
			role1 = comRelation.split('/')[0]
			binaryRelationDic[role1] += 1
		string = ''
		for factor in sorted(binaryRelationDic.items(),key=lambda d:d[1],reverse = True):
			string += ('\t' + factor[0])
		f_multi2binary.write(string)
		f_multi2binary.write('\n')
f_multi2binary.close()
		
		

	

