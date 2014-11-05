import sys
import numpy as np
# Import the random forest package
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor 
from sklearn.datasets import load_svmlight_file, load_svmlight_files

if len(sys.argv) < 5:
    print '<usage> p_trian p_test n_tree depth'
    exit(1)
p_train = sys.argv[1]
p_test = sys.argv[2]
n_tree = int(sys.argv[3])
depth = int(sys.argv[4])
print p_train, p_test, n_tree, depth

# How to load data?
#dtrain = np.loadtxt( dpath+'/training.csv', delimiter=',', skiprows=1, converters={32: lambda x:int(x=='s') } )
#X_train, y_train, X_test, y_test = load_svmlight_files(p_train, p_test)
X_train, y_train = load_svmlight_file(p_train)
X_train = X_train.toarray()
X_test, y_test = load_svmlight_file(p_test, n_features=X_train.shape[1])
X_test = X_test.toarray()

# Create the random forest object which will include all the parameters
# for the fit
forest = RandomForestClassifier(n_estimators=n_tree, criterion='gini', max_depth=depth, n_jobs=4)

# Fit the training data to the Survived labels and create the decision trees
forest = forest.fit(X_train, y_train)

# Take the same decision trees and run it on the test data
output = forest.predict(X_test)

with open('pred_forest.txt', 'w') as fo:
    for o in output:
        fo.write('%s\n' % o)
