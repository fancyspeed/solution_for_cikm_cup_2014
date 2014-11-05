
label_map = {}
max_label = 0
def load_label_map(p_in):
    global max_label
    for line in open(p_in):
        label, c = line.strip().split('\t')
        label_map[int(c)] = label
        max_label = max(max_label, int(c))

def get_match(p_pred, p_test, p_out):
    fo = open(p_out, 'w')
    fl = open(p_test)
    fin = open(p_pred)
    fin.readline()
    for line in fin: 
        c = int(line.split(' ')[0])
        #c = max(0, min(max_label, int(float(line.strip())+0.5)))
        label = label_map[c]
        feats = fl.readline().strip()
        fo.write('%s\t%s\n' % (feats, label))
    fin.close()
    fl.close()
    fo.close()

if __name__ == '__main__':
    import sys
    if len(sys.argv) != 5:
        print '<usage> pred test label out'
        exit(1)
    
    load_label_map(sys.argv[3])
    print 'max_label:', max_label
    get_match(sys.argv[1], sys.argv[2], sys.argv[4])
