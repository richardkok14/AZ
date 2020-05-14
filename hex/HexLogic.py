'''
Board class for the game of Hex.
Default board size is 3x3.
Board data:
  1=RED, -1=BLUE, 0=empty
  first dim is column , 2nd is row:
     pieces[0][0] is the top left square,
     pieces[2][0] is the bottom left square,
Squares are stored and manipulated as (x,y) tuples.

Author: Richard Kok
Date: May 2020.

Based on the board for the game of Othello by Eric P. Nichols.

'''
# from bkcharts.attributes import color
class Board():

    RED = 1
    BLUE = -1
    # list of all 8 directions on the board, as (x,y) offsets
    __directions = [(1,1),(1,0),(1,-1),(0,-1),(-1,-1),(-1,0),(-1,1),(0,1)]
    def __init__(self, n=3):
        "Set up initial board configuration."

        self.n = n
        # Create the empty board array.
        self.pieces = [None]*self.n
        for i in range(self.n):
            self.pieces[i] = [0]*self.n

    # add [][] indexer syntax to the Board
    def __getitem__(self, index): 
        return self.pieces[index]
    def is_color(self, coord, color):
        (y,x) = coord
        return self[y][x] == color
    def get_legal_moves(self):
        """Returns all the legal moves.
        """
        moves = set()  # stores the legal moves.

        # Get all the empty squares (color==0)
        for y in range(self.n):
            for x in range(self.n):
                if self[y][x]==0:
                    newmove = (y,x)
                    moves.add(newmove)
        return list((moves))

    def has_legal_moves(self):
        for y in range(self.n):
            for x in range(self.n):
                if self[y][x]==0:
                    return True
        return False
    def get_neighbors(self, coordinates):
        (cy,cx) = coordinates
        neighbors = []
        if cx-1>=0:   neighbors.append((cy,cx-1))
        if cx+1<self.n: neighbors.append((cy,cx+1))
        if cx-1>=0    and cy+1<=self.n-1: neighbors.append((cy+1,cx-1))
        if cx+1<self.n  and cy-1>=0: neighbors.append((cy-1,cx+1))
        if cy+1<self.n: neighbors.append((cy+1,cx))
        if cy-1>=0:   neighbors.append((cy-1,cx))
        return neighbors
    def border(self, color, move):
        (ny, nx) = move
        return (color == self.BLUE and nx == self.n-1) or (color == self.RED and ny == self.n-1)
    def traverse(self, color, move, visited):
        if not self.is_color(move, color) or (move in visited and visited[move]): return False
        if self.border(color, move): return True
        visited[move] = True
        for n in self.get_neighbors(move):
          if self.traverse(color, n, visited): return True
        return False
    def is_win(self, color):
        for i in range(self.n):
          if color == self.BLUE: move = (i,0)
          else: move = (0,i)
          if self.traverse(color, move, {}):
            return True
        return False

    def execute_move(self, move, color):
        """Perform the given move on the board; 
        color gives the color pf the piece to play (1=red,-1=blue)
        """

        (y,x) = move

        # Add the piece to the empty square.
        assert self[y][x] == 0
        self[y][x] = color

