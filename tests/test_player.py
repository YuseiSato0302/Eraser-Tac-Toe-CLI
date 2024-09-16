import unittest
from unittest.mock import patch
from player import Player
from board import Board

class TestPlayer(unittest.TestCase):
    def setUp(self):
        self.board = Board()
        self.player = Player("Test Player", 'X')

    @patch('builtins.input', side_effect=['a1'])
    def test_make_move(self, mock_input):
        """プレイヤーがコマを配置できるかをテスト"""
        self.player.make_move(self.board)
        self.assertEqual(self.board.cells['a1'], 'X')
        self.assertIn('a1', self.player.moves)

if __name__ == '__main__':
    unittest.main()
