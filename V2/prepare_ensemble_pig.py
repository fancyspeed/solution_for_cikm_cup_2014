n_sample = 39013

label_map = {}
label_map2 = {}
max_label = 0
for line in open('../dataset/label_map_dog'):
    label, c = line.strip().split('\t')
    label_map[int(c)] = label
    label_map2[label] = int(c)
    max_label = max(max_label, int(c))
print 'max_label:', max_label 

weights = []
for i in xrange(n_sample):
    weights.append([0]*((max_label+1)*8))

if __name__ == '__main__':
    import sys
    if len(sys.argv) < 4:
        print '<usage> out label in1 m1 [in2 m2 ...]'
        exit(1)

    i = 3
    while i < len(sys.argv):
        in_i = sys.argv[i]
        m_i = sys.argv[i+1]
        print in_i, m_i
        if m_i == 'xgboost':
            nclass = int(sys.argv[i+2])
            fin = open(in_i)
            for isample in xrange(n_sample):
                for ipred in xrange(nclass):
                    pred = float(fin.readline().strip())
                    if ipred <= max_label:
                        weights[isample][ipred] = pred 
            fin.close()
            i += 3
        elif m_i == 'liblinear':
            fin = open(in_i)
            fin.readline()
            for isample in xrange(n_sample):
                preds = [float(v) for v in fin.readline().strip().split(' ')[1:]] 
                for ipred, pred in enumerate(preds):
                    weights[isample][max_label+1+ipred] = pred
            i += 2
        elif m_i == 'semilda':
            lda_map = {}
            for line in open('../dataset/label_map_lda'):
                label, c = line.strip().split('\t')
                lda_map[int(c)] = label
            feat_map = {}
            fin = open('../trans_data/test.simple1')
            for line in open(in_i):
                preds = [float(v) for v in line.strip().split(' ')] 
                tot = sum(preds) + 0.001
                preds = [v/tot for v in preds]
                feats = fin.readline().strip().split('\t')[1]
                feat_map[feats] = preds
            fin.close()
            fin = open('../raw_data/test.txt')
            for isample in xrange(n_sample):
                feats = fin.readline().strip()
                preds = feat_map[feats]
                for ipred, pred in enumerate(preds):
                    ipred2 = label_map2[lda_map[ipred]]
                    weights[isample][(max_label+1)*2+ipred2] = pred / tot
            fin.close()
            i += 2
        elif m_i == 'sessionlabel':
            fin = open(in_i)
            for isample in xrange(n_sample):
              try:
                pairs = [pair.split(':') for pair in fin.readline().strip().split(' || ')]
                if pairs and pairs[0] and pairs[0][0]:
                  tot = sum([float(v[1]) for v in pairs])
                  if tot > 0:
                    for pair in pairs:
                        label, v = pair[0], float(pair[1])
                        label = ' | '.join(sorted(label.split(' | ')))
                        if label not in label_map2: label = label.split(' | ')[0]
                        c = label_map2[label]
                        weights[isample][(max_label+1)*3+c] = v / tot
              except:
                print pairs
                exit(1)
            i += 2


    with open(sys.argv[1], 'w') as fo:
        idx = 0
        for line in open(sys.argv[2]):
            arr = line.strip().split('\t')
            if len(arr) >= 2:
                label = arr[1] 
                label = ' | '.join(sorted(label.split(' | ')))
                if label not in label_map2: label = label.split(' | ')[0]
                label = label_map2[label]
            else:
                label = 0
            fo.write('%s %s\n' % (label, ' '.join(['%s:%s' % (i+1, pred) for i, pred in enumerate(weights[idx])])))
            idx += 1


