
label_map = {}
max_label = 0
adjust = {}
def load_label_map(p_in):
    global max_label
    for line in open(p_in):
        label, c = line.strip().split('\t')
        label_map[int(c)] = label
        max_label = max(max_label, int(c))

    for i in range(max_label+1):
        adjust[i] = 0

def get_match(p_pred, p_test, p_out):
    npred = len(open(p_pred).readlines()) / len(open(p_test).readlines())
    fo = open(p_out, 'w')
    fp = open(p_pred)
    for line in open(p_test):
        feats = line.strip()

        pred = []
        for i in range(npred):
            if i <= max_label:
                pred.append(float(fp.readline().strip())) 
            else:
                fp.readline()
        c = sorted([(k, v+adjust[k]) for k, v in enumerate(pred)], key=lambda d:-d[1])[0][0]
        label = label_map[c]
        fo.write('%s\t%s\n' % (feats, label))
    fp.close()
    fo.close()

if __name__ == '__main__':
    import sys
    if len(sys.argv) < 5:
        print '<usage> pred test label out adjust'
        exit(1)
    
    load_label_map(sys.argv[3])
    print 'max_label:', max_label
    if len(sys.argv) >= 6:
        for line in open(sys.argv[5]):
            cid, v = line.strip().split('\t')
            adjust[int(cid)] = float(v)
    get_match(sys.argv[1], sys.argv[2], sys.argv[4])
