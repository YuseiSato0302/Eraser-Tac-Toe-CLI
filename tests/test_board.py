import sys
import os
sys.path.append(
    os.path.abspqth(
        os.path.join(os.path.dirname(__file__), "..")
    )
)

import unittest
from board import Board

class TestBoard(unittest.TestCase):
    def setUp(self):
        self.board = Board()

    def test_board_initialization(self):
        """盤面が正しく初期化されているかをテスト"""
        for cell in self.board.cells.values():
            self.assertEqual(cell, ' ')

    def test_update_cell(self):
        """セルの更新が正しく行われるかをテスト"""
        self.board.update_cell('a1', 'X')
        self.assertEqual(self.board.cells['a1'], 'X')

    def test_is_cell_empty(self):
        """セルが空かどうかの判定をテスト"""
        self.assertTrue(self.board.is_cell_empty('a2'))
        self.board.update_cell('a2', 'O')
        self.assertFalse(self.board.is_cell_empty('a2'))

if __name__ == '__main__':
    unittest.main()