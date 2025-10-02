from DecisionTree import DecisionTree
from collections import Counter
import numpy as np

class RandomForest:
    def __init__(self, numberTrees = 10, maxDepth = 10, minSamplesSplit = 2, nFeatures = None):
        self.numberTrees = numberTrees
        self.maxDepth = maxDepth
        self.minSamplesSplit = minSamplesSplit
        self.nFeatures = nFeatures
        self.trees = []
    def fit(self, X, y):
        self.trees = []
        for _ in range(self.numberTrees):
            tree = DecisionTree(maxDept=self.maxDepth, minSampleSplit= self.minSamplesSplit, nFeatures= self.nFeatures)
            XSample, ySample = self.bootStrapSamples(X,y)

            tree.fit(XSample, ySample)
            self.trees.append(tree)

    def bootStrapSamples(self, X, y):
        nSamples = X.shape[0] #number of features
        index = np.random.choice(nSamples, nSamples, replace = True)
        return X[index], y[index]

    def mostCommonLabel(self, y):
        counter = Counter(y)
        mostCommon = counter.most_common(1)[0][0]
        return mostCommon

    def predict(self, X):
        predictions =  np.array([tree.preduct(X) for tree in self.trees])
        #this will give us a list of lists
        #need to then pick a majority for each list
        treePredictions = np.swapaxes(predictions, 0, 1)
        return np.array([self.mostCommonLabel(pred) for pred in treePredictions])