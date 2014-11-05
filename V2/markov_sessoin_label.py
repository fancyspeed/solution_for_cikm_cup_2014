
p_train = '../raw_data/train.txt'
p_test = '../raw_data/test.txt'
p_dog = '../trans_data/dog.txt'
p_valid = '../trans_data/valid.txt'

def markov(p_in, p_query, p_out):
    test_label = {}
    unknown_label = {}
    test_unknown = {}

    label_query = {}
    unknown_query = {}
    test_query = {}
    session = [] 
    for line in open(p_in):
        if not line.strip():
            n_query = len(label_query) + len(unknown_query) + len(test_query) 
            label_dict = {}
            for query, label in label_query.items():
                label_dict[label] = label_dict.get(label, 0) + 1
            if len(label_dict) <= 1 or (len(label_dict) == 2 and (label_dict.keys()[0].find(label_dict.keys()[1])==0 or label_dict.keys()[1].find(label_dict.keys()[0])==0)):
              for query in test_query:
                if query not in test_label: 
                    test_label[query] = {}
                for query2, label in label_query.items():
                    test_label[query][label] = test_label[query].get(label, 0) + 1
                if query not in test_unknown:
                    test_unknown[query] = {}
                for query2 in unknown_query:
                    test_unknown[query][query2] = test_unknown[query].get(query2, 0) + 1
              for query in unknown_query:
                if query not in unknown_label: 
                    unknown_label[query] = {}
                for query2, label in label_query.items():
                    unknown_label[query][label] = unknown_label[query].get(label, 0) + 1
            else:
                #print session
                pass
            label_query = {}
            unknown_query = {}
            test_query = {}
            session = []
            continue
        label, query = line.strip().split('\t')[:2]
        label = ' | '.join(sorted(label.split(' | ')))
        if not session or query != session[-1][1]:
            session.append( (label, query) )
        if label=='CLASS=TEST':
            test_query[query] = 1
        elif label=='CLASS=UNKNOWN':
            if query.count(' ') > 1:
                unknown_query[query] = 1
        else:
            label_query[query] = label

    with open(p_out, 'w') as fo:
        for line in open(p_query):
            query = line.strip()
            if query in test_label and test_label[query]:
                s = ['%s:%s' % (k, v) for k, v in test_label[query].items()]
                fo.write('%s\n' % (' || '.join(s)))
            elif query in test_unknown:
                label_dict = {}
                for query2, v1 in test_unknown[query].items():
                    if query2 in unknown_label:
                        for label, v2 in unknown_label[query2].items():
                            label_dict[label] = label_dict.get(label, 0) + v1*v2
                if label_dict:
                    s = ['%s:%s' % (k, v) for k, v in label_dict.items()]
                    fo.write('%s\n' % (' || '.join(s)))
                else:
                    fo.write('\n')
            else:
                fo.write('\n')

markov(p_dog, p_valid, 'pred_session_dog.txt')
markov(p_train, p_test, 'pred_session_pig.txt')

