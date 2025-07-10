# Kyle Nguyen
import random

def initialBoard():
    board = [['-','-','-','-'] ,
            ['-','-','-','-'] ,
            ['-','-','-','-'] ,
            ['-','-','-','-'] ]
    return board



def spawnRanPiece(board):
    # can't spawn a random piece if it is full
    count = boardCount(board)
    if count == 16:
        return board

    while True:
        randTileVal = random.randint(0,9)
        if randTileVal == 9:
            randTileVal = 4
        else:
            randTileVal = 2

        randRow = random.randint(0,3)
        randCol = random.randint(0,3)

        if board[randRow][randCol] == '-':
            board[randRow][randCol] = randTileVal
            return board

def printBoard(board):
    #THIS NEEDS TO BE UPDATED, IF WE HAVE A NUMBER THAT IS TWO CHARACTERS LONG, 
    # THEN ALL THE OTHER TILES NEED TO BE TWO CHARACTERS LONG TOO
    for i in range (len(board)):
        for j in range (len(board[0])):
            print(board[i][j], end="")
            if not j == len(board[0]) - 1:
                print("|",end="")
        print("")

def getUserInput():
    while True:
        userIn = input("Playermove: ")
        userIn = userIn.lower()
        if userIn == 'w' or userIn == 'a' or userIn == 's' or userIn == 'd':
            return userIn
        else:
            print("Invalid input received, please enter in w, a, s, or d")

def movePiece(board, move):
    if move == 'w':
        return handleUp(board)
    elif move == 'a':
        return handleLeft(board)
    elif move == 's':
        return handleDown(board)
    elif move == 'd':
        return handleRight(board)
    else: 
        print("Invalid move given")

#Move all pieces up, then check if its surrounding pieces have any matches, 
# if it does, then connect them, after recheck again if there is any gaps 

# Order I search in will matter, should look at the tiles closer to the wall first

def handleUp(board):
    movePiecesUp(board)
    
    # After moving the pieces up, need to check the surrounding pieces to see if any pieces next to each other match

    # tileCombined = [] # Don't think I need this, after combining the pieces, there shoudn't be any more pieces that can be combined
    for i in range (len(board)):
        for j in range (len(board[0])):
            piece = board[i][j]
            if i - 1 >= 0 and (not piece == '-') and board[i-1][j] == piece:
                board[i][j] = '-'
                intPiece = int(piece) * 2
                board[i-1][j] = intPiece
                # tileCombined.append((i-1,j))
    
    movePiecesUp(board)
    return board

def movePiecesUp(board):
    for i in range(len(board)):
        for j in range(len(board[0])):
            piece = board[i][j]
            #If we find a tile piece, we now need to move it up 
            if not piece == '-':
                board[i][j] = '-'
                rowTemp = i
                #Find the next tile piece that isn't empty
                while rowTemp - 1 >= 0 and board[rowTemp-1][j] == '-':
                    rowTemp-=1
                board[rowTemp][j] = piece
    


def handleDown(board):
    movePiecesDown(board)

    i = len(board) -1
    while i > -1:
        for j in range(len(board[0])):
            piece = board[i][j]
            if i + 1 < len(board) and (not piece == '-') and board[i+1][j] == piece:
                board[i][j] = '-'
                intPiece = int(piece) * 2
                board[i+1][j] = intPiece
        i-=1
    movePiecesDown(board)
    return board


def movePiecesDown(board):
    i = len(board) -1
    #Start at the bottom then make your way up^
    while i > -1:
        for j in range (len(board[0])):
            piece = board[i][j]
            
            if not piece == '-':
                board[i][j] = '-'
                rowTemp = i
                while rowTemp + 1 < len(board) and board[rowTemp + 1][j] == '-':
                    rowTemp+=1
                board[rowTemp][j] = piece    
        i-=1
    


def handleLeft(board):
    movePiecesLeft(board)
    for i in range(len(board)):
        for j in range(len(board[0])):
            piece = board[i][j]
            if j - 1 > -1 and (not piece == '-') and board[i][j-1] == piece:
                board[i][j] = '-'
                intPiece = int(piece) * 2
                board[i][j-1] = intPiece

    movePiecesLeft(board)
    return board

def movePiecesLeft(board):
    for i in range (len(board)):
        for j in range (len(board[0])):
            piece = board[i][j]
            if not piece == '-':
                board[i][j] = '-'
                colTemp = j
                while colTemp - 1 > -1 and board[i][colTemp-1] == '-':
                    colTemp-=1
                board[i][colTemp] = piece
    

def handleRight(board):
    movePiecesRight(board)
    for i in range(len(board)):
        j = len(board[0]) -1
        while j > -1:
            piece = board[i][j]
            if j + 1 < len(board[0]) and (not piece == '-') and board[i][j+1] == piece:
                board[i][j] = '-'
                intPiece = int(piece) *2
                board[i][j+1] = intPiece

    movePiecesRight(board)
    return board

def movePiecesRight(board):
    for i in range(len(board)):
        j = len(board[0]) -1
        while j > - 1:
            piece = board[i][j]
            if not piece == '-':
                colTemp = j
                while colTemp + 1 < len(board[0]) and board[i][colTemp+1] == '-':
                    colTemp+=1
                board[i][colTemp] = piece    
                board[i][j] = '-'


def boardCount(board):
    tileCount = 0
    for i in range (len(board)):
        for j in range (len(board[0])):
            if not board[i][j] == '-':
                tileCount+=1
    return tileCount

def checkGameOver(board):
    tileCount = 0
    for i in range (len(board)):
        for j in range(len(board[0])):
            if not board[i][j] == '-':
                tileCount+=1
            # Found a piece with 2048 value
            if board[i][j] == '2048':
                return 1
            
    if tileCount == 16:
        canMove = checkPossibleMoves(board)
        if canMove:
            return 0
        else:
            return -1
    
    return 0


# Check if there is any possible moves when the game is full
def checkPossibleMoves(board):
    # At each position, check if any of its neighbors has the same number, 
    # if it does, then there is a possible move

    for i in range (len(board)):
        for j in range (len(board[0])):
            numValue = board[i][j]

            # Check below
            if i + 1 < len(board) and board[i + 1][j] == numValue:
                return True
            # Check Above
            if i - 1 > -1 and board[i-1][j] == numValue:
                return True
            
            if j + 1 < len(board[0]) and board[i][j+1] == numValue:
                return True
            if j - 1 > -1 and board[i][j-1] == numValue:
                return True
            
    return False

def continuePlaying():
    return False

            
if __name__ == '__main__':
    print("Wellcome to 2048!")
    print("2048 is a simple game played on a 4x4 board")
    print("On the board, a random tile will spawn each time a move has been made")
    print("Each tile that spawns will have a number value, the goal is to combine tiles until one of the tile values becomes 2048")
    print("A tile will be combined with another when tiles are touch each other")

    #When the game starts, have two tiles be spawned on the board
    gameBoard = initialBoard()
    
    #Add two tiles to the start of the game
    gameBoard = spawnRanPiece(gameBoard)
    gameBoard = spawnRanPiece(gameBoard)

    printBoard(gameBoard)

    playingGame = True

    while playingGame:
        # Get user input
        playerInput = getUserInput()

        # Apply user input
        gameBoard = movePiece(gameBoard, playerInput)
        printBoard(gameBoard)

        # Check if game is over. Game is over if the whole board is filled, and there is no more possible moves, 
        # or if there is a tile with a value of 2048

        gameState = checkGameOver(gameBoard)
        if gameState == 1:
            print("You won! You have a tile with value 2048!")
            #TODO Probably ask the user if they want to continue playing or just quit the game here
            playingGame = continuePlaying()


        elif gameState == -1:
            print("You lost! The board is full and there is no more possible moves that can be made!")
            playingGame = False

        #If the user doesn't make a game winning move, now add a random piece

        gameBoard = spawnRanPiece(gameBoard)



        # Repeat 

