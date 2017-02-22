#coding = utf-8

import codecs

f_relation_schema = codecs.open('./relationSchemaSimple.txt', 'r', 'utf-8')
typeSet = set()
for line in f_relation_schema:
    line = line.strip()
    typeList = line.split('\t')[1:]
    for type in typeList:
        typeSet.add(type)
f_relation_schema.close()
print(len(typeSet))

###保存type
ind = 0
f_type = codecs.open('./type.txt', 'w', 'utf-8')
for type in typeSet:
    f_type.write(type + '\n')
    ind += 1
f_type.close()
print(max)
print(ind)