#coding = utf-8

import codecs

f_relation_type = codecs.open('./relationSchemaSimple.txt', 'r', 'utf-8')
TypeSet = {}
for line in f_relation_type:
    line = line.strip()
    typeList = line.split('\t')[1:]
    for type in typeList:
        TypeSet[type] = 0
f_relation_type.close()

f_entity_type = codecs.open('./entityType.txt', 'r', 'utf-8')
f_entity_type_simple = codecs.open('./entityTypeSimple.txt', 'w', 'utf-8')
for line in f_entity_type:
    line = line.strip()
    string = line.split('\t')[1]
    typeList = line.split('\t')[2:]
    count = 0
    for type in typeList:
        if type in TypeSet:
            count += 1
            string += ('\t' + type)
    string = str(count) + '\t' + string
    f_entity_type_simple.write(string + '\n')
f_entity_type_simple.close()
f_entity_type.close()