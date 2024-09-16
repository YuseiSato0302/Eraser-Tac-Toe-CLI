import sys
import os
sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), '..')
    )
)

import unittest
from player import Player
from board import Board

class TestPlayer(unittest.TestCase):
    def setUp(self):
        self.board = Board()
        self.player = Player("Test Player", 'X')

    def test_make_move(self):
        """プレイヤーがコマを配置できるかをテスト"""
        # ユーザー入力をモック
        input_values = ['a1']

        def mock_input(_):
            return input_values.pop(0)

        original_input = __builtins__.input
        __builtins__.input = mock_input

        self.player.make_move(self.board)
        __builtins__.input = original_input

        self.assertEqual(self.board.cells['a1'], 'X')
        self.assertIn('a1', self.player.moves)

    def test_remove_oldest_move(self):
        """古いコマが正しく削除されるかをテスト"""
        moves = ['a1', 'a2', 'a3', 'b1']
        for move in moves:
            self.board.update_cell(move, self.player.symbol)
            self.player.moves.append(move)
            if len(self.player.moves) > 3:
                self.player.remove_oldest_move(self.board)

        self.assertEqual(self.board.cells['a1'], ' ')
        self.assertEqual(len(self.player.moves), 3)
        self.assertNotIn('a1', self.player.moves)

if __name__ == '__main__':
    unittest.main()
