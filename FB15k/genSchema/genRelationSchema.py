#coding = utf-8

import codecs

f_relation = codecs.open('../data_fb15k/relation.txt', 'r', 'utf-8')
relationList = []
relation2headType = {}
relation2tailType = {}
for line in f_relation:
    line = line.strip()
    relation = line[:-1].strip()
    relationList.append(relation)
    if '.' in relation:
        headRelation = relation.split('.')[0]
        tailRelation = relation.split('.')[1]
        relation2headType[headRelation] = 'null'
        relation2tailType[tailRelation] = 'null'
    else:
        relation2headType[relation] = 'null'
        relation2tailType[relation] = 'null'
f_relation.close()

f_domain = codecs.open('./data/domain.list', 'r', 'utf-8')
for line in f_domain:
    line = line.strip()
    line = line[:-1].strip()
    relation = '/' + line.split('\t')[0][1:-1].split('/')[-1].replace('.','/')
    headType = line.split('\t')[2][1:-1].split('/')[-1]
    relation2headType[relation] = headType
f_domain.close()

f_range = codecs.open('./data/range.list', 'r', 'utf-8')
for line in f_range:
    line = line.strip()
    line = line[:-1].strip()
    relation = '/' + line.split('\t')[0][1:-1].split('/')[-1].replace('.','/')
    tailType = line.split('\t')[2][1:-1].split('/')[-1]
    relation2tailType[relation] = tailType
f_range.close()

f_relation_schema = codecs.open('./genData/allRelationSchema.txt', 'w', 'utf-8')
for relation in relationList:
    if '.' in relation:
        headRelation = relation.split('.')[0]
        tailRelation = relation.split('.')[1]
        headType = relation2headType[headRelation]
        tailType = relation2tailType[tailRelation]
    else:
        headType = relation2headType[relation]
        tailType = relation2tailType[relation]
    f_relation_schema.write(relation + '\t' + headType + '\t' + tailType + '\n')
f_relation_schema.close()
