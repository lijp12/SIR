#coding = utf-8

import codecs

f_relation_schema = codecs.open('./genData/allRelationSchema.txt', 'r', 'utf-8')
f_relation_schema_expected_both = codecs.open('./genData/relationSchemaBoth.txt', 'w', 'utf-8')
for line in f_relation_schema:
    line = line.strip()
    relation = line.split('\t')[0]
    headType = line.split('\t')[1]
    tailType = line.split('\t')[2]
    if ((headType != 'null') & (tailType != 'null')):
        f_relation_schema_expected_both.write(line + '\n')
f_relation_schema_expected_both.close()
f_relation_schema.close()
