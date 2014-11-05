
p_train = '../raw_data/train.txt'
p_dog = '../trans_data/dog.txt'
p_test = '../raw_data/test.txt'
p_valid = '../trans_data/valid.txt'

s_train = '../trans_data/train.simple2'
s_test = '../trans_data/test.simple2'
s_dog = '../trans_data/dog.simple2'
s_valid = '../trans_data/valid.simple2'

def trans(in1, in2, out1, out2):
    train_dict = {}
    test_dict = {}

    query_freq = {}
    query_titles = {}

    query_session = {}
    query_search = {}
    query_click = {}
    query_dupclick = {}

    query_session_search = {}
    query_session_click = {}
    query_session_dupclick = {}

    # for session
    session_train_query = {}
    session_test_query = {}
    session_labels = {}
    session_search = 0
    session_click = {}
    session_query_search = {}
    session_query_click = {}

    for line in open(in1):
        if not line.strip():
            #session end
            session_dupclick = 0
            for title in session_click:
                if session_click[title] > 1: session_dupclick += 1
            for query in session_train_query:
                query_session[query] = query_session.get(query, 0) + 1.
                query_session_search[query] = query_session_search.get(query, 0) + session_search
                query_session_click[query] = query_session_click.get(query, 0) + len(session_click)
                query_session_dupclick[query] = query_session_dupclick.get(query, 0) + session_dupclick
                query_search[query] = query_search.get(query, 0) + session_query_search.get(query, 0)
                query_click[query] = query_click.get(query, 0) + len(session_query_click.get(query, {}))
                session_query_dup = 0
                for title in session_query_click.get(query, {}):
                    if session_query_click[query][title] > 1: session_query_dup += 1
                query_dupclick[query] = query_dupclick.get(query, 0) + session_query_dup
            for query in session_test_query:
                query_session[query] = query_session.get(query, 0) + 1.
                query_session_search[query] = query_session_search.get(query, 0) + session_search
                query_session_click[query] = query_session_click.get(query, 0) + len(session_click)
                query_session_dupclick[query] = query_session_dupclick.get(query, 0) + session_dupclick
                query_search[query] = query_search.get(query, 0) + session_query_search.get(query, 0)
                query_click[query] = query_click.get(query, 0) + len(session_query_click.get(query, {}))
                session_query_dup = 0
                for title in session_query_click.get(query, {}):
                    if session_query_click[query][title] > 1: session_query_dup += 1
                query_dupclick[query] = query_dupclick.get(query, 0) + session_query_dup

            session_train_query = {}
            session_test_query = {}
            session_labels = {}
            session_search = 0
            session_click = {}
            session_query_search = {}
            session_query_click = {}
            continue

        try:
            label, query, title = line.strip().split('\t')
        except:
            label, query = line.strip().split('\t')
            title = '-'
        #label = ' | '.join(sorted(label.split(' | ')))

        query_freq[query] = query_freq.get(query, 0) + 1
        if title and title != '-':
            if query not in query_titles: query_titles[query] = [0., 0.]
            query_titles[query][0] += 1
            query_titles[query][1] += len(title.split(' '))
            session_click[title] = session_click.get(title, 0) + 1
            if query not in session_query_click: session_query_click[query] = {}
            session_query_click[query][title] = session_query_click[query].get(title, 0) + 1
        else:
            session_search += 1
            if query not in session_query_search: session_query_search[query] = 0
            session_query_search[query] += 1

        if label.startswith('CLASS=TEST'):
            if query not in test_dict: 
                test_dict[query] = [label, {}, {}, {}]
            session_test_query[query] = 1
        elif not label.startswith('CLASS=UNKNOWN'):
            if query not in train_dict: 
                train_dict[query] = [{}, {}, {}, {}]
            session_train_query[query] = label.replace(' ', '')


    with open(out1, 'w') as ft:
        for query in train_dict:
            stat_pairs = []
            stat_pairs.append( '%s:%s' % ('query_len', len(query.split(' '))) )
            stat_pairs.append( '%s:%s' % ('query_freq', query_freq[query]) )
            if query_titles.get(query, [0, 0])[0] >= 3:
                stat_pairs.append( '%s:%s' % ('title_len', query_titles[query][1]/query_titles[query][0]) )

            stat_pairs2 = []
            if query_session.get(query, 0) >= 5:
                stat_pairs2.append( '%s:%s' % ('query_search', query_search[query]/query_session[query]) )
                stat_pairs2.append( '%s:%s' % ('query_click', query_click[query]/query_session[query]) )
                stat_pairs2.append( '%s:%s' % ('query_dupclick', query_dupclick[query]/query_session[query]) )
                stat_pairs2.append( '%s:%s' % ('query_session_search', query_session_search[query]/query_session[query]) )
                stat_pairs2.append( '%s:%s' % ('query_session_click', query_session_click[query]/query_session[query]) )
                stat_pairs2.append( '%s:%s' % ('query_session_dupclick', query_session_dupclick[query]/query_session[query]) )

            ft.write('%s\t%s\t%s\n' % (query, ';'.join(stat_pairs), ';'.join(stat_pairs2)))

    with open(out2, 'w') as fo:
        for query in test_dict:
            stat_pairs = []
            stat_pairs.append( '%s:%s' % ('query_len', len(query.split(' '))) )
            stat_pairs.append( '%s:%s' % ('query_freq', query_freq[query]) )
            if query_titles.get(query, [0, 0])[0] >= 3:
                stat_pairs.append( '%s:%s' % ('title_len', query_titles[query][1]/query_titles[query][0]) )

            stat_pairs2 = []
            if query_session.get(query, 0) >= 5:
                stat_pairs2.append( '%s:%s' % ('query_search', query_search[query]/query_session[query]) )
                stat_pairs2.append( '%s:%s' % ('query_click', query_click[query]/query_session[query]) )
                stat_pairs2.append( '%s:%s' % ('query_dupclick', query_dupclick[query]/query_session[query]) )
                stat_pairs2.append( '%s:%s' % ('query_session_search', query_session_search[query]/query_session[query]) )
                stat_pairs2.append( '%s:%s' % ('query_session_click', query_session_click[query]/query_session[query]) )
                stat_pairs2.append( '%s:%s' % ('query_session_dupclick', query_session_dupclick[query]/query_session[query]) )

            fo.write('%s\t%s\t%s\n' % (query, ';'.join(stat_pairs), ';'.join(stat_pairs2)))

trans(p_train, p_test, s_train, s_test)
trans(p_dog, p_valid, s_dog, s_valid)

