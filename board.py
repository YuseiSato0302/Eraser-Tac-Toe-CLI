from constants import ROWS, COLUMNS

class Board:
    def __init__(self):
        self.cells = {}
        for row in ROWS:
            for col in COLUMNS:
                position = f"{row}{col}"
                self.cells[position] = " "
                
    def display(self):
        # 盤面の表示
        print("    1   2   3")
        print("  +---+---+---+")
        for row in ROWS:
            row_cells = [self.cells[f"{row}{col}"] for col in COLUMNS]
            print(f"{row} | {' | '.join(row_cells)} |")
            print("  +---+---+---+")
            
    def update_cell(self, position, symbol):
        # 指定されたセルを更新
        self.cells[position] = symbol
        
    def is_cell_empty(self, position):
        # 指定されたセルが空か確認
        return self.cells.get(position, "X") == " "
    
    def get_empty_cells(self):
        # 空いているセルのリストを取得
        return [pos for pos, val in self.cells.items() if val == " "]