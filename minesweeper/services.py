from models import Cell, Game, Player
from random import randint
import json

class GameService:
    """
    GameService:
      Initialize game, Update game board and game status
    """
    def __init__(self, row, col, mines, players):
        self._game = Game(row, col, mines)
        self._players = []
        if players:
            for player in players:
                self._players.append(player)

    def add_player_to_game(self, players): #Enable multiple players
        if players:
            for player in players:
                self._game._players.append(player)
            self._game._current_player = players[0]

    def set_board(self):
        for row in range(self._game._rows):
            rowCells = []
            for col in range(self._game._cols):
                rowCells.append(Cell())
            self._game._board.append(rowCells)
        self._create_mines()
        self._init_cell()

    def _create_mines(self): #Create mines randomly
        while len(self._game._mines) < self._game._minesNumber:
            row = randint(0, self._game._rows-1)
            col = randint(0, self._game._cols-1)
            if (row, col) not in self._game._mines:
                self._game._board[row][col]._isMine = True
                self._game._mines.append((row, col))

    def _init_cell(self): #Set data, state for each cell
        for row in range(self._game._rows):
            for col in range(self._game._cols):
                number = 0
                for (x, y) in self._get_neighbors(row, col):
                    if self._game._board[x][y]._isMine:
                        number += 1
                self._game._board[row][col]._minesAround = number

    def _get_neighbors(self, row, col):
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
        """This method is called when left click a cell
        """
        cell = self._game._board[x][y]
        if not cell._isRevealed and not cell._isFlagged:
            if cell._isMine:
                self._game._result = -1
            elif cell._minesAround == 0:#means we need to update more cells
                self._update_neighbor_cells(x, y)
            cell._isRevealed = True
            self._update_game_status()

    def update_board_with_flag(self, x, y):
        """This method is called when right click a cell
        """
        if not self._game._board[x][y]._isRevealed:
            if self._game._board[x][y]._isFlagged:
                self._game._board[x][y]._isFlagged = False
            else:
                self._game._board[x][y]._isFlagged = True
        self._update_game_status()

    def _update_neighbor_cells(self, row, col): #Call this recursive method when a cell is revealed
        cell = self._game._board[row][col]
        if not cell._isRevealed:
            cell._isRevealed = True
            if cell._minesAround == 0:
                for (r, c) in self._get_neighbors(row, col):
                    ncell = self._game._board[r][c]
                    if not ncell._isRevealed and not ncell._isFlagged:
                        self._update_neighbor_cells(r, c)

    def _update_game_status(self):
        """Update game result
        """
        emptyCells = 0
        for rows in self._game._board:
            for cell in rows:
                if not cell._isRevealed or cell._isFlagged:
                    emptyCells += 1
        if emptyCells == self._game._minesNumber:
            self._game._result = 1

class Jsonify:
    """Transform data to Json according to front end requirements
    """
    @classmethod
    def to_board_view(cls, board, result):
        boardView=[]
        for rows in board:
            rowsView = []
            for cell in rows:
                if result is not 0 and cell._isMine:
                    rowsView.append(["X", True, cell._isFlagged])
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