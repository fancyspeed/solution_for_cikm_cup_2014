BIN=../../tools/xgboost3/xgboost

python prepare_ensemble_cat.py ../dataset/cat_ensemble ../trans_data/cat.label pred_xgboost_cat.txt xgboost 10 pred_linear_cat.txt liblinear pred_semilda_dog.txt semilda
python prepare_ensemble_dog.py ../dataset/dog_ensemble ../trans_data/valid2.label pred_xgboost_dog.txt xgboost 10 pred_linear_dog.txt liblinear pred_semilda_dog.txt semilda
python prepare_ensemble_pig.py ../dataset/pig_ensemble ../raw_data/test.txt pred_xgboost_pig.txt xgboost 10 pred_linear_pig.txt liblinear pred_semilda_pig.txt semilda


$BIN xgboost3.conf num_round=200 num_class=10 bst:max_depth=7 data=../dataset/cat_ensemble eval[test]=../dataset/cat_ensemble
$BIN xgboost3.conf task=pred num_class=10 model_in=0200.model test:data=../dataset/dog_ensemble
mv pred.txt pred_ensemble_dog.txt
$BIN xgboost3.conf task=pred num_class=10 model_in=0200.model test:data=../dataset/pig_ensemble
mv pred.txt pred_ensemble_pig.txt

python construct_maxprob.py pred_ensemble_dog.txt ../trans_data/valid2.txt ../dataset/label_map_dog ../submit/dog_ensemble.txt
python metric_F1.py ../trans_data/valid2.label ../submit/dog_ensemble.txt 

#python construct_maxprob.py pred_ensemble_pig.txt ../raw_data/test.txt ../dataset/label_map_pig ../submit/pig_ensemble.txt
#python construct_maxprob_multi.py pred_ensemble_pig.txt ../raw_data/test.txt ../dataset/label_map_pig ../submit/pig_ensemble2.txt
