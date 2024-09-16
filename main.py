import subprocess
import sys
import signal
from utils import play_bgm, stop_bgm
from game import Game

# グローバル変数としてBGMプロセスを保持
title_bgm_process = None
game_bgm_process = None

def display_title():
    # タイトルを表示します
    title_text = "Tic Tac Toe"
    result = subprocess.run(["figlet", title_text], stdout=subprocess.PIPE)
    print(result.stdout.decode())
    
def main_menu():
    # メインメニューを表示してユーザーの選択を受け付ける
    print("ゲームモードを選択してください：")
    print("1. 2人プレイ")
    print("2. CPU対戦(現在開発中)")
    print("3. オンライン対戦(現在開発中)")
    print("4. 終了")
    print("")
    choice = input("選択肢を入力してください(1~4) :")
    return choice

def signal_handler(sig, frame):
    # Ctrl+C でプログラムを終了
    if title_bgm_process is not None:
        stop_bgm(title_bgm_process)
    if game_bgm_process is not None:
        stop_bgm(game_bgm_process)
    print("\nプログラムを終了します。")
    sys.exit(0)

if __name__ == "__main__":
    # シグナルハンドラを登録
    signal.signal(signal.SIGINT, signal_handler) # Ctrl+C
    signal.signal(signal.SIGTERM, signal_handler) # 終了要求
    
    try:
        while True:
            # タイトル画面用BGMを再生
            title_bgm_process = play_bgm("assets/title_bgm.mp3") 
            
            display_title()
            choice = main_menu()
            
            # タイトル用BGMを停止
            stop_bgm(title_bgm_process)
            title_bgm_process = None
            
            if choice == "1":
                # ゲーム用BGMを再生
                game_bgm_process = play_bgm("assets/game_bgm.mp3")
                
                game = Game()
                game.start()
                
                # ゲーム終了後BGMを停止
                stop_bgm(game_bgm_process)
                game_bgm_process = None
                
                # 再戦するかどうかの確認
                replay_choice = input("もう一度プレイしますか？(y/n): ")
                if replay_choice.lower() != "y":
                    print("ゲームを終了します。")
                    break # ゲームを終了
            elif choice == "2" or choice == "3":
                print("このモードは現在開発中です。")
                input("タイトル画面に戻るためにはEnterキーを押してください。")
                continue  # メインメニューに戻る
            elif choice == "4":
                print("ゲームを終了します。")
                break # ゲームを終了
            else:
                print("無効な入力です。もう一度選択してください。")
                input("タイトル画面に戻るためにはEnterキーを押してください。")
    
    finally:
        # プログラム終了時に BGM プロセスを確実に停止
        if title_bgm_process is not None:
            stop_bgm(title_bgm_process)
        if game_bgm_process is not None:
            stop_bgm(game_bgm_process)    
            
            