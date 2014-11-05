
p_train = '../raw_data/train.txt'
p_test = '../raw_data/test.txt'
p_dog = '../trans_data/dog.txt'
p_valid = '../trans_data/valid.txt'

def refine(p_in, p_out):
    with open(p_out, 'w') as fo:
        last_query = None
        has_known = False
        session_lines = []
        for line in open(p_in):
            if not line.strip():
                fo.write('\n')
                if has_known:
                    for l in session_lines:
                        fo.write(l)
                last_query = None
                has_known = False
                session_lines = []
            else:
                label, query = line.strip().split('\t')[:2]
                query_set = set(query.split(' '))
                if not last_query or (last_query & query_set):
                    session_lines.append(line)
                    if label != 'CLASS=UNKNOWN':
                        has_known = True
                    last_query = query_set
                else:
                    fo.write('\n')
                    if has_known:
                        for l in session_lines:
                            fo.write(l)
                    last_query = None
                    has_known = False
                    session_lines = []

refine(p_dog, '../trans_data/dog_refine.txt')
refine(p_train, '../trans_data/train_refine.txt')
                
            
