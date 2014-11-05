python forest.py ../dataset/pig_train ../dataset/pig_test 20 5

python construct_maxlabel.py pred_forest.txt ../raw_data/test.txt ../dataset/label_map ../submit/predict_forest.txt 
