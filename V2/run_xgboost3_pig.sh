#!/bin/bash
BIN=../../tools/xgboost3/xgboost

$BIN xgboost3.conf num_round=200 num_class=10 bst:max_depth=7 data=../dataset/pig_train eval[test]=../dataset/pig_train
$BIN xgboost3.conf task=pred num_class=10 model_in=0200.model test:data=../dataset/pig_test
mv pred.txt pred_xgboost_pig.txt

python construct_maxprob.py pred_xgboost_pig.txt ../raw_data/test.txt ../dataset/label_map_pig ../submit/pig_xgboost.txt
python construct_maxprob_multi.py pred_xgboost_pig.txt ../raw_data/test.txt ../dataset/label_map_pig ../submit/pig_xgboost2.txt
