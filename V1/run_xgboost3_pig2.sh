#!/bin/bash
BIN=../../tools/xgboost3/xgboost

$BIN xgboost3.conf num_round=200 num_class=18 bst:max_depth=7 data=../dataset/pig_train2 eval[test]=../dataset/pig_train2
$BIN xgboost3.conf task=pred num_class=18 model_in=0200.model test:data=../dataset/pig_test2
mv pred.txt pred_xgboost.txt

python construct_maxprob.py pred_xgboost.txt ../raw_data/test.txt ../dataset/label_map ../submit/predict_xgboost.txt
python construct_maxprob_multi.py pred_xgboost.txt ../raw_data/test.txt ../dataset/label_map ../submit/predict_xgboost2.txt
