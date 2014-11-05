import random

p_train = '../raw_data/train.txt'
p_test = '../raw_data/test.txt'

p_dog = '../trans_data/dog.txt'
p_valid = '../trans_data/valid.txt'
p_label = '../trans_data/valid.label'

n_fold = 3

train_dict = {}
test_dict = {}
unknown_dict = {}

for line in open(p_train):
    if not line.strip(): continue
    try:
        label, query, title = line.strip().split('\t')
    except:
        label, query = line.strip().split('\t')
        title = '-'

    if query not in train_dict:
        train_dict[query] = {} 
    train_dict[query][label] = train_dict[query].get(label, 0) + 1
    if label.startswith('CLASS=TEST'):
        test_dict[query] = 1
    if label.startswith('CLASS=UNKNOWN'):
        unknown_dict[query] = 1

valid_dict = {}
fv2 = open('../trans_data/valid.txt', 'w')
fv3 = open('../trans_data/valid.label', 'w')
for query in train_dict:
    if query in test_dict: continue
    if query in unknown_dict: continue
    if random.randint(0, n_fold-1) == 1:
        valid_dict[query] = 1
        label = sorted(train_dict[query].items(), key=lambda d:-d[1])[0][0]
        fv2.write('%s\n' % query)
        fv3.write('%s\t%s\n' % (query, label))
fv2.close()
fv3.close()

fv1 = open('../trans_data/dog.txt', 'w')
for line in open(p_train):
    if not line.strip():
        fv1.write(line)
        continue

    try:
        label, query, title = line.strip().split('\t')
    except:
        label, query = line.strip().split('\t')
        title = '-'
    if query in test_dict: continue
    if query in train_dict:
        if query in valid_dict:
            label = 'CLASS=TEST'
            fv1.write('%s\t%s\t%s\n' % (label, query, title))
        else:
            fv1.write(line)
fv1.close()

