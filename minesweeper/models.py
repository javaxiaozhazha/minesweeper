
class Cell:
    """
    Cell class to represent a cell in the game board

    It stores all data(markers, states) of a cell
    """
    def __init__(self):
        self._isMine = False #the cell is a mine or not
        self._isRevealed = False #the cell is revealed by player or not
        self._isFlagged = False #the cell is flagged by player or not
        self._minesAround = 0 #the mines around current cell [0, 8] (upper left, upper, upper right, left, right, down left, down, down right)

class Game:
    """
    Game class represent a game board
    Game holds a board of 2D cells, and all states (game done or game ongoing...)
    """
    def __init__(self, rows, cols, minesNumber):
        self._rows = rows
        self._cols =cols
        self._minesNumber = minesNumber #The number of mines the board holds
        self._board = [] #The size of this board should be rows*cols
        self._mines = [] #A list of cells which are mines
        self._result = 0 #Game result [0:game ongoing, 1:player win, -1: player lose]
        self._start_time = ""
        self._end_time = ""

class Player:
    """
    Player: every player has their game history, current game status
    """
    def __init__(self, name):
        self._history = []
        self._name = name
