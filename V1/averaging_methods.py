n_sample = 39013

label_map = {}
label_map2 = {}
max_label = 0
for line in open('../dataset/label_map'):
    label, c = line.strip().split('\t')
    label_map[int(c)] = label
    label_map2[label] = int(c)
    max_label = max(max_label, int(c))
print 'max_label:', max_label 

weights = []
for i in xrange(n_sample):
    weights.append([0]*(max_label+1))

if __name__ == '__main__':
    import sys
    if len(sys.argv) < 4:
        print '<usage> out in1 m1 w1 [in2 m2 w2 ...]'
        exit(1)

    i = 2
    while i < len(sys.argv):
        in_i = sys.argv[i]
        m_i = sys.argv[i+1]
        w_i = float(sys.argv[i+2])
        print in_i, m_i, w_i
        if m_i == 'xgboost':
            nclass = int(sys.argv[i+3])
            fin = open(in_i)
            for isample in xrange(n_sample):
                for ipred in xrange(nclass):
                    pred = float(fin.readline().strip())
                    if ipred <= max_label:
                        weights[isample][ipred] += pred * w_i
            fin.close()
            i += 4
        elif m_i == 'liblinear':
            fin = open(in_i)
            fin.readline()
            for isample in xrange(n_sample):
                preds = [float(v) for v in fin.readline().strip().split(' ')[1:]] 
                for ipred, pred in enumerate(preds):
                    weights[isample][ipred] += pred * w_i
            i += 3
        elif m_i == 'semilda':
            lda_map = {}
            for line in open('../dataset/label_map_lda'):
                label, c = line.strip().split('\t')
                lda_map[int(c)] = label
            feat_map = {}
            fin = open('../trans_data/test.simple')
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
                    weights[isample][ipred2] += pred / tot * w_i
            fin.close()
            i += 3
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
                        weights[isample][c] += v / tot * w_i
              except:
                print pairs
                exit(1)
            i += 3


    with open(sys.argv[1], 'w') as fo:
        for preds in weights:
            for pred in preds:
                fo.write('%s\n' % pred)
            #label = sorted([(i, v) for i, v in enumerate(preds)], key=lambda d:-d[1])[0][0]
            #fo.write('%s\n' % label)


