from models import Cell, Game, Player
from random import randint
import json

class GameService:
    """
    GameService:
      Initialize game, Update game board and game status
    """

    def __init__(self, name):
        self._player = Player
        self._game = Game(10, 10, 5)
        self._player = Player(name, self._game)
        self._game.set_player(self._player)

    def set_board(self):
        for row in range(self._game._rows):
            rowCells = []
            for col in range(self._game._cols):
                rowCells.append(Cell())
            self._game._board.append(rowCells)
        self.create_mines()
        self.init_cell()

    def create_mines(self): #Create mines randomly
        while len(self._game._mines) < self._game._minesNumber:
            row = randint(0, self._game._rows - 1)
            col = randint(0, self._game._cols - 1)
            if (row,col) not in self._game._mines:
                self._game._board[row][col]._isMine = True
                self._game._mines.append((row,col))

    def init_cell(self):
        for row in range(self._game._rows):
            for col in range(self._game._cols):
                number = 0
                for (x, y) in self.get_neighbors(row, col):
                    if self._game._board[x][y]._isMine:
                        number += 1
                self._game._board[row][col]._minesAround = number

    def get_neighbors(self, row, col):
        neighborCells = []
        eightNeighbors = [(row-1, col-1), (row-1, col), (row-1, col+1),
                          (row, col-1), (row, col+1),
                          (row+1, col-1), (row+1, col), (row+1, col+1),
                          ]
        for (x, y) in eightNeighbors:
            if 0 <= x < self._game._rows and 0 <= y < self._game._cols:
                neighborCells.append((x, y))
        return neighborCells

    def update_board_with_reveal(self, x, y):
        """
        This method is called when left click a cell
        """
        cell = self._game._board[x][y]
        if not cell._isRevealed and not cell._isFlagged:
            if cell._isMine:
                self._game._result = -1
            elif cell._minesAround == 0:#means we need to update more cells
                self.update_neighbor_cells(x, y)
            cell._isRevealed = True
            self.update_game_status()

    def update_board_with_flag(self, x, y):
        """
        This method is called when right click a cell
        """
        if self._game._board[x][y]._isFlagged:
            self._game._board[x][y]._isFlagged = False
        else:
            self._game._board[x][y]._isFlagged = True
        self.update_game_status()

    def update_neighbor_cells(self, row, col): #Call this method when a cell is revealed
        cell = self._game._board[row][col]
        if not cell._isRevealed:
            cell._isRevealed = True
            if cell._minesAround == 0:
                for (r, c) in self.get_neighbors(row, col):
                    ncell = self._game._board[r][c]
                    if not ncell._isRevealed and not ncell._isFlagged:
                        self.update_neighbor_cells(r, c)

    def update_game_status(self):
        """
        Update game state
        """
        emptyCells = 0
        for rows in self._game._board:
            for cell in rows:
                if cell._isRevealed == False or cell._isFlagged:
                    emptyCells += 1
        if emptyCells == self._game._minesNumber:
            self._game._result = 1

class Jsonify:
    """
    Transform data to json according to requirements from Views
    """
    @classmethod
    def to_board_view(cls, board, result):
        boardView=[]
        for rows in board:
            rowsView = []
            for cell in rows:
                if result is not 0 and cell._isMine:
                    rowsView.append(["X", True, cell.isFlagged()])
                else:
                    if cell._isRevealed:
                        if cell._minesAround>0:
                            rowsView.append([cell._minesAround,True, cell._isFlagged])
                        else:
                            rowsView.append(["", True, cell._isFlagged])
                    else:
                        rowsView.append(["", False, cell._isFlagged])
            boardView.append(rowsView)
        return json.loads(json.dumps(boardView, default=lambda o: o.__dict__))

    @classmethod
    def to_mines_view(cls, board):
        """
        Show the board with all mines revealed
        :param board:
        :return:
        """
        boardView = []
        for rows in board:
            rowsView = []
            for cell in rows:
                if cell._isMine:
                    rowsView.append("X")
                else:
                    rowsView.append("")
            boardView.append(rowsView)
        return json.loads(json.dumps(boardView, default=lambda o: o.__dict__))

    @classmethod
    def to_mines_number_view(cls, board):
        """
        Show the board with each cell show the number of mines around it
        :param board:
        :return:
        """
        boardView = []
        for rows in board:
            rowsView = []
            for cell in rows:
                if cell._minesAround>0:
                    rowsView.append(cell._minesAround)
                else:
                    rowsView.append("")
            boardView.append(rowsView)
        return json.loads(json.dumps(boardView, default=lambda o: o.__dict__))