import random

p_pig_train = '../raw_data/train.txt'
p_dog_train = '../trans_data/dog.txt'
p_pig_out = '../trans_data/pig.simple5'
p_dog_out = '../trans_data/dog.simple5'
p_pig_valid = '../trans_data/test.simple5'
p_dog_valid = '../trans_data/valid.simple5'

rates = {'CLASS=VIDEO' : 0.5}


def stat(p_in, p_out):
    session = [set(), set()]
    labels = []
    
    fo = open(p_out, 'w')
    tot_line = 0
    for line in open(p_in):
        if not line.strip():
            session_label = ''
            session_flag = True
            positive_count = 0
            for key in labels:
                label, query = key.split('\t')
                if label.find('TEST')>=0 or label.find('KNOWN')>=0:
                    if positive_count < 1: session_flag = False
                    #elif positive_count == 1: positive_count = 0 
                    #else: positive_count = 0.5
                    else: positive_count = 0
                elif session_flag:
                    if not session_label: 
                        session_label = label
                        positive_count += 1
                    elif session_label != label: 
                        session_flag = False
                    else:
                        positive_count += 1
            if session[0] and session_label and session_flag and positive_count > 0:
                if session[1] and len(session[1])<=10 and len(session[0])<=5:
                    rate = rates.get(session_label, 1.0)
                    if random.random()<=rate:
                        fo.write('%s\t%s\t%s\n' % (session_label, ';'.join(session[0]), ';'.join(session[1])))
            session = [set(), set()]
            labels = []
            continue

        try:
            label, query, title = line.strip().split('\t')
        except:
            label, query = line.strip().split('\t')
            title = '-'

        key = label + '\t' + query
        if not labels or labels[-1] != key:
            labels.append(key)
        session[0].add(query)
        if title and title!='-':
            session[1].add(title)

        tot_line += 1
        #if tot_line == 1000000: break
    fo.close()
            
def valid(p_in, p_out):
    session = [set(), set()]
    has_test = False

    fo = open(p_out, 'w')
    tot_line = 0
    for line in open(p_in):
        if not line.strip():
            if has_test and session[1] and len(session[1])<=10 and len(session[0])<=5:
                fo.write('%s\t%s\t%s\n' % (0, ';'.join(session[0]), ';'.join(session[1])))
            session = [set(), set()]
            has_test = False
            continue
        try:
            label, query, title = line.strip().split('\t')
        except:
            label, query = line.strip().split('\t')
            title = '-'

        if label.find('TEST') >= 0:
            has_test = True
        session[0].add(query)
        if title and title!='-':
            session[1].add(title)

        tot_line += 1
        #if tot_line == 10000: break
    fo.close()

stat(p_pig_train, p_pig_out)
#stat(p_dog_train, p_dog_out)
valid(p_pig_train, p_pig_valid)
#valid(p_dog_train, p_dog_valid)
