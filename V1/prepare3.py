
p_dog_train_feat = '../trans_data/dog.simple'
p_dog_valid_feat = '../trans_data/valid.simple'
p_dog_valid_id = '../trans_data/valid.txt'

p_pig_train_feat = '../trans_data/train.simple'
p_pig_valid_feat = '../trans_data/test.simple'
p_pig_valid_id = '../raw_data/test.txt'

p_label_map = '../dataset/label_map'
p_dog_train = '../dataset/dog_train'
p_dog_test = '../dataset/dog_test'
p_pig_train = '../dataset/pig_train'
p_pig_test = '../dataset/pig_test'

min_word_df = 5
min_title_df = 10

label_map = {}
cur_label = 0
word_map = {}
cur_word = 1 

pig_train = []
test_dict = {}
pig_test = [] 

label_df = {}
word_df = {}

def get_df(p_in):
  for line in open(p_in):
    row = line.strip().split('\t')
    label = row[0]
    label = ' | '.join(sorted(label.split(' | ')))
    label_df[label] = label_df.get(label, 0) + 1
    query = row[1]
    titles = row[2] if len(row)>=3 else ''
    session_queries = row[5] if len(row)>=6 else ''
    session_titles = row[6] if len(row)>=7 else ''

    feat_list = query.split(' ')
    for i, word in enumerate(feat_list):
        #if not word: continue
        word_df[word] = word_df.get(word, 0) + 1
        if i>=1:
            word = ' '.join(feat_list[i-1:i+1])
            word_df[word] = word_df.get(word, 0) + 1
            word = '%s_%s' % (i-1, ' '.join(feat_list[i-1:i+1]))
            word_df[word] = word_df.get(word, 0) + 1
        word = '%s_%s' % (i, feat_list[i])
        word_df[word] = word_df.get(word, 0) + 1
        if i >= len(feat_list)/2:
            word = '%s_%s' % (i-len(feat_list), feat_list[i])
            word_df[word] = word_df.get(word, 0) + 1

    for pair in titles.split(';'):
        if not pair: continue
        title, freq = pair.split(':')
        feat_list = title.split(' ')
        for i, word in enumerate(feat_list):
            #if not word: continue
            word = 't_' + word
            word_df[word] = word_df.get(word, 0) + 1
            if i>=1:
                word = 't_' + ' '.join(feat_list[i-1:i+1])
                word_df[word] = word_df.get(word, 0) + 1

    for pair in session_queries.split(';'):
        if not pair: continue
        title, freq = pair.split(':')
        feat_list = title.split(' ')
        for i, word in enumerate(feat_list):
            #if not word: continue
            word = 'sq_' + word
            word_df[word] = word_df.get(word, 0) + 1
    for pair in session_titles.split(';'):
        if not pair: continue
        title, freq = pair.split(':')
        feat_list = title.split(' ')
        for i, word in enumerate(feat_list):
            #if not word: continue
            word = 'st_' + word
            word_df[word] = word_df.get(word, 0) + 1

def prepare(p_in, p_out, isTrain, p_in2):
  global cur_label
  global cur_word

  if isTrain: fo = open(p_out, 'w')
  fin2 = open(p_in2)

  for line in open(p_in):
    row = line.strip().split('\t')
    label = row[0]
    query = row[1]
    titles = row[2] if len(row)>=3 else ''
    labels = row[3] if len(row)>=4 else ''
    session_queries = row[5] if len(row)>=6 else ''
    session_titles = row[6] if len(row)>=7 else ''

    row2 = fin2.readline().split('\t')
    if row2[0] == query:
        stats = row2[1]
        stats2 = row2[2].strip()
    else:
        print 'query mismatch'
        exit(1)

    if isTrain:
        label = ' | '.join(sorted(label.split(' | ')))
        if label_df[label] < 200:
            label = label.split(' ')[0]
        if label not in label_map:
            label_map[label] = cur_label
            cur_label += 1

    feat_list = query.split(' ')
    word_tf = {}
    for i, word in enumerate(feat_list):
        if isTrain and word_df[word] >= min_word_df and word not in word_map:
            word_map[word] = cur_word
            cur_word += 1
        if word in word_map:
            word_tf[word_map[word]] = word_tf.get(word_map[word], 0) + 1./len(feat_list)
        if i>=1:
            word = ' '.join(feat_list[i-1:i+1])
            if isTrain and word_df[word] >= min_word_df and word not in word_map:
                word_map[word] = cur_word
                cur_word += 1
            if word in word_map:
                word_tf[word_map[word]] = word_tf.get(word_map[word], 0) + 1./len(feat_list)
            word = '%s_%s' % (i-1, ' '.join(feat_list[i-1:i+1]))
            if isTrain and word_df[word] >= min_word_df and word not in word_map:
                word_map[word] = cur_word
                cur_word += 1
            if word in word_map:
                word_tf[word_map[word]] = word_tf.get(word_map[word], 0) + 1./len(feat_list)
        word = '%s_%s' % (i, feat_list[i])
        if isTrain and word_df[word] >= min_word_df and word not in word_map:
            word_map[word] = cur_word
            cur_word += 1
        if word in word_map:
            word_tf[word_map[word]] = word_tf.get(word_map[word], 0) + 1./len(feat_list)
        if i >= len(feat_list) / 2:
            word = '%s_%s' % (i-len(feat_list), feat_list[i])
            if isTrain and word_df[word] >= min_word_df and word not in word_map:
                word_map[word] = cur_word
                cur_word += 1
            if word in word_map:
                word_tf[word_map[word]] = word_tf.get(word_map[word], 0) + 1./len(feat_list)

    tot_freq = 0
    for pair in titles.split(';'):
        if not pair: continue
        title, freq = pair.split(':')
        tot_freq += float(freq)
    word_tf2 = {}
    for pair in titles.split(';'):
        if not pair: continue
        title, freq = pair.split(':')
        freq = float(freq)
        feat_list = title.split(' ')
        for i, word in enumerate(feat_list):
            word = 't_' + word
            if isTrain and word_df[word] >= min_title_df and word not in word_map:
                word_map[word] = cur_word
                cur_word += 1
            if word in word_map:
                word_tf2[word_map[word]] = word_tf2.get(word_map[word], 0) + 1./len(feat_list)*freq/tot_freq
            if i>=1:
                word = 't_' + ' '.join(feat_list[i-1:i+1])
                if isTrain and word_df[word] >= min_title_df and word not in word_map:
                    word_map[word] = cur_word
                    cur_word += 1
                if word in word_map:
                    word_tf2[word_map[word]] = word_tf2.get(word_map[word], 0) + 1./len(feat_list)*freq/tot_freq

    tot_freq = 0
    for pair in session_queries.split(';'):
        if not pair: continue
        title, freq = pair.split(':')
        tot_freq += float(freq)
    for pair in session_queries.split(';'):
        if not pair: continue
        title, freq = pair.split(':')
        freq = float(freq)
        feat_list = title.split(' ')
        for i, word in enumerate(feat_list):
            word = 'sq_' + word
            if isTrain and word_df[word] >= min_title_df and word not in word_map:
                word_map[word] = cur_word
                cur_word += 1
            if word in word_map:
                word_tf2[word_map[word]] = word_tf2.get(word_map[word], 0) + 1./len(feat_list)*freq/tot_freq

    tot_freq = 0
    for pair in session_titles.split(';'):
        if not pair: continue
        title, freq = pair.split(':')
        tot_freq += float(freq)
    for pair in session_titles.split(';'):
        if not pair: continue
        title, freq = pair.split(':')
        freq = float(freq)
        feat_list = title.split(' ')
        for i, word in enumerate(feat_list):
            word = 'st_' + word
            if isTrain and word_df[word] >= min_title_df and word not in word_map:
                word_map[word] = cur_word
                cur_word += 1
            if word in word_map:
                word_tf2[word_map[word]] = word_tf2.get(word_map[word], 0) + 1./len(feat_list)*freq/tot_freq

    for pair in labels.split(';'):
        if not pair: continue
        word, freq = pair.split(':')
        freq = float(freq)
        if isTrain and word not in word_map:
            word_map[word] = cur_word
            cur_word += 1
        if word in word_map:
            word_tf2[word_map[word]] = word_tf2.get(word_map[word], 0) + freq

    for pair in stats.split(';') + stats2.split(';'):
        if not pair: continue
        word, freq = pair.split(':')
        freq = float(freq)
        if isTrain and word not in word_map:
            word_map[word] = cur_word
            cur_word += 1
        if word in word_map:
            word_tf2[word_map[word]] = word_tf2.get(word_map[word], 0) + freq

    if isTrain:
        label, F = (label_map[label], word_tf.items() + word_tf2.items())
        F = sorted(F, key=lambda d:d[0])
        f_str = ' '.join(['%s:%s' % (k, v) for k, v in F])
        fo.write('%s %s\n' % (label, f_str))
    else:
        test_dict[query] = word_tf.items() + word_tf2.items()

  if isTrain: fo.close()
  fin2.close()

  # save label map
  with open(p_label_map, 'w') as fo:
    for label in label_map:
        fo.write('%s\t%s\n' % (label, label_map[label]))


def save_test(p_in, p_out):
  with open(p_out, 'w') as fo:
    for line in open(p_in):
        query = line.strip()
        F = test_dict[query]
        F = sorted(F, key=lambda d:d[0])
        f_str = ' '.join(['%s:%s' % (k, v) for k, v in F])
        fo.write('%s %s\n' % (0, f_str))
        
#for dog
#get_df(p_dog_train_feat)
#prepare(p_dog_train_feat, p_dog_train, True, '../trans_data/dog.simple2')
#for pig
get_df(p_pig_train_feat)
prepare(p_pig_train_feat, p_pig_train, True, '../trans_data/train.simple2')

#prepare(p_dog_valid_feat, '', False, '../trans_data/valid.simple2')
prepare(p_pig_valid_feat, '', False, '../trans_data/test.simple2')
#save_test(p_dog_valid_id, p_dog_test)
save_test(p_pig_valid_id, p_pig_test)

