import random
import gc

p_train = '../raw_data/train.txt'
p_test = '../raw_data/test.txt'
p_dog = '../trans_data/dog.txt'
p_valid = '../trans_data/valid.txt'

def norm(a2b):
    gc.disable()
    for a in a2b:
        tot = sum([a2b[a][b] for b in a2b[a]]) 
        for b in a2b[a]: a2b[a][b] /= tot
    gc.enable()

def multiple(a2b, b2c):
    gc.disable()
    a2c = {}
    for a in a2b:
        if a not in a2c: a2c[a] = {}
        for b in a2b[a]:
            v1 = a2b[a][b]
            if b in b2c:
                for c in b2c[b]:
                    if c not in a2c[a]: a2c[a][c] = 0
                    v2 = b2c[b][c]
                    a2c[a][c] += a2b[a][b] * b2c[b][c]
    gc.enable()
    return a2c

class Converter(object):
    def __init__(self):
        self.max_idx = 0
        self.s_dict = {}
    def str2id(self, s):
        if s not in self.s_dict: 
            self.s_dict[s] = self.max_idx
            self.s_dict[self.max_idx] = s
            self.max_idx += 1
        return self.s_dict[s]
    def id2str(self, i):
        return self.s_dict.get(i, '')

def build(p_in):
    #gc.disable()
    convert = Converter()
    
    all_to_class = {}
    query_to_all = {}

    print 'loading from', p_in 

    session_query = set()
    session_all = set()
    for line in open(p_in):
        if not line.strip():
            #session end
            for q in session_query:
                for q2 in session_all:
                    if q!=q2:
                        if q not in query_to_all: query_to_all[q] = {}
                        query_to_all[q][q2] = query_to_all[q].get(q2, 0) + 1.

            session_query = set()
            session_all = set()
            continue

        try:
            labels, query, title = line.strip().split('\t')
        except:
            labels, query = line.strip().split('\t')
            title = '-'

        query = convert.str2id(query)
        session_query.add(query)
        session_all.add(query)
        if title and title != '-':
            title = convert.str2id('t_' + title)
            session_all.add(title)

        if labels!='CLASS=TEST' and labels!='CLASS=UNKNOWN':
            label_list = labels.split(' | ')
            for label in label_list:
                label = convert.str2id(label)
                if query not in all_to_class: all_to_class[query] = {}
                all_to_class[query][label] = all_to_class[query].get(label, 0) + 1.
                if title and title != '-':
                    if title not in all_to_class: all_to_class[title] = {}
                    all_to_class[title][label] = all_to_class[title].get(label, 0) + 1.
    print 'load finished'

    norm(all_to_class)
    norm(query_to_all)
    print 'normalize finished'

    return all_to_class, query_to_all, convert

def markov(p_in, p_query, p_out1, p_out2):
    all_to_class, query_to_all, convert = build(p_in)

    query_to_class1 = multiple(query_to_all, all_to_class)
    print 'round 1 finished'
    query_to_class2 = multiple(query_to_all, query_to_class1)
    print 'round 2 finished'

    fo1 = open(p_out1, 'w') 
    fo2 = open(p_out2, 'w')    
    for line in open(p_query):
        query = line.strip()
        query = convert.str2id(query)
        if query not in query_to_class1:
            fo1.write('\n')
            fo2.write('\n')

        query = convert.id2str(query)
        rs = ['%s:%s' % (convert.id2str(k), v) for k, v in query_to_class1.get(query, {}).items()]
        rs2 = ['%s:%s' % (convert.id2str(k), v) for k, v in query_to_class2.get(query, {}).items()]
        fo1.write('%s\n' % (' || '.join(rs))) 
        fo2.write('%s\n' % (' || '.join(rs2))) 
    fo1.close()
    fo2.close()
    print 'write to file finished'

markov(p_train, p_test, 'pred_markov1', 'pred_markov2')
#markov(p_dog, p_valid, 'dog_pred1', 'dog_pred2')

