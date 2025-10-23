import numpy as np

def sigmoid(x):
    return 1 / (1 + np.exp(-x))

class LogisticRegression():

    def __init__(self, learningRate = 0.001, numberIterations = 1000):
        self.learningRate = learningRate
        self.numberIterations = numberIterations
        self.weights = None
        self.bias = None

    def fit(self, X, y):
        nSamples, nFeatures = X.shape
        self.weights = np.zeros(nFeatures)
        self.bias = 0

        for _ in range(self.numberIterations):
            prediction = np.dot(X, self.weights) + self.bias
            actualPrediction = sigmoid(prediction)

            #calculate gradient
            gradientWeight = (1/nSamples) * np.dot(X.T, (actualPrediction - y))
            gradientBias = (1/nSamples) * np.sum(actualPrediction - y)

            self.weights = self.weights - self.learningRate * gradientWeight
            self.bias = self.bias - self.learningRate * gradientBias



    def predict(self, X):
        prediction = np.dot(X, self.weights) + self.bias
        actualPrediction = sigmoid(prediction)
        classPred = [0 if y <= 0.5 else 1 for y in actualPrediction]
        return classPred
