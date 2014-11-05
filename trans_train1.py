
p_train = '../trans_data/train_refine.txt'
p_dog = '../trans_data/dog_refine.txt'
#p_train = '../raw_data/train.txt'
#p_dog = '../trans_data/dog.txt'
p_test = '../raw_data/test.txt'
p_valid = '../trans_data/valid.txt'

s_train = '../trans_data/train.simple'
s_test = '../trans_data/test.simple'
s_dog = '../trans_data/dog.simple'
s_valid = '../trans_data/valid.simple'

def trans(in1, in2, out1, out2):
    train_dict = {}
    test_dict = {}

    # for session
    session_train_query = {}
    session_test_query = {}
    session_labels = {}
    session_click = {}


    for line in open(in1):
        if not line.strip():
            #session end
            for query in session_train_query:
                #if len(session_labels) == 1:
                for q2 in session_train_query:
                    if query != q2:
                        label = session_train_query[q2]
                        train_dict[query][2][label] = train_dict[query][2].get(label, 0) + 1
                        train_dict[query][3][q2] = train_dict[query][3].get(q2, 0) + 1
                for title in session_click:
                    train_dict[query][4][title] = train_dict[query][4].get(title, 0) + 1
            for query in session_test_query:
                #if len(session_labels) == 1:
                for q2 in session_train_query:
                    if query != q2:
                        label = session_train_query[q2]
                        test_dict[query][2][label] = test_dict[query][2].get(label, 0) + 1
                        test_dict[query][3][q2] = test_dict[query][3].get(q2, 0) + 1
                for title in session_click:
                    test_dict[query][4][title] = test_dict[query][4].get(title, 0) + 1
            session_train_query = {}
            session_test_query = {}
            session_labels = {}
            session_click = {}
            continue

        try:
            label, query, title = line.strip().split('\t')
        except:
            label, query = line.strip().split('\t')
            title = '-'
        #label = ' | '.join(sorted(label.split(' | ')))

        if title and title != '-':
            session_click[title] = session_click.get(title, 0) + 1

        if label.startswith('CLASS=TEST'):
            if query not in test_dict: 
                test_dict[query] = [label, {}, {}, {}, {}]
            if title and title != '-':
                test_dict[query][1][title] = test_dict[query][1].get(title, 0) + 1
            session_test_query[query] = 1
        elif not label.startswith('CLASS=UNKNOWN'):
            if query not in train_dict: 
                train_dict[query] = [{}, {}, {}, {}, {}]
            train_dict[query][0][label] = train_dict[query][0].get(label, 0) + 1
            if title and title != '-':
                train_dict[query][1][title] = train_dict[query][1].get(title, 0) + 1
            session_labels[label] = 1
            session_train_query[query] = label.replace(' ', '')

    n_top_title = 30
    n_top_label = 3
    n_top_query = 10 
    n_top_session_title = 30 

    with open(out1, 'w') as ft:
        for query in train_dict:
            label = sorted(train_dict[query][0].items(), key=lambda d:-d[1])[0][0]

            titles = sorted(train_dict[query][1].items(), key=lambda d:-d[1])
            title_pairs = ['%s:%s' % (v[0], v[1]) for v in titles[:n_top_title+1]]

            labels = sorted(train_dict[query][2].items(), key=lambda d:-d[1])
            label_pairs = ['%s:%s' % (v[0], v[1]) for v in labels[:n_top_label+1]]
            tot_label = float(sum(train_dict[query][2].values()))
            label_pairs += ['f%s:%s' % (v[0], v[1]/tot_label) for v in labels[:n_top_label+1]]

            queries = sorted(train_dict[query][3].items(), key=lambda d:-d[1])
            query_pairs = []
            query_pairs = ['%s:%s' % (v[0], v[1]) for v in queries[:n_top_query+1]]

            stitles = sorted(train_dict[query][4].items(), key=lambda d:-d[1])
            stitle_pairs = ['%s:%s' % (v[0], v[1]) for v in stitles[:n_top_session_title+1]]

            stat_pairs = []

            ft.write('%s\t%s\t%s\t%s\t%s\t%s\t%s\n' % (label, query, ';'.join(title_pairs), ';'.join(label_pairs), ';'.join(stat_pairs), ';'.join(query_pairs), ';'.join(stitle_pairs)))

    with open(out2, 'w') as fo:
        for query in test_dict:
            label = test_dict[query][0]

            titles = sorted(test_dict[query][1].items(), key=lambda d:-d[1])
            title_pairs = ['%s:%s' % (v[0], v[1]) for v in titles[:n_top_title+1]]

            labels = sorted(test_dict[query][2].items(), key=lambda d:-d[1])
            label_pairs = ['%s:%s' % (v[0], v[1]) for v in labels[:n_top_label+1]]
            tot_label = float(sum(test_dict[query][2].values()))
            label_pairs += ['f%s:%s' % (v[0], v[1]/tot_label) for v in labels[:n_top_label+1]]

            queries = sorted(test_dict[query][3].items(), key=lambda d:-d[1])
            query_pairs = []
            query_pairs = ['%s:%s' % (v[0], v[1]) for v in queries[:n_top_query+1]]

            stitles = sorted(test_dict[query][4].items(), key=lambda d:-d[1])
            stitle_pairs = ['%s:%s' % (v[0], v[1]) for v in stitles[:n_top_session_title+1]]

            stat_pairs = []

            fo.write('%s\t%s\t%s\t%s\t%s\t%s\t%s\n' % (label, query, ';'.join(title_pairs), ';'.join(label_pairs), ';'.join(stat_pairs), ';'.join(query_pairs), ';'.join(stitle_pairs)))

trans(p_train, p_test, s_train, s_test)
trans(p_dog, p_valid, s_dog, s_valid)

