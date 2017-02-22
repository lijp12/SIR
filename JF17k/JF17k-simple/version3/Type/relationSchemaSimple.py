#coding = utf-8

import codecs

f_relation = codecs.open('../relation.txt', 'r', 'utf-8')
relationDic = {}
for line in f_relation:
    line = line.strip()
    relationDic[line.split('\t')[0]] = 0
f_relation.close()

f_relation_schema = codecs.open('../../../../JF17k/totalRelationType.txt', 'r', 'utf-8')
f_relation_schema_simple = codecs.open('./relationSchemaSimple.txt', 'w', 'utf-8')
for line in f_relation_schema:
    relation = line.split('\t')[0]
    if relation in relationDic:
        f_relation_schema_simple.write(line)
f_relation_schema_simple.close()
f_relation_schema.close()