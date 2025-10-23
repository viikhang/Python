import numpy as np
from sklearn.model_selection import train_test_split
from sklearn import datasets
import matplotlib.pyplot as plt
from LogisticRegression import LogisticRegression


breastCancerDataSet = datasets.load_breast_cancer()
X, y = breastCancerDataSet.data, breastCancerDataSet.target
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=1234)

classifier = LogisticRegression(learningRate = 0.01)
classifier.fit(X_train, y_train)

yPrediction = classifier.predict(X_test)

def accuracy(y_Pred, yTest):
    return np.sum(y_Pred == yTest) / len(yTest)

acc = accuracy(yPrediction, y_test)
print(acc)