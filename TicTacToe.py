
def checkWinner(board, row, col):
    #Need to check all possible directions of the piece that was placed
    pass

def playAgain():
    while(True):
        userIn = input("Would you like to play again? (Yes/No)")

        if(userIn == "Yes" or userIn == "yes"):
            return True
        elif(userIn == "No" or userIn == "no"):
            return False
        else:
            print("Invalid input given, please type yes or no") 
    


if __name__ == '__main__':
    previousMoves = []

    gameBoard = [['-','-','-'] ,
                 ['-','-','-'] ,
                 ['-','-','-'] ]
    print("Welcome to TicTacToe!\n" \
    "To play the game, type the row number followed by the column number\n" \
    "For example, 11 corresponds to the top left and 22 correspons to the middle\n" \
    "Whoever creates a line with three of the same characters wins!")

    print("Player 1 enter in desired letter: ")
    validLetter = False
    letterP1 = input("Player 1 enter in desired letter: ")
    while(len(letterP1) != 1):
        letterP1 = input("Invalid input given, please give a new input: ")

    letterP1 = input("Player 1 enter in desired letter: ")
    letterP2 = input("Player 2 enter in desired letter: ")

    while(letterP1 == letterP2):
        print("Player 2 please choose a different letter again!")
        letterP2 = input("Player 2 enter in a desired leter: ")
    
    playingGame = True
    P1Turn = True

    while(playingGame):
        currentChar = None
        if(P1Turn):
            currentChar = letterP1
            print("Player 1, please pick your move")
        else:
            currentChar = letterP2
            print("Player 2, please pick your move")

        validMove = False
        playerMove = None
        while(not validMove):
            playerMove = input("Input: ")
            if(len(playerMove) == 2):
                try:
                    playerMove = int (playerMove)
                except:
                    print("Invalid input given, please give a different input")
            else:
                print("Invalid input length given, please give a different input")
            #Check if a valid row and column values are given
            rowVal = playerMove // 10
            colVal = playerMove % 10

            if(not (rowVal == 1 or rowVal == 2 or rowVal == 3)):
                print("Invalid row number given, please give a different input")
            else:
                if (not (colVal == 1 or colVal == 2 or colVal == 3)):
                    print("Invalid column value given, please give a different input")
                else:
                    if playerMove in previousMoves:
                        print("Move already made at this location, please give a different input")
                    else:
                        validMove = True # If we've reached this fair this we have a valid move

        row = playerMove // 10
        col = playerMove % 10

        gameBoard[row][col] = currentChar

        if(checkWinner):
            if(P1Turn):
                print("Player one has won!")
            else:
                print("Player two has won!")
        
        P1Turn = not P1Turn



            


