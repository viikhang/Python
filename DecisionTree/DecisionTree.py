import numpy as np
from collections import Counter
class Node:
    def __init__(self, feature=None, threshold = None, left = None, right = None, *, value = None):
        self.feature = feature #feature of node
        self.threshold = threshold#value that determines how we split left and right branch
        self.left = left
        self.right = right
        self.value = value

    #check if a node if a leaf node or not
    def isLeafNode(self):
        return self.value is not None

class DecisionTree:
    def __init__(self, minSampleSplit = 2, maxDept = 100, nFeatures = None):
        self.minSampleSplit = minSampleSplit
        self.maxDepth = maxDept
        self.nFeatures = nFeatures #number of features we want to consider at a node, can add randomness to avoid overfitting
        self.root = None

    def fit(self, X, y):
        #shape gives us number of samples and number of features [1] means it should be number of features
        #first check if number of features is defined, if not then
        #number of features should either be the maximum number of features allowed or the total numbers of feature from X
        self.nFeatures = X.shape[1] if not self.nFeatures else min(X.shape[1], self.nFeatures)

        self.root = self.growTree(X,y)

    def growTree(self, X, y, depth = 0):
        nSamples, nFeatures = X.shape
        nLabels = len( np.unique(y))

        #check stopping criteria
        # shouldn't keep going if we reached our max depth
        # If number of labels is just 1, no way to split
        # If number of samples < minimum sample split
        if (depth >= self.maxDepth or nLabels == 1 or nSamples < self.minSampleSplit):
            leafValue = self.mostCommonLabel(y)
            return Node(value= leafValue)

        #select a random group of features
        #number of features we have, number of features we want to select
        featidxs = np.random.choice(nFeatures, self.nFeatures, replace = False)
        #find the best split
        bestFeature , bestThreshold= self.bestSplit(X,y, featidxs)


        #create the child nodes

        leftIdx, rightIdx = self.split(X[:, bestFeature], bestThreshold) #get column with best feature
        # make X only contain values in leftIndex, while also keeping columns/features
        # y contains correct outputs
        left = self.growTree(X[leftIdx, :] , y[leftIdx], depth + 1)
        right = self.growTree(X[rightIdx, : ], y[rightIdx], depth + 1)
        return Node(bestFeature, bestThreshold, left, right)

    def bestSplit(self, X, y, featidxs):
        bestGain = -1
        splitIndex, splitThreshold = None, None

        for featidx in featidxs:
            X_column = X[:, featidx] #get all the data that has this feature, example: age -> [22,35,...]
            #TODO WHAT IF NUMBER OF THRESHOLDS IS VERY LARGE? HOW CAN WE DEAL WITH THIS
            thresholds = np.unique(X_column) #number of candidate threshold that could be split on

            #calculate information gain
            for thr in thresholds:
                gain = self.informationGain(y, X_column, thr)

                if gain > bestGain:
                    bestGain = gain
                    splitIndex = featidx
                    splitThreshold = thr

            return splitIndex, splitThreshold

    def informationGain(self, y , X_column, threshold):
        #parent entropy
        parentEntropy = self.entropy(y)
        #create children
        leftidx, rightidx = self.split(X_column, threshold)
        if len(leftidx) == 0 or len(rightidx) == 0:
            return 0
        #calculate weighted average entropy of children
        n = len(y) #total number of samples
        nL, nR = len(leftidx), len(rightidx) #number of elements in left and right children
        # calculate the entropy for left and right, when we call y[index] -> takes entries from y at only positions saved from leftidx and right idx
        entropyLeft, entropyRight = self.entropy(y[leftidx]), self.entropy(y[rightidx])
        childEntropy = (nL/n) * entropyLeft + (nR/n) * entropyRight

        #calculate the information gain
        informationGain = parentEntropy - childEntropy
        return informationGain

    def split(self, X_column, splitThreshold):
        leftIdxs = np.argwhere(X_column <= splitThreshold).flatten()
        rightIdxs = np.argwhere (X_column > splitThreshold).flatten()
        return leftIdxs, rightIdxs

    def entropy(self, y):
        hist = np.bincount(y) #get an array that tells us the number of occurrences for each element
        probs = hist / len(y) #divide each number of occurrences by the total number of values
        return -np.sum([p*np.log(p) for p in probs if p > 0]) #list comprehension

    def mostCommonLabel(self, y):
        counter = Counter(y)
        #TODO READ THIS DOCUMENTATION
        value = counter.most_common(1)[0][0] #find the most common data
        return value


    def predict(self, X):
        return np.array([self.traverseTree(x, self.root) for x in X])

    def traverseTree(self, x, node):
        if node.isLeafNode():
            return node.value
        if x[node.feature] <= node.threshold:
            return self.traverseTree(x, node.left)
        return self.traverseTree(x, node.right)