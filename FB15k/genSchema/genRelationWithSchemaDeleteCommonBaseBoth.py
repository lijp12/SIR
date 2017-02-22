#coding = utf-8

import codecs

f_relation_schema = codecs.open('./genData/relationSchemaBoth.txt', 'r', 'utf-8')
f_relation_schema_delete_common = codecs.open('./genData/relationSchemaDeleteCommon.txt', 'w', 'utf-8')
count = 0
for line in f_relation_schema:
    line = line.strip()
    headType = line.split('\t')[1]
    tailType = line.split('\t')[2]
    if ((headType != 'common.topic') & (tailType != 'common.topic')):
        f_relation_schema_delete_common.write(line + '\n')
        count += 1
f_relation_schema.close()
f_relation_schema_delete_common.close()
print(count)