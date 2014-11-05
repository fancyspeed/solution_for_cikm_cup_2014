#!/usr/bin/python
# coding: utf-8
# @author: zuotaoliu@126.com
# @created: 2014-08-29
import os
import sys
import re

def do_word_index(p_in, p_out):
    label_map = {}
    cur_label = 0
    word_count = {}
    cur_idx = 0
    fo = open(p_out, 'w')
    for line in open(p_in):
        row = line.rstrip().split('\t')

        if len(row) >= 3:
            feats = row[1] + ':1;' + ';'.join(row[2].split(';')[:5])
        else:
            feats = row[1] + ':1'

        labels = row[0].split(' | ')
        cids = []
        for label in labels:
            if label not in label_map: 
                label_map[label] = cur_label
                cur_label += 1
            cids.append(str(label_map[label]))
        wc = {}
        for pair in feats.split(';'):
            if not pair: continue
            words, freq = pair.split(':')
            freq = min(1, int(freq))
            for word in words.split(' '):
                if not word: continue
                wc[word] = wc.get(word, 0) + freq
                word_count[word] = word_count.get(word, 0) + freq
        fo.write('%s\n' % (' '.join(['%s %s' % (k, v) for k, v in wc.items()]))) 
    fo.close()
        
    return word_count
        
if __name__ == "__main__":
    if len(sys.argv) < 3:
        print '<usage> inputfile outputfile'
        exit(-1)
    word_count = do_word_index(sys.argv[1], sys.argv[2])




