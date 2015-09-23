
class Cell:
    """
    Cell class to represent a cell in the game board

    It stores all data(markers, states) of a cell
    """
    def __init__(self):
        self.__isMine = False #the cell is a mine or not
        self.__isRevealed = False #the cell is revealed by player or not
        self.__isFlagged = False #the cell is flagged by player or not
        self.__minesAround = 0 #the mines around current cell [0, 8] (upper left, upper, upper right, left, right, down left, down, down right)

    def is_mine(self):
        return self.__isMine

    def set_mine(self):
        self.__isMine = True

    def unset_mine(self):
        self.__isMine = False

    def is_revealed(self):
        return self.__isRevealed

    def set_revealed(self):
        self.__isRevealed = True

    def unset_revealed(self):
        self.__isRevealed = False

    def is_flagged(self):
        return self.__isFlagged

    def set_flagged(self):
        self.__isFlagged = True

    def unset_flagged(self):
        self.__isFlagged = False

    def get_mines_around(self):
        return self.__minesAround

    def set_mines_around(self, mines_around):
        self.__minesAround = mines_around