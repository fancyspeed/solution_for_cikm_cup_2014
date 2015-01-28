
sh -x run_prepare.sh

sh -x run_liblinear_dog.sh
sh -x run_liblinear_pig.sh
sh -x run_xgboost3_dog.sh
sh -x run_xgboost3_pig.sh

sh -x run_ensemble.sh
