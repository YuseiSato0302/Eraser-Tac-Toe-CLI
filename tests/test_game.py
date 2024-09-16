import sys
import os
sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), '..')
    )
)

import unittest
from game import Game

class TestGame(unittest.TestCase):
    def setUp(self):
        self.game = Game()
        self.game.max_turns = 5  # テスト用に小さい値を設定

    def test_check_winner(self):
        """勝利条件の判定をテスト"""
        b = self.game.board
        b.update_cell('a1', 'X')
        b.update_cell('a2', 'X')
        b.update_cell('a3', 'X')
        self.assertTrue(self.game.check_winner())

    def test_is_draw(self):
        """最大ターン数による引き分けをテスト"""
        self.game.turn_count = 5
        self.assertTrue(self.game.is_draw())

if __name__ == '__main__':
    unittest.main()
