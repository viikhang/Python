import numpy as np

from DecisionTree import DecisionTree

class RandomForest:
    def __init__(self, numTrees = 20, criterium=None, chiSquareTerm=None, discreteData=None, continuousData=None, maxDepth=None,
                     minSampleSplit=2, nFeatures=None):
            self.numTrees = numTrees
            self.criterium = criterium  # what we use to measure impurity
            self.chiSquareTerm = chiSquareTerm  # termination value for chi square
            self.discreteData = discreteData  # list of discrete columns
            self.continuousData = continuousData  # list of continuous columns
            self.maxDepth = maxDepth  # max depth the tree should be
            self.minSampleSplit = minSampleSplit  # minimum number of samples we need to split
            self.nFeatures = nFeatures  # how many columns we should consider
            self.root = None
            self.trees = []


    # Function creates bootstrapped data set for RF
    def bootstrap(self, X, y):
        numSamples = X.shape[0]
        # adjust number of features we should consider, 0.2 20% of whole data
        subSampleSize = int(0.2 * numSamples)

        labels = y.unique()

        rowIndices = {}
        for label in labels:
            rowIndices[label] = np.where(y == label)[0]

        sampleCount = subSampleSize // len(labels)

        sample = []
        for label in labels:
            rows = rowIndices[label]
            rowPicked = np.random.choice(rows, size=sampleCount, replace=True)
            sample.extend(rowPicked)
        sample = list(sample)
        np.random.shuffle(sample)


        #rowIndices = np.random.choice(numSamples, subSampleSize, replace=True)

        # testx = X.iloc[rowIndices, :] #idk if this made a difference
        testx = X.iloc[sample]
        testy = y.iloc[sample]

        return testx, testy


    # def creates_trees_from_bootstrap_data(self, X, y):
    def fit(self, X, y):
        # creates the number of trees
        # replace number of trees
        for i in range(self.numTrees):
            print("Creating Decision tree number", i+1)
            tree = DecisionTree(criterium=self.criterium,
                                chiSquareTerm=self.chiSquareTerm,
                                discreteData=self.discreteData,
                                continuousData=self.continuousData,
                                maxDepth=self.maxDepth,
                                minSampleSplit=self.minSampleSplit,
                                nFeatures=self.nFeatures)

            testX, testY = self.bootstrap(X, y)
            tree.fit(testX, testY)
            self.trees.append(tree)

    def predict_multiple_trees(self,X):
        prediction = []
        heights = []
        for tree in self.trees:
            #gets tree predictions
            treePredict = tree.predict(X)
            prediction.append(treePredict)
            treeHeight = tree.getHeight()
            heights.append(treeHeight)
        print("Average height of trees:", np.mean(heights))
        print("Tallest Tree: ", max(heights))
        return self.get_majority_decision(prediction)

    def get_majority_decision(self, predictionarray):
        predictionarray = np.array(predictionarray)
        # Transpose so rows are samples, columns are tree predictions
        predictionarray = predictionarray.T

        majorityLabel = []
        for sample_predictions in predictionarray:
            values, counts = np.unique(sample_predictions, return_counts=True)
            majorityLabel.append(values[np.argmax(counts)])

        return majorityLabel