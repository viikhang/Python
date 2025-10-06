"""
Decision Tree Class, handles creating a decision tree based on a given data set
"""
import numpy as np

from Node import Node


class DecisionTree:
    def __init__(self, criterium=None, chiSquareTerm=None, discreteData=None, continuousData=None, maxDepth=None,
                 minSampleSplit=2, nFeatures=None, classWeight = None):
        self.criterium = criterium  # what we use to measure impurity
        self.chiSquareTerm = chiSquareTerm  # termination value for chi square
        self.discreteData = discreteData  # list of discrete columns
        self.continuousData = continuousData  # list of continuous columns
        self.maxDepth = maxDepth  # max depth the tree should be
        self.minSampleSplit = minSampleSplit  # minimum number of samples we need to split
        self.nFeatures = nFeatures  # how many columns we should consider
        self.root = None  # Root node
        self.classWeight = None

    def fit(self, X, y):
        """
        Fit data to create decision tree
        :param X: Features
        :param y: Labels
        :return: Decision Tree
        """
        self.classWeight = self.computeClassWeight(y)
        self.root = self.buildTree(X, y)

    def computeClassWeight(self, y):
        """
        Compute class weight for each class label
        :param y: Class labels
        :return: Array of class weights
        """
        values, counts = np.unique(y, return_counts=True)
        total = len(y)
        classes = len(values)

        weights = {}
        for val, count in zip(values, counts):
            weights[val] = total / (classes * count)

        return weights
        # values,counts = np.unique(y, return_counts=True)
        #
        # majorityClass = values[np.argmax(counts)]
        # minorityClass = values[np.argmin(counts)]
        #
        # x0 = counts[np.argmax(counts)]
        # x1 = counts[np.argmin(counts)]
        #
        # IR = x1 / x0
        #
        # weights = {
        #     majorityClass : IR,
        #     minorityClass : 1.0
        # }
        # return weights

    def buildTree(self, X, y, depth=0):
        """
        Method that builds the decision tree recursively
        :param X: Features
        :param y: Labels
        :param depth: Depth of current tree
        :return: Decision Tree
        """
        # number of samples in each column, number of columns
        numSamples, numFeatures = X.shape
        # 1 if just fraud/notFraud, 2 if both
        numLabels = len(np.unique(y))

        # Check if we pass tests that tell use to continue or not
        if numLabels == 1 or depth >= self.maxDepth or numSamples < self.minSampleSplit:
            values, counts = np.unique(y, return_counts=True)
            leafValue = values[np.argmax(counts)]
            return Node(value=leafValue)

        # pick random features to consider
        featureIndex = np.random.choice(numFeatures, self.nFeatures, replace=False)

        bestFeature, bestThreshold = self.bestSplit(X, y, featureIndex)

        # if there is no good feature then we should stop
        if bestFeature is None:
            values, counts = np.unique(y, return_counts=True)
            leafValue = values[np.argmax(counts)]
            return Node(value=leafValue)

        featureData = X.iloc[:, bestFeature]

        columnName = X.columns[bestFeature]

        # Check to see if we are handling discrete vs continuous data
        if columnName in self.discreteData:
            curIsDiscrete = True
            leftIndex, rightIndex = self.split(featureData, bestThreshold, True)
        else:
            curIsDiscrete = False
            leftIndex, rightIndex = self.split(featureData, bestThreshold, False)

        # in case one or splits give an empty list
        if len(leftIndex) == 0 or len(rightIndex) == 0:
            values, counts = np.unique(y, return_counts=True)
            leafValue = values[np.argmax(counts)]
            return Node(value=leafValue)

        # If we don't pass chiSquare test then also stop splitting
        if not (self.chiSquareTest(y, y.iloc[leftIndex], y.iloc[rightIndex])):
            values, counts = np.unique(y, return_counts=True)
            leafValue = values[np.argmax(counts)]
            return Node(value=leafValue)

        # get the data that will go into left and right nodes
        leftData = X.iloc[leftIndex, :]
        rightData = X.iloc[rightIndex, :]

        left = self.buildTree(leftData, y.iloc[leftIndex], depth + 1)
        right = self.buildTree(rightData, y.iloc[rightIndex], depth + 1)

        # recurse
        return Node(bestFeature, bestThreshold, left, right, isDiscrete=curIsDiscrete)

    def bestSplit(self, X, y, featureIndex):
        """
        Determine what the best feature to split based on
        :param X: Features
        :param y: Labels
        :param featureIndex: Index's of the features that we should consider
        :return: Feature Index and what we split based on
        """
        bestInfoGain = -1
        splitIndex = None
        splitThreshold = None

        # loop through the features we are considering
        for features in featureIndex:
            featureData = X.iloc[:, features]
            columnName = X.columns[features]

            if columnName in self.discreteData:
                candidateThreshold = np.unique(featureData)
                isDiscrete = True
            else:  # handle continuous data
                uniqueVal = np.unique(featureData)
                if len(uniqueVal) == 1:
                    continue

                maxCandidates = 30
                if len(uniqueVal) > maxCandidates:
                    candidateThreshold = np.percentile(uniqueVal, np.linspace(0, 100, maxCandidates + 1)[1:])
                else:
                    candidateThreshold = (uniqueVal[:-1] + uniqueVal[1:]) / 2
                isDiscrete = False

            # Determine what candidate we should use based on the current feature
            for candidate in candidateThreshold:
                leftChildIndex, rightChildIndex = self.split(featureData, candidate, isDiscrete)
                leftChild = y.iloc[leftChildIndex]
                rightChild = y.iloc[rightChildIndex]

                infoGain = self.informationGain(y, leftChild, rightChild)
                if infoGain > bestInfoGain:
                    bestInfoGain = infoGain
                    splitIndex = features
                    splitThreshold = candidate

        return splitIndex, splitThreshold

    def split(self, data, threshold, isDiscrete=False):
        """
        Split the data into left and right based on given threshold
        :param data: Data being split
        :param threshold: Threshold to split based on
        :param isDiscrete: If given threshold is discrete or not
        :return: Index we split at
        """
        if isDiscrete:
            leftChildIndex = np.argwhere(data == threshold).flatten()
            rightChildIndex = np.argwhere(data != threshold).flatten()
        else:
            leftChildIndex = np.argwhere(data <= threshold).flatten()
            rightChildIndex = np.argwhere(data > threshold).flatten()
        return leftChildIndex, rightChildIndex

    def chiSquareTest(self, parentLabels, leftLabels, rightLabels):
        """
        Calculate chiSquare to see if it will pass based on given labels
        :param parentLabels: Parent node labels
        :param leftLabels: Left node labels
        :param rightLabels: Right node labels
        :return: True if we pass chiSquare, false if not
        """

        parentValues, parentCounts = np.unique(parentLabels, return_counts=True)
        parentProportion = parentCounts / len(parentLabels)

        leftCounts = [np.sum(leftLabels == label) for label in parentValues]
        rightCounts = [np.sum(rightLabels == label) for label in parentValues]

        expectedCountLeft = [pro * len(leftLabels) for pro in parentProportion]
        expectedCountRight = [pro * len(rightLabels) for pro in parentProportion]

        chiSquareLeft = [(leftCount - expectedLeft) ** 2 / expectedLeft for (leftCount, expectedLeft) in
                         zip(leftCounts, expectedCountLeft)]
        chiSquareRight = [(rightCount - expectedRight) ** 2 / expectedRight for (rightCount, expectedRight) in
                          zip(rightCounts, expectedCountRight)]

        return (sum(chiSquareLeft) + sum(chiSquareRight)) >= self.chiSquareTerm

    def informationGain(self, parent, left, right):
        """
        Calculate information gain based on parent node, left node, and right node
        :param parent: Parent node features
        :param left: Left node features
        :param right: Right node features
        :return: Information gain value based on criterium
        """
        if len(right) == 0 or len(left) == 0:
            return 0

        if self.criterium == "entropy":
            parent_impurity = self.entropy(parent)
            left_weight = self.entropy(left) * (len(left) / len(parent))
            right_weight = self.entropy(right) * (len(right) / len(parent))
            final_weight = parent_impurity - (left_weight + right_weight)
            return final_weight
        elif self.criterium == "weightedEntropy":
            parent_impurity = self.weightedEntropy(parent)
            left_weight = self.weightedEntropy(left) * (len(left) / len(parent))
            right_weight = self.weightedEntropy(right) * (len(right) / len(parent))
            final_weight = parent_impurity - (left_weight + right_weight)
            return final_weight
        elif self.criterium == "gini":
            parent_impurity = self.giniIndex(parent)
            left_weight = self.giniIndex(left) * (len(left) / len(parent))
            right_weight = self.giniIndex(right) * (len(right) / len(parent))
            final_weight = parent_impurity - (left_weight + right_weight)
            return final_weight
        elif self.criterium == "weightedGini":
            parent_impurity = self.weightGiniIndex(parent)
            left_weight = self.weightGiniIndex(left) * (len(left) / len(parent))
            right_weight = self.weightGiniIndex(right) * (len(right) / len(parent))
            final_weight = parent_impurity - (left_weight + right_weight)
            return final_weight
        elif self.criterium == "misclassification":
            parent_impurity = self.misclassificationError(parent)
            left_weight = self.misclassificationError(left) * (len(left) / len(parent))
            right_weight = self.misclassificationError(right) * (len(right) / len(parent))
            final_weight = parent_impurity - (left_weight + right_weight)
            return final_weight
        elif self.criterium == "weightedMisclassification":
            parent_impurity = self.weightedMisclassificationError(parent)
            left_weight = self.weightedMisclassificationError(left) * (len(left) / len(parent))
            right_weight = self.weightedMisclassificationError(right) * (len(right) / len(parent))
            final_weight = parent_impurity - (left_weight + right_weight)
            return final_weight
        return None

    def entropy(self, collection):
        """
        Calculate entropy based on given collection of features
        :param collection: Collection of features
        :return: Entropy value
        """
        total = len(collection)

        values, counts = np.unique(collection, return_counts=True)

        probabilities = counts / total

        entropyValue = 0

        for i in probabilities:
            entropyValue += -i * np.log2(i)
        return entropyValue

    def weightedEntropy(self, collection):
        """
        Calculate weighted entropy based on given collection of features
        :param collection: Collection of features
        :return: Entropy value
        """
        total = len(collection)
        values, counts = np.unique(collection, return_counts=True)

        probabilities = counts / total

        entropyValue = 0

        for val, probs in zip(values, probabilities):
            weight = self.classWeight[val]
            entropyValue += -(weight * probs) * np.log2(probs)

        return entropyValue


    def giniIndex(self, collection):
        """
        Calculate giniIndex based on given collection of features
        :param collection: Collection of features
        :return: GiniIndex value
        """
        total = len(collection)
        values, counts = np.unique(collection, return_counts=True)
        probabilities = counts / total
        giniValue = 0
        for i in probabilities:
            giniValue += i * i
        return 1 - giniValue

    def weightGiniIndex(self, collection):
        """
        Calculate weighted giniIndex based on given collection of features
        :param collection: Collection of features
        :return: GiniIndex value
        """
        total = len(collection)
        values, counts = np.unique(collection, return_counts=True)
        probabilities = counts / total
        giniValue = 0
        for val, probs in zip(values, probabilities):
            weight = self.classWeight[val]
            giniValue += probs * probs * weight
        return 1 - giniValue

    def misclassificationError(self, collection):
        """
        Calculate misclassification error based on given collection of features
        :param collection: Collection of features
        :return: Misclassification error value
        """
        totalLabel = len(collection)
        values, counts = np.unique(collection, return_counts=True)
        probabilities = counts / totalLabel
        maxProb = probabilities.max()

        return 1 - maxProb

    def weightedMisclassificationError(self, collection):
        """
        Calculate weighted misclassification error based on given collection of features
        :param collection: Collection of features
        :return: Misclassification error value
        """
        values, counts = np.unique(collection, return_counts=True)

        weighted_counts = []
        for val, count in zip(values, counts):
            weight = self.classWeight[val]
            weighted_counts.append(count * weight)

        total_weighted = sum(weighted_counts)
        weighted_probs = [wc / total_weighted for wc in weighted_counts]

        maxProb = max(weighted_probs)
        return 1 - maxProb

    def predict(self, X):
        """
        Predict given data based on decision tree.
        :param X:
        :return: Predictions made by decision tree.
        """
        return np.array([self.traverseTree(x, self.root) for x in X.to_numpy()])

    def traverseTree(self, x, node):
        """
        Traver decision tree
        :param x: current data entry being predicted
        :param node: Node location
        :return: final decision
        """
        if node.value is not None:
            return node.value

        if node.isDiscrete:
            if x[node.feature] == node.threshold:
                return self.traverseTree(x, node.left)
            else:
                return self.traverseTree(x, node.right)
        else:
            if x[node.feature] <= node.threshold:
                return self.traverseTree(x, node.left)
            else:
                return self.traverseTree(x, node.right)

    def getHeight(self):
        """
        Returns the height of the decision tree.
        :return: Height of tree
        """
        return self.treeHeight(self.root)

    def treeHeight(self, node):
        """
        Traver the decision tree to get the height
        :param node: Root node
        :return: Height of decision tree
        """

        if node.value is not None:
            return 0  # not sure if this should be zero or a one
        if node.right is None:
            return 1 + self.treeHeight(node.left)
        if node.left is None:
            return 1 + self.treeHeight(node.right)
        leftHeight = self.treeHeight(node.left)
        rightHeight = self.treeHeight(node.right)

        return 1 + max(leftHeight, rightHeight)
