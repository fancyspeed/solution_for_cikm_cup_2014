
label_map = {}
label_map2 = {}
max_label = 0
adjust = {}
def load_label_map(p_in):
    global max_label
    for line in open(p_in):
        label, c = line.strip().split('\t')
        label_map[int(c)] = label
        label_map2[label] = int(c)
        max_label = max(max_label, int(c))
    print label_map
    print label_map2

    for c in range(max_label+1):
        adjust[c] = 0.

truth_dict = {}
def load_truth(p_truth):
    tot = 0.
    for line in open(p_truth):
        label = line.strip().split('\t')[1]
        label = ' | '.join(sorted(label.split(' | ')))
        if label not in label_map: label = label.split(' | ')[0]
        c = label_map2[label]
        truth_dict[c] = truth_dict.get(c, 0) + 1
        tot += 1.
    for c in range(max_label+1):
        truth_dict[c] = truth_dict.get(c, 0) / tot
    print truth_dict

def learn(p_pred, npred):
    i = 0
    preds = []
    pred = []
    for line in open(p_pred):
        j = i % npred
        if j <= max_label:
            pred.append(float(line.strip()))
        if j == npred-1:
            preds.append(pred)
            pred = []
        i += 1
    ite = 0
    while ite < 20:
        cids = {}
        tot = len(preds)
        for pred in preds:
            c = sorted([(k, v+adjust[k]) for (k, v) in enumerate(pred)], key=lambda d:-d[1])[0][0]
            cids[c] = cids.get(c, 0) + 1./tot
        for c in cids:
            if cids[c] < truth_dict[c] * 0.8: adjust[c] += 0.005
            elif cids[c] < truth_dict[c] * 0.2: adjust[c] += 0.015
            elif cids[c] > truth_dict[c] * 1.2: adjust[c] -= 0.005
            elif cids[c] > truth_dict[c] * 5: adjust[c] -= 0.015
        ite += 1


def get_match(p_pred, p_test, p_out):
    npred = len(open(p_pred).readlines()) / len(open(p_test).readlines())

    learn(p_pred, npred)

    fo = open(p_out, 'w')
    fp = open(p_pred)
    for line in open(p_test):
        feats = line.strip()

        pred = []
        for c in range(npred):
            if c <= max_label:
                pred.append(float(fp.readline().strip())) 
            else:
                fp.readline()
        sort_list = sorted([(c, v+adjust[c]) for c, v in enumerate(pred)], key=lambda d:-d[1])
        c = sort_list[0][0]
        label = label_map[c]
        if sort_list[1][1] > 0.45: 
            label = label + ' | ' + label_map[sort_list[1][0]]  
        label = ' | '.join(label.split(' | ')[:2])
        fo.write('%s\t%s\n' % (feats, label))
    fp.close()
    fo.close()

if __name__ == '__main__':
    import sys
    if len(sys.argv) < 5:
        print '<usage> pred test label out adjust'
        exit(1)
    
    load_label_map(sys.argv[3])
    load_truth('../trans_data/valid.label')
    print 'max_label:', max_label
    if len(sys.argv) >= 6:
        for line in open(sys.argv[5]):
            cid, v = line.strip().split('\t')
            adjust[int(cid)] = float(v)
    get_match(sys.argv[1], sys.argv[2], sys.argv[4])

