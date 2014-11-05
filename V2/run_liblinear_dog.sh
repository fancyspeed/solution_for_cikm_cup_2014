#!/bin/bash
TRAIN_BIN=../../tools/liblinear/train
TEST_BIN=../../tools/liblinear/predict

$TRAIN_BIN -s 6 -c 10 -e 0.001 ../dataset/dog_train dog.model
$TEST_BIN -b 1 ../dataset/cat_test dog.model pred_linear_cat.txt 
$TEST_BIN -b 1 ../dataset/dog_test dog.model pred_linear_dog.txt 

python construct_liblinear_b1.py pred_linear_dog.txt ../trans_data/valid2.txt ../dataset/label_map_dog ../submit/dog_linear.txt
python metric_F1.py ../trans_data/valid2.label ../submit/dog_linear.txt 



