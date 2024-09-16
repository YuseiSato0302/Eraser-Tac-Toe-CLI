from board import Board
from player import Player
from constants import PLAYER_SYMBOLS

class Game:
    def __init__(self):
        self.board = Board()
        self.players = [
            Player("Player 1", PLAYER_SYMBOLS[0]),
            Player("Player 2", PLAYER_SYMBOLS[1])
        ]
        self.current_player_index = 0
        self.winner = None
        self.turn_count = 0 # ターン数をカウント
        self.max_turns = 50 # 最大ターン数
        
        
    def switch_player(self):
        # プレイヤーを切り替え
        self.current_player_index = 1 - self.current_player_index
        
    def check_winner(self):
        # 勝者がいるかチェック
        b = self.board.cells
        s = self.current_player().symbol
        win_patterns = [
            ['a1', 'a2', 'a3'],
            ['b1', 'b2', 'b3'],
            ['c1', 'c2', 'c3'],
            ['a1', 'b1', 'c1'],
            ['a2', 'b2', 'c2'],
            ['a3', 'b3', 'c3'],
            ['a1', 'b2', 'c3'],
            ['a3', 'b2', 'c1'],
        ]
        for pattern in win_patterns:
            if all(b[pos] == s for pos in pattern):
                self.winner = self.current_player()
                return True
        return False
    
    def is_draw(self):
        # 引き分けかどうかチェック
        return self.turn_count >= self.max_turns
    
    def current_player(self):
        # 現在のプレイヤーを取得
        return self.players[self.current_player_index]
    
    def start(self):
        # ゲームを開始
        while True:
            self.board.display()
            player = self.current_player()
            player.make_move(self.board)
            self.turn_count += 1 # ターン数を増加
            
            if self.check_winner():
                self.board.display()
                print(f"勝者：{self.winner.name}")
                break
            
            if self.is_draw():
                self.board.display()
                print("引き分け")
                break
            
            self.switch_player()