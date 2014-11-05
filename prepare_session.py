
p_dog_train_feat = '../trans_data/dog.simple5'
p_dog_valid_feat = '../trans_data/valid.simple5'
p_dog_valid_id = '../trans_data/valid.txt'

p_pig_train_feat = '../trans_data/pig.simple5'
p_pig_valid_feat = '../trans_data/test.simple5'
p_pig_valid_id = '../raw_data/test.txt'

p_label_map = '../dataset/label_map_session'
p_dog_train = '../dataset/dog_train_session'
p_dog_test = '../dataset/dog_test_session'
p_pig_train = '../dataset/pig_train_session'
p_pig_test = '../dataset/pig_test_session'

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
    queries = row[1]
    titles = row[2] if len(row)>=3 else ''

    for query in queries.split(';'):
        if not query: continue
        feat_list = query.split(' ')
        for i, word in enumerate(feat_list):
            if not word: continue
            word_df[word] = word_df.get(word, 0) + 1
            #if i>=1:
            #    word = ' '.join(feat_list[i-1:i+1])
            #    word_df[word] = word_df.get(word, 0) + 1
            #word = '%s_%s' % (i, feat_list[i])
            #word_df[word] = word_df.get(word, 0) + 1
            #if i >= len(feat_list)/2:
            #    word = '%s_%s' % (i-len(feat_list), feat_list[i])
            #    word_df[word] = word_df.get(word, 0) + 1

    for title in titles.split(';'):
        if not title: continue
        feat_list = title.split(' ')
        for i, word in enumerate(feat_list):
            if not word: continue
            word = 't_' + word
            word_df[word] = word_df.get(word, 0) + 1
            #if i>=1:
            #    word = 't_' + ' '.join(feat_list[i-1:i+1])
            #    word_df[word] = word_df.get(word, 0) + 1


def prepare(p_in, p_out, isTrain):
  global cur_label
  global cur_word

  fo = open(p_out, 'w')

  for line in open(p_in):
    row = line.strip().split('\t')
    label = row[0]
    queries = row[1]
    titles = row[2] if len(row)>=3 else ''

    if isTrain:
        label = ' | '.join(sorted(label.split(' | ')))
        if label_df[label] < 50:
            label = label.split(' ')[0]
        if label not in label_map:
            label_map[label] = cur_label
            cur_label += 1

    word_tf = {}
    query_list = queries.split(';')
    for query in query_list:
        if not query: continue
        feat_list = query.split(' ')
        for i, word in enumerate(feat_list):
            if not word: continue
            if isTrain and word_df[word] >= min_word_df and word not in word_map:
                word_map[word] = cur_word
                cur_word += 1
            if word in word_map:
                word_tf[word_map[word]] = word_tf.get(word_map[word], 0) + 1./len(feat_list)*1./len(query_list)
            #if i>=1:
            #    word = ' '.join(feat_list[i-1:i+1])
            #    if isTrain and word_df[word] >= min_word_df and word not in word_map:
            #        word_map[word] = cur_word
            #        cur_word += 1
            #    if word in word_map:
            #        word_tf[word_map[word]] = word_tf.get(word_map[word], 0) + 1./len(feat_list)
            #word = '%s_%s' % (i, feat_list[i])
            #if isTrain and word_df[word] >= min_word_df and word not in word_map:
            #    word_map[word] = cur_word
            #    cur_word += 1
            #if word in word_map:
            #    word_tf[word_map[word]] = word_tf.get(word_map[word], 0) + 1./len(feat_list)
            #if i >= len(feat_list) / 2:
            #    word = '%s_%s' % (i-len(feat_list), feat_list[i])
            #    if isTrain and word_df[word] >= min_word_df and word not in word_map:
            #        word_map[word] = cur_word
            #        cur_word += 1
            #    if word in word_map:
            #        word_tf[word_map[word]] = word_tf.get(word_map[word], 0) + 1./len(feat_list)

    word_tf2 = {}
    title_list = titles.split(';')
    for title in title_list:
        if not title: continue
        feat_list = title.split(' ')
        for i, word in enumerate(feat_list):
            word = 't_' + word
            if isTrain and word_df[word] >= min_title_df and word not in word_map:
                word_map[word] = cur_word
                cur_word += 1
            if word in word_map:
                word_tf2[word_map[word]] = word_tf2.get(word_map[word], 0) + 1./len(feat_list)*1./len(title_list)
            #if i>=1:
            #    word = 't_' + ' '.join(feat_list[i-1:i+1])
            #    if isTrain and word_df[word] >= min_title_df and word not in word_map:
            #        word_map[word] = cur_word
            #        cur_word += 1
            #    if word in word_map:
            #        word_tf2[word_map[word]] = word_tf2.get(word_map[word], 0) + 1./len(feat_list)*freq/tot_freq


    if isTrain:
        label, F = (label_map[label], word_tf.items() + word_tf2.items())
        F = sorted(F, key=lambda d:d[0])
        f_str = ' '.join(['%s:%s' % (k, v) for k, v in F])
        fo.write('%s %s\n' % (label, f_str))
    else:
        label, F = 0, word_tf.items() + word_tf2.items()
        F = sorted(F, key=lambda d:d[0])
        f_str = ' '.join(['%s:%s' % (k, v) for k, v in F])
        fo.write('%s %s\n' % (label, f_str))

  if isTrain: fo.close()

  # save label map
  with open(p_label_map, 'w') as fo:
    for label in label_map:
        fo.write('%s\t%s\n' % (label, label_map[label]))


#for dog
#get_df(p_dog_train_feat)
#prepare(p_dog_train_feat, p_dog_train, True)
#for pig
get_df(p_pig_train_feat)
prepare(p_pig_train_feat, p_pig_train, True)

#prepare(p_dog_valid_feat, p_dog_test, False)
prepare(p_pig_valid_feat, p_pig_test, False)

