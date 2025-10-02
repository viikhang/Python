from sklearn import datasets
from sklearn.model_selection import train_test_split
import numpy as np
from DecisionTree import DecisionTree

data = datasets.load_breast_cancer()
#Think of X as a 2D array, first [i] tells the patient number
# [i][j] gives us a specific feature of a patient
# y is simply a 1D array, it contains the class values, ie Yes or No
X, y = data.data, data.target
#split data set into training set, and testing set
X_train, X_test, y_train, y_test = train_test_split(X,y, test_size = 0.2, random_state=1234)

clf = DecisionTree()
clf.fit(X_train, y_train)
predictions = clf.predict(X_test)

def accuracy(y_test, y_predictions):
    return np.sum(y_test == y_predictions) / len(y_test)

acc = accuracy(y_test, predictions)
print(acc)