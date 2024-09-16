import subprocess
import os
from constants import ROWS, COLUMNS

def validate_input(input_str):
    # ユーザーの入力が有効か検証
    input_str = input_str.lower().strip()
    if len(input_str) != 2:
        return False
    row, col = input_str[0], input_str[1]
    return row in ROWS and col in COLUMNS

def play_bgm(file_path):
    # バックグラウンドでBGMを再生
    if not os.path.exists(file_path):
        print(f"警告：BGMファイルが見つかりません({file_path})。BGMなしでゲームを開始します。")
        return None
    try:
        return subprocess.Popen(["mpg123", "-q", "--loop", "-1", file_path])
    except FileNotFoundError:
        print("エラー：mpg123がインストールされていません。'sudo apt-get install mpg123'でインストールしてください。")
        return None
    
def stop_bgm(process):
    # BGMを停止
    if process:
        process.terminate()