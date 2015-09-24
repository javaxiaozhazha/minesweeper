import unittest

from pyramid import testing
from models import Cell, Game, Player
from services import GameService

class ViewTests(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()

    def tearDown(self):
        testing.tearDown()

    def test_my_view(self):
        from .views import my_view
        request = testing.DummyRequest()
        info = my_view(request)
        self.assertEqual(info['project'], 'minesweeper')

    def test_model_cell(self):
        """
        Test cell model works
        """
        cell = Cell()
        self.assertEqual(cell._isMine, False)
        self.assertEqual(cell._isRevealed, False)
        self.assertEqual(cell._isRevealed, False)
        self.assertEqual(cell._minesAround, 0)

        cell._isMine = True
        cell._isRevealed = True
        cell._isFlagged = True
        cell._minesAround = 8
        self.assertEqual(cell._isMine, True)
        self.assertEqual(cell._isRevealed, True)
        self.assertEqual(cell._isFlagged, True)
        self.assertEqual(cell._minesAround, 8)

    def test_model_game(self):
        game = Game(10, 10, 5)
        player = Player("player1", game)
        game.set_player(player)
        self.assertEqual(game._mines, [])
        self.assertEqual(game._result, 0)
        self.assertEqual(game._player._name, "player1")

    def test_game_services(self):
        gameService = GameService("player1")
        self.assertEqual(gameService._game._rows, 10)
        gameService.set_board()
        self.assertEqual(len(gameService._game._mines), 5)
        gameService.update_board_with_reveal(0, 0)
        self.assertEqual(gameService._game._board[0][0]._isRevealed, True)
        gameService.update_board_with_flag(1, 1)
        self.assertEqual(gameService._game._board[1][1]._isFlagged, True)
        self.assertEqual(gameService._game._result, 0)

