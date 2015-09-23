import unittest

from pyramid import testing
from models import Cell, Board

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
        self.assertEqual(cell.is_mine(), False)
        self.assertEqual(cell.is_revealed(), False)
        self.assertEqual(cell.is_flagged(), False)
        self.assertEqual(cell.get_mines_around(), 0)

        cell.set_flagged()
        cell.set_revealed()
        cell.set_mine()
        cell.set_mines_around(8)
        self.assertEqual(cell.is_mine(), True)
        self.assertEqual(cell.is_revealed(), True)
        self.assertEqual(cell.is_flagged(), True)
        self.assertEqual(cell.get_mines_around(), 8)

    def test_model_board(self):
        board = Board(10, 10, 5)
        self.assertEqual(board.get_mines(), [])
        self.assertEqual(board.get_result(), 0)