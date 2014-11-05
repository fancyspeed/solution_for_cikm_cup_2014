p_simple = '../trans_data/train.simple'
p_raw_train = '../dataset/pig_train'
p_svm_train = '../dataset/svm_train'

label_map = {}
cur_label = 0
for line in open('../dataset/label_map'):
    label = line.split('\t')[0]
    if label.count(' | ') == 0:
        if label not in label_map:
                label_map[label] = cur_label
                cur_label += 1
                print label
with open('../dataset/label_map_svm', 'w') as fo:
    for label in label_map:
        fo.write('%s\t%s\n' % (label, label_map[label]))

fout = []
for c in range(7):
    fout.append( open('%s%s' % (p_svm_train, c), 'w') )

with open(p_simple) as fin:
    for line in open(p_raw_train):
        arr = line.split(' ')
        labels = fin.readline().split('\t')[0].split(' | ')
        c_dict = {label_map[label]:1 for label in labels}
        for c in range(7):
            if c in c_dict:
                fout[c].write('%s %s' % (1, ' '.join(arr[1:])))
            else:
                fout[c].write('%s %s' % (0, ' '.join(arr[1:])))
                
            
for c in range(7):
    fout[c].close()
