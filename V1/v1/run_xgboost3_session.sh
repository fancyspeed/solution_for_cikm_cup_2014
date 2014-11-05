
BIN=../../tools/xgboost3/xgboost

#$BIN xgboost3.conf num_round=90 num_class=18 bst:max_depth=7 data=../dataset/pig_train_session eval[test]=../dataset/pig_train_session
#$BIN ../boost/xgboost3.conf task=pred num_class=18 model_in=0090.model test:data=../dataset/pig_test_session
#mv pred.txt pred_session.txt
#python construct_session_prob.py pred_session.txt ../trans_data/test.simple5 ../raw_data/test.txt ../dataset/label_map_session pred_session2.txt
python construct_maxprob.py pred_session2.txt ../raw_data/test.txt ../dataset/label_map_session ../submit/predict_session.txt
