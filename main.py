import numpy as np


game = np.zeros((9,9))
game = np.array([
        [3, 0, 6, 5, 0, 8, 4, 0, 0],
        [5, 2, 0, 0, 0, 0, 0, 0, 0],
        [0, 8, 7, 0, 0, 0, 0, 3, 1],
        [0, 0, 3, 0, 1, 0, 0, 8, 0],
        [9, 0, 0, 8, 6, 3, 0, 0, 5],
        [0, 5, 0, 0, 9, 0, 6, 0, 0],
        [1, 3, 0, 0, 0, 0, 2, 5, 0],
        [0, 0, 0, 0, 0, 0, 0, 7, 4],
        [0, 0, 5, 2, 0, 6, 3, 0, 0]
    ])

easy = np.array([
    [5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9]
])


hard = np.array([
    [0, 0, 0, 6, 0, 0, 4, 0, 0],
    [7, 0, 0, 0, 0, 3, 6, 0, 0],
    [0, 0, 0, 0, 9, 1, 0, 8, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 5, 0, 1, 8, 0, 0, 0, 3],
    [0, 0, 0, 3, 0, 6, 0, 0, 0],
    [0, 0, 0, 0, 0, 7, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0]
])

class GameState:
    def __init__(self, array):
        self.gameArray = array
        self.dataArray = LoadGame(array)

class Square:
    def __init__(self, x, y, value):
      self.x = x 
      self.y = y
      self.solved = False
      self.value = value
      self.possibilities= np.array([1,2,3,4,5,6,7,8,9])



game = hard 

def LoadGame(array):
    gameState = np.empty((9,9), dtype=object)
    for y in range(9):
       for x in range(9):
           gameState[y,x] = Square(x,y,array[y,x])
    return gameState
 

def SolveGame(gameState):
    lastindicies = np.where(gameState.gameArray==1)
    attempts = 0

    while 1:
        indicies = np.where(gameState.gameArray==0)
        if (indicies[0].shape == lastindicies[0].shape):
            if (indicies[0] == lastindicies[0]).all():
                attempts+=1
                if attempts == 2:
                    print("no new solves, stuck")
                    print(game)
                    return
            else:
                attempts = 0
        lastindicies = indicies
        if (len(indicies[0])==0):
            print(game)
            return
        for i in range(len(indicies[0])):
            #indicies[0] = y
            #indicies[1] = x
            Solve(indicies[1][i], indicies[0][i], gameState)


def Solve(x,y,gameState):
    #load possiblities into variable for ease of use 
    possibilities = gameState.dataArray[y,x].possibilities
    #vertical slice
    possibilities = np.setdiff1d(possibilities, gameState.gameArray[:,x])
    #horizontal slice
    possibilities = np.setdiff1d(possibilities, gameState.gameArray[y,:] )
    #region
    regionX, regionY = GetTopLeftCornerOfRegion(x,y)
    possibilities = np.setdiff1d(possibilities,gameState.gameArray[regionY:regionY+3,regionX:regionX+3])
    gameState.dataArray[y,x].possibilities = possibilities
    if len(possibilities) == 1:
        print("solved at ",x, "," , y)
        gameState.gameArray[y,x] = possibilities[0]
        return

    #vert,horizontal,region singular didn't work, narrowed it down to the minimum posibilities
    #take all the blank spots in the row
    blankRowMask = gameState.gameArray[y,:] == 0
    blankSquares = gameState.dataArray[y,blankRowMask] 
    existingPossibilities = np.empty((1))
    #combine all the possible options for all the other blank spots in the row
    for square in blankSquares:
        existingPossibilities = np.concatenate((existingPossibilities, square.possibilities))
    #remove all the possible options from our taget, if only 1 item remains it has to be that item
    possibilities = np.setdiff1d(possibilities, square.possibilities)
    if len(possibilities)==1:
        print("solved at ",x, "," , y)
        gameState.dataArray[y,x].value = possibilities[0]
        gameState.gameArray[y,x] = possibilities[0]
        return

    #repeat for column
    blankColMask = gameState.gameArray[:,x] == 0
    blankSquares = gameState.dataArray[blankColMask, x]
    existingPossibilities = np.empty((1))
    for square in blankSquares:
        existingPossibilities = np.concatenate((existingPossibilities, square.possibilities))
    possibilities = np.setdiff1d(possibilities, square.possibilities)
    if len(possibilities)==1:
        print("solved at ",x, "," , y)
        gameState.dataArray[y,x].value = possibilities[0]
        gameState.gameArray[y,x] = possibilities[0]
        return

    #repeat for region
    regionX, regionY = GetTopLeftCornerOfRegion(x,y)
    blankRegionMask = gameState.gameArray[regionY:regionY+3,regionX:regionX+3] == 0
    region = gameState.dataArray[regionY:regionY+3, regionX:regionX+3]
    blankSquares = region[blankRegionMask]
    for square in blankSquares:
        existingPossibilities = np.concatenate((existingPossibilities, square.possibilities))
    possibilities = np.setdiff1d(possibilities, square.possibilities)
    if len(possibilities)==1:
        print("solved at ",x, "," , y)
        gameState.dataArray[y,x].value = possibilities[0]
        gameState.gameArray[y,x] = possibilities[0]
        return



#idea for an algorithm to solve
#do normal linear traversal to find first solve.
#from that check all blank spots in the column, row, region as they have a higher chance to being solvable after
#solving that one

def GetTopLeftCornerOfRegion(x,y):
    regionX =0
    regionY = 0
    if x < 3:
        regionX = 0
    elif x <6:
        regionX = 3
    else:
        regionX = 6
    if y < 3:
        regionY = 0
    elif y < 6:
        regionY = 3
    else:
        regionY = 6
    return regionX, regionY 

Game = GameState(hard)
SolveGame(Game)