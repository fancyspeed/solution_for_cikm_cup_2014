#!/bin/sh -x
python trans_session.py
python prepare_session.py
python markov_sessoin_label.py

#python construct_semilda.py pred_semilda_dog.txt $test_file ../trans_data/valid.txt ../dataset/label_map_lda ../submit/dog_semilda.txt
#python metric_F1.py ../trans_data/valid.label ../submit/dog_semilda.txt 

#python construct_semilda.py pred_semilda_pig.txt $test_file ../raw_data/test.txt ../dataset/label_map_lda ../submit/pig_semilda.txt

