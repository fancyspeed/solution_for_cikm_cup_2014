BIN=../../tools/xgboost3/xgboost

$BIN xgboost3.conf num_round=200 num_class=10 bst:max_depth=7 data=../dataset/dog_train eval[test]=../dataset/dog_train
$BIN xgboost3.conf task=pred num_class=10 model_in=0200.model test:data=../dataset/cat_test
mv pred.txt pred_xgboost_cat.txt
$BIN xgboost3.conf task=pred num_class=10 model_in=0200.model test:data=../dataset/dog_test
mv pred.txt pred_xgboost_dog.txt

python construct_maxprob.py pred_xgboost_dog.txt ../trans_data/valid2.txt ../dataset/label_map_dog ../submit/dog_xgboost.txt
python metric_F1.py ../trans_data/valid2.label ../submit/dog_xgboost.txt 
python construct_maxprob_multi.py pred_xgboost_dog.txt ../trans_data/valid2.txt ../dataset/label_map_dog ../submit/dog_xgboost2.txt
python metric_F1.py ../trans_data/valid2.label ../submit/dog_xgboost2.txt 

