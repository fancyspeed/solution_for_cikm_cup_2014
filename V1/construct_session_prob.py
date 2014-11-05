
label_map = {}
max_label = 0
def load_label_map(p_in):
    global max_label
    for line in open(p_in):
        label, c = line.strip().split('\t')
        label_map[int(c)] = label
        max_label = max(max_label, int(c))


def get_match(p_pred, p_session, p_test, p_out):
    npred = len(open(p_pred).readlines()) / len(open(p_session).readlines())
    query_dict = {} 
    query_num = {}
    for line in open(p_test):
        query = line.strip()
        query_dict[query] = [0]*npred     
        query_num[query] = 0

    fp = open(p_pred)
    for line in open(p_session):
        query_list = line.strip().split('\t')[1].split(';')

        pred = []
        for i in range(npred):
            if i <= max_label:
                pred.append(float(fp.readline().strip())) 
            else:
                fp.readline()
        for query in query_list:
            if query in query_dict: 
                for i, v in enumerate(pred):
                    query_dict[query][i] += v
                query_num[query] += 1
    fp.close()
    print 'query_dict', len(query_dict)

    not_in_test = 0
    fo = open(p_out, 'w')
    for line in open(p_test):
        query = line.strip()
        #c = sorted([(k, v+adjust[k]) for k, v in enumerate(pred)], key=lambda d:-d[1])[0][0]
        #label = label_map[c]
        if query_num[query] > 0:
            for i in range(npred):
                fo.write('%s\n' % (query_dict[query][i]/query_num[query]))
        else:
            for i in range(npred):
                fo.write('0\n')
            not_in_test += 1
    fo.close()
    print 'not in session:', not_in_test

if __name__ == '__main__':
    import sys
    if len(sys.argv) < 6:
        print '<usage> pred session testid label out'
        exit(1)
    
    load_label_map(sys.argv[4])
    print 'max_label:', max_label

    get_match(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[5])
