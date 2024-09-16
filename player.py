from utils import validate_input

class Player:
    def __init__(self, name, symbol):
        self.name = name
        self.symbol = symbol
        self.moves = []
        
    def make_move(self, board):
        # プレイヤーがコマを配置する
        while True:
            position = input(f"プレイヤー{self.symbol}の番です。コマを置く位置を入力してください(e.g. a1) :").lower().strip()
            if not validate_input(position):
                print("無効な入力です。もう一度入力してください。")
                continue
            if not board.is_cell_empty(position):
                print("そのセルには既にコマが置かれています。別の位置を入力してください。")
                continue
            board.update_cell(position, self.symbol)
            self.moves.append(position)
            if len(self.moves) > 3:
                self.remove_oldest_move(board)
            break
        
    def remove_oldest_move(self, board):
        # プレイヤーの最も古いコマを削除
        oldest_move = self.moves.pop(0)
        board.update_cell(oldest_move, " ")
        
    #TODO 将来的なAIプレイヤーのクラス(未実装)
    class AIPlayer(Player):
        def make_move(self, board):
            pass
    