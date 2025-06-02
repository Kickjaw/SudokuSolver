import numpy as np



class GameState:
    def __init__(self):
      self.solved = False
      self.game = np.array((9,9), dtype=object)

    def LoadGame(self, array):
        for y in range(9):
            for x in range (9):
                self.game[y,x] = Square(x,y)

    def SolveGame(self):
        solved = False
        while solved != False:
            for y in range(9):
                for x in range(9):
                    if self.game[y,x].solved != False:
                       solve= 1 


class Square:
    def __init__(self, x, y, value):
      self.x = x 
      self.y = y
      self.solved = False
      self.value = value
      self.possible = []