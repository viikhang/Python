import math

import pandas as pd
import numpy as np


from DecisionTree import DecisionTree
from RandomForest import RandomForest


def main():
    # load training data
    trainingData = pd.read_csv('train.csv')
    X = trainingData.drop("isFraud", axis=1)
    X = X.drop("TransactionID", axis=1)

    #Uncomment to run smaller data size
    #X = X.sample(n=10000, random_state=42)


    continuousData = {"TransactionDT", "TransactionAmt", "C1", "C2", "C3", "C4", "C5", "C6", "C7", "C8", "C9", "C10",
                      "C11", "C12", "C13", "C14"}
    discreteData = {"ProductCD", "card1", "card2", "card3", "card4", "card5", "card6", "addr1", "addr2"}

    #different ways we can handle missing data
    # X = inputMissing(X, continuousData, discreteData)
    # X = keepNotFoundNegative(X, continuousData)

    #preprocess data:
    X = keepNotFoundMedian(X, continuousData)
    y = trainingData["isFraud"]

    # for smaller data size
    y = y[X.index] #using smaller training size to test if tree even works

    #loading testing data we are trying to predict
    testingData = pd.read_csv('test.csv')
    testingData = keepNotFoundMedian(testingData, continuousData)
    testingDataDropped = testingData.drop("TransactionID", axis=1)

    #Values that can be adjusted for decision tree
    criterium = "weightedGini"
    chiSquareTerm = 0.01
    numTrees = 200

    #create model based on given data
    #For creating just a decision tree
    #finalModel = DecisionTree(criterium, chiSquareTerm, discreteData, continuousData, maxDepth=10,nFeatures=int(math.sqrt(X.shape[1])))
    #finalModel = RandomForest(numTrees, criterium, 0.9, discreteData, continuousData, maxDepth=10,nFeatures=5, minSampleSplit=25)
    finalModel = RandomForest(numTrees,criterium, chiSquareTerm, discreteData, continuousData, maxDepth=15, nFeatures=int(math.sqrt(X.shape[1])))
    #make model based on given data
    finalModel.fit(X, y)

    print("Predicting")
    testPredictions = finalModel.predict_multiple_trees(testingDataDropped)

    #for just creating a decision tree and predicting with it
    #testPredictions = finalModel.predict(testingDataDropped) #for using decision tree prediction

    # create file of our results
    output = pd.DataFrame({
        "TransactionID": testingData["TransactionID"],
        "isFraud": testPredictions
    })
    output.to_csv("submission.csv", index=False)
    #output.to_csv(r"C:\machineLearning\submission.csv", index=False)


def inputMissing(X, continuousData, discreteData):
    """
    Handles missing values from data set by adjusting both continuous and discrete columns
    :param X: Features that contain missing data
    :param continuousData: Continuous features
    :param discreteData: Discrete features
    :return: New dataset without missing features
    """
    XCopy = X.copy()
    for data in continuousData:
        #replace missing continuous data with median value
        XCopy[data] = pd.to_numeric(XCopy[data].replace("NotFound", np.nan))
        median = XCopy[data].median()
        XCopy[data] = XCopy[data].fillna(median)
    for data in discreteData:
        #replace missing discrete data with most common value
        mode = XCopy[data].mode()[0]
        XCopy[data] = XCopy[data].replace("NotFound", mode)

    return XCopy


def keepNotFoundMedian(X, continuousData):
    """
    Handles missing values by adjusting only continuous data
    :param X: Features that contain missing data
    :param continuousData: Continuous features
    :return: New dataset adjusted to handle missing features
    """
    XCopy = X.copy()
    for data in continuousData:
        # replace missing continuous data with median value
        XCopy[data] = pd.to_numeric(XCopy[data].replace("NotFound", np.nan))
        median = XCopy[data].median()
        XCopy[data] = XCopy[data].fillna(median)
    return XCopy


def keepNotFoundNegative(X, continuousData):
    """
    Handles missing values by adjusting only continuous data, gives a value that is likely not in the data set
    :param X: Features that contain missing data
    :param continuousData: Continuous features
    :return: New dataset adjusted to handle missing features
    """
    XCopy = X.copy()
    for data in continuousData:
        XCopy[data] = pd.to_numeric(XCopy[data].replace("NotFound", -429))
    return XCopy


if __name__ == "__main__":
    main()
