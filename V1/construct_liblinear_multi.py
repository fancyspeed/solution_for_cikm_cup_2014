
label_map = {}
max_label = 0
def load_label_map(p_in):
    global max_label
    for line in open(p_in):
        label, c = line.strip().split('\t')
        label_map[int(c)] = label
        max_label = max(max_label, int(c))

def get_match(p_pred, p_test, p_out):
    fin = []
    for i in range(7):
        fin.append( open('%s_%s.txt' % (p_pred, i)) )
        fin[i].readline()
    fo = open(p_out, 'w')

    for line in open(p_test):
        feats = line.strip()

        preds = []
        for i in range(7):
            #preds.append( (label_map[i], int(fin[i].readline().split(' ')[0]))) 
            preds.append( (label_map[i], float(fin[i].readline().strip().split(' ')[2]))) 
        labels = sorted(preds, key=lambda d:-d[1])
        if labels[1][1] > 0.5:
            label = labels[0][0] + ' | ' + labels[1][0]
        else:
            label = labels[0][0]
        fo.write('%s\t%s\n' % (feats, label))
    fo.close()
    for i in range(7):
        fin[i].close()

if __name__ == '__main__':
    import sys
    if len(sys.argv) != 5:
        print '<usage> pred test label out'
        exit(1)
    
    load_label_map(sys.argv[3])
    print 'max_label:', max_label

    get_match(sys.argv[1], sys.argv[2], sys.argv[4])
