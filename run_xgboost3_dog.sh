
BIN=../../tools/xgboost3/xgboost

$BIN ../boost/xgboost3.conf num_round=120 num_class=18 bst:max_depth=7 data=../dataset/dog_train eval[test]=../dataset/dog_train

$BIN ../boost/xgboost3.conf task=pred num_class=18 model_in=0120.model test:data=../dataset/dog_test
#cp pred.txt pred5.txt
python ../boost/construct_maxprob.py pred.txt ../trans_data/valid.txt ../dataset/label_map ../submit/dog.txt
python ../evaluate/metric_F1.py ../trans_data/valid.label ../submit/dog.txt 
python ../evaluate/metric_confusion.py ../trans_data/valid.label ../submit/dog.txt
#python ../evaluate/construct_maxprob_multi.py pred.txt ../trans_data/valid.txt ../dataset/label_map ../submit/dog.txt
#python ../evaluate/metric_F1.py ../trans_data/valid.label ../submit/dog.txt 

$BIN ../boost/xgboost3.conf task=pred num_class=18 model_in=0120.model test:data=../dataset/pig_test
#cp pred.txt pred5_2.txt
python ../boost/construct_maxprob.py pred.txt ../raw_data/test.txt ../dataset/label_map ../submit/pig.txt
python ../evaluate/construct_maxprob_multi.py pred.txt ../raw_data/test.txt ../dataset/label_map ../submit/pig2.txt
