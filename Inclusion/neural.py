import numpy, random, os

#Two input values, true or false, expected output we should get
def Perceptron(input1, input2, output):
    outputP = input1 * weights[0] + input2*weights[1] + bias* weights[2]
    if outputP > 0: 
        outputP = 1
    else:
        outputP = 0

    error = output - outputP
    weights[0] += error * input1 * lr
    weights[1] += error * input2 * lr
    weights[2] += error * bias * lr

lr = 1 # Learning rate
bias = 1 # value of bias
weights = [random.random(), random.random(), random.random()] # Generate random weight values



#Create loop that makes neural network repeat every situtation several times
# This is the learning phase
for i in range(50):
    Perceptron(1,1,1)
    Perceptron(1,0,1)
    Perceptron(0,1,1)
    Perceptron(0,0,0) 

x = int(input())
y = int(input())

outputP = x * weights[0] + y * weights[1] + bias * weights[2]
if outputP > 0:
    outputP = 1
else:
    outputP = 0



print(x, "or", y, "is  : " , outputP)
