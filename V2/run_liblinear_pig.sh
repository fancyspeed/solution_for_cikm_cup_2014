#!/bin/bash
TRAIN_BIN=../../tools/liblinear/train
TEST_BIN=../../tools/liblinear/predict

$TRAIN_BIN -s 6 -c 10 -e 0.001 ../dataset/pig_train pig.model
$TEST_BIN -b 1 ../dataset/pig_test pig.model pred_linear_pig.txt 

python construct_liblinear_b1.py pred_linear_pig.txt ../raw_data/test.txt ../dataset/label_map_pig ../submit/pig_linear.txt



