#!/bin/sh -x
ldapath=../cpp_lda/src

train_file=../trans_data/dog.simple
test_file=../trans_data/test.simple

ldatrain_file=../dataset/train_semilda.train
ldatest_file=../dataset/test_semilda.test
ldapred_file=pred_semilda.txt

index_file=../dataset/word_index
seed_file=lda_seed_words
model_file=lda.model

num_topic=7
alpha=0.5
beta=0.05

python prepare_lda_train.py $train_file $ldatrain_file $index_file

time /Users/zuotaoliu/install/mpich2/bin/mpiexec -n 4 $ldapath/mpi_slda \
--num_topics $num_topic \
--alpha $alpha --beta $beta \
--training_data_file $ldatrain_file \
--model_file $model_file \
--word_index_file $index_file \
--compute_likelihood true \
--burn_in_iterations 50 --total_iterations 120


python prepare_lda_test.py $test_file $ldatest_file

args="--alpha ${alpha} \
      --beta ${beta} \
      --inference_data_file ${ldatest_file} \
      --inference_result_file ${ldapred_file} \
      --model_file ${model_file} \
      --burn_in_iterations 50 \
      --total_iterations 120 \
      --file_type 0
      "

time $ldapath/infer $args

python construct_semilda.py pred_semilda.txt $test_file ../raw_data/test.txt ../dataset/label_map_lda ../submit/predict_semilda.txt
