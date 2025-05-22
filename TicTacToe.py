# Kyle Nguyen
# Simple TicTacToe game that is played through the terminal

# Checks if the current piece has made a winning move on the gameboard
# -1 Represents that no one has won and the game can continue
# 1 Represents that the current piece has made a winning move
# 0 Represents that a draw has been made
def checkWinner(gameBoard,curChar, row, col):
    totalPieces = checkNumPieces(gameBoard) 
    if totalPieces < 4: # Must be at least  
        return -1
    else:
        if(checkHorizontal(gameBoard, row, curChar) or 
           checkVertical(gameBoard, col, curChar) or
           checkDiagonal(gameBoard, row, col, curChar)):
            return 1
        else:
            if(totalPieces == 9):
                return 0
            else:
                return -1

#Check if player has won in horizontal direction 
def checkHorizontal(gameBoard, row, char):
    charCount = 0
    for j in range (len(gameBoard[0])):
        if (gameBoard[row][j] == char):
            charCount+=1
    return charCount == 3

#Check if player has won in diagonal direction
def checkDiagonal(gameBoard, row, col, char):
    if (row == 0 and col == 1):
        return False
    if (row == 1 and col == 0):
        return False
    if (row == 1 and col == 2):
        return False
    if (row == 2 and col == 1):
        return False
    # Check right diagonal \
    charCount = 0
    i = 0
    j = 0
    while( i < len(gameBoard)):
        if(gameBoard[i][j] == char):
            charCount+=1
        i+=1
        j+=1
    
    if(charCount == 3):
        return True
    
    # Check left diagonal /
    charCount = 0
    i = 0
    j = 2
    while (i < len(gameBoard)):
        if(gameBoard[i][j] == char):
            charCount+=1
        i+=1
        j-=1

    return charCount == 3
    
#Check if player has won in vertical direction
def checkVertical(gameBoard, col, char):
    charCount = 0
    for i in range (len(gameBoard)):
        if(gameBoard[i][col] == char):
            charCount+=1
    return charCount == 3
    
#Check number of pieces currently on the gameboard
def checkNumPieces(gameBoard):
    totalPiece = 0
    for i in range(len(gameBoard)):
        for j in range (len(gameBoard[0])):
                if not gameBoard[i][j] == '-':
                    totalPiece+=1
    return totalPiece

#Print what the game board currently looks like
def printGameBoard(gameBoard):
    print("Gameboard: ")
    for i in range (len(gameBoard)):
        for j in range (len(gameBoard[0])):
            gameChar = gameBoard[i][j]
            if(not (gameChar == '-')):
                print(gameChar, end="")
            else:
                print(" ", end="")
            if( not (j == len(gameBoard[0]) -1) ):
                print("|", end="")
        print("")

# Prints the board and the corresponding positions
def printDefaultBoard():
    print("")
    print("11|12|13")
    print("21|22|23")
    print("31|32|33")
    print("")

# Returns empty game board
def defaultBoard():
    board = [['-','-','-'] ,
            ['-','-','-'] ,
            ['-','-','-'] ]
    return board

# Main main where the program starts
if __name__ == '__main__':
    previousMoves = []
    gameBoard = defaultBoard()
    gameDone= False

    print("Welcome to TicTacToe!\n" \
    "To play the game, type the row number followed by the column number\n" \
    "For example, 11 corresponds to the top left and 22 correspons to the middle\n" \
    "Whoever creates a line with three of the same characters wins!")

    printDefaultBoard()
    

    validLetter = False
    letterP1 = input("Player 1 enter in desired letter: ")
    while(len(letterP1) != 1):
        letterP1 = input("Invalid input given, please give a new input: ")

    
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
                        previousMoves.append(playerMove)

        row = (playerMove // 10) - 1
        col = (playerMove % 10) - 1

        # Place piece on board
        gameBoard[row][col] = currentChar

        #After a valid move has been made, need to print the board out
        printGameBoard(gameBoard)

        # After player places piece down, now check if they have won
        gameStatus = checkWinner(gameBoard,currentChar, row, col) 
        if(gameStatus == 1): # Game has been won
            if(P1Turn):
                print("Player 1 has made a winning move!")
            else:
                print("Player 2 has made a winning move!")
                gameDone = True
        elif (gameStatus == 0): # Game has resulted in a draw
            print("All spots on the board have been filled and no player has won! " \
                  "Game has ended with a draw!")
            gameDone = True
            
        else: # Game can continued to be played
            pass

        P1Turn = not P1Turn

        if(gameDone):
            playAgain = input("Would you like to play again? (y/n): ")
            if(playAgain == "y" or playAgain == "Y"):
                print("Player one will start first again!")
                P1Turn = True #Make player one start first
                gameBoard = defaultBoard()
                previousMoves = []
                printDefaultBoard()
                gameDone = False
            else:
                playingGame = False
                print("Thank you for playing!")