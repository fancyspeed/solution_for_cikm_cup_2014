
label_map = {}
max_label = 0
def load_label_map(p_in):
    global max_label
    for line in open(p_in):
        label, c = line.strip().split('\t')
        label_map[int(c)] = label
        max_label = max(max_label, int(c))

def get_match(p_pred, p_test_simple, p_test, p_out):
    feat_map = {}
    fl = open(p_test_simple)
    fin = open(p_pred)
    for line in fin: 
        pred = [float(v) for v in line.strip().split(' ')]
        tot = sum(pred) + 0.001
        pred = [v/tot for v in pred]
        c = sorted([(k, v) for k, v in enumerate(pred)], key=lambda d:-d[1])[0][0]
        label = label_map[c]
        feats = fl.readline().strip().split('\t')[1]
        feat_map[feats] = label
    fin.close()
    fl.close()
    fo = open(p_out, 'w')
    for line in open(p_test):
        feats = line.strip()
        fo.write('%s\t%s\n' % (feats, feat_map[feats]))
    fo.close()

if __name__ == '__main__':
    import sys
    if len(sys.argv) != 6:
        print '<usage> pred test.simple test label out'
        exit(1)
    
    load_label_map(sys.argv[4])
    print 'max_label:', max_label
    get_match(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[5])
