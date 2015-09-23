import unittest

from pyramid import testing
from models import Cell, Game

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

    def test_model_board(self):
        game = Game(10, 10, 5)
        self.assertEqual(game._mines, [])
        self.assertEqual(game._result, 0)