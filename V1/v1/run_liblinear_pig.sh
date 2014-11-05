#!/bin/bash
TRAIN_BIN=../../tools/liblinear/train
TEST_BIN=../../tools/liblinear/predict

#$TRAIN_BIN -s 6 -c 10 -e 0.001 -w0 0.5 -w5 0.6 ../dataset/pig_train pig.model
$TRAIN_BIN -s 6 -c 10 -e 0.001 ../dataset/pig_train pig.model

$TEST_BIN -b 1 ../dataset/pig_test pig.model pred_linear.txt 
python construct_liblinear_b1.py pred_linear.txt ../raw_data/test.txt ../dataset/label_map ../submit/predict_linear.txt

#$TEST_BIN ../dataset/pig_test pig.model pred_linear.txt 
#python construct_maxlabel.py pred_linear.txt ../raw_data/test.txt ../dataset/label_map ../submit/predict_linear.txt


