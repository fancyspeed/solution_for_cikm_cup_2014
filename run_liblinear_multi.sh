#!/bin/bash
TRAIN_BIN=../../tools/liblinear/train
TEST_BIN=../../tools/liblinear/predict

for ((i=0; i<=6; i++)); do
  $TRAIN_BIN -s 6 -c 10 -e 0.001 ../dataset/svm_train${i} svm.model
  $TEST_BIN -b 1 ../dataset/pig_test svm.model pred_linear_${i}.txt 
done

#python construct_liblinear_b1.py pred_linear.txt ../raw_data/test.txt ../dataset/label_map ../submit/predict_linear.txt

#$TEST_BIN ../dataset/pig_test pig.model pred_linear.txt 
#python construct_maxlabel.py pred_linear.txt ../raw_data/test.txt ../dataset/label_map ../submit/predict_linear.txt


