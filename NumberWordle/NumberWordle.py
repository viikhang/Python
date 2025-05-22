import random

def checkWinner(numSeq):
    for i in range(len(numSeq)):
        if(numSeq[i] == 'X' or numSeq[i] == 'W'):
            return False
    return True

def printList(numSeq):
    for i in range(len(numSeq)):
        print(numSeq[i], end="")
    print("")

if __name__ == '__main__':
    randomSequence = []
    while(len(randomSequence) != 5):
        randomNumber = random.randint(0,9)
        if randomNumber in randomSequence:
            pass
        else: 
            randomSequence.append(randomNumber)
    printList(randomSequence)

    print("Welcome to Number Wordle! \n" \
    "In this version, you will be given a random five number sequence,\n"\
    "where no duplicate numbers are present\n\n" \
    "X represents a unknown number\n" \
    "W represents a correct number but wrong position\n" \
    "If the number is in the correct position, it will appear\n\n" \
    "You will have four attemps, good luck!\n")
    guessedCorrect = False
    numAttempts = 1
    while(numAttempts != 5):
        print("Attempt#", numAttempts)
        userSeqInt = 0
        userSeq = input("Input: ")
        if(len(userSeq) != 5):
            print("Invalid input")
            print("Please enter in at least 5 numbers")
            pass
        try: 
            userSeqInt = int(userSeq)
        except:
            print("Invalid input")
            print("Please enter a valid sequece (Example: 12345)")
            pass
        
        outputSeq = ["X","X","X","X","X"]

        for i in range(len(userSeq)):
            number = int (userSeq[i])
            if(randomSequence[i] == number): # If numbers match, indicate it
                outputSeq[i] = number
            else: # Check if the number is in a different position now
                for j in range(len(userSeq)):
                    if(randomSequence[j] == number):
                        outputSeq[i] = 'W'

        if checkWinner(outputSeq):
            print("You guessed the correct sequence!")
            printList(outputSeq)
            numAttempts = 5
            guessedCorrect = True
        else:
            print(outputSeq)
            numAttempts+=1
        
        

    if(not guessedCorrect):
       print("Thank you for playing! The correct sequence was: ")
       printList(randomSequence)
       

