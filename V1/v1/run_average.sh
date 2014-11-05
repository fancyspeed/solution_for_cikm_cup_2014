#python averaging_methods.py pred_average.txt pred_linear.txt liblinear 0.2 pred_xgboost.txt xgboost 0.8 18
python averaging_methods.py pred_average.txt pred_xgboost.txt xgboost 0.65 18 pred_linear.txt liblinear 0.15 pred_semilda.txt semilda 0.0 pred_session2.txt xgboost 0.1 18 pred_session_label.txt sessionlabel 0.1

python construct_maxprob.py pred_average.txt ../raw_data/test.txt ../dataset/label_map ../submit/predict_average.txt
python construct_maxprob_multi.py pred_average.txt ../raw_data/test.txt ../dataset/label_map ../submit/predict_average2.txt
#python construct_maxprob_balance.py pred_average.txt ../raw_data/test.txt ../dataset/label_map ../submit/predict_average3.txt
