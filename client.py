import websockets
import json

from board import Board

async def online_mode():
    # サーバーのアドレスとポート
    uri = "ws://localhost:8765"

    async with websockets.connect(uri) as websocket:
        while True:
            print("オンライン対戦メニュー：")
            print("1. ルームを作成する")
            print("2. ルームに参加する")
            print("3. 戻る")
            online_choice = input("選択肢を入力してください(1~3): ")

            if online_choice == "1":
                await create_room(websocket)
                await game_loop(websocket)
                break
            elif online_choice == "2":
                await join_room(websocket)
                await game_loop(websocket)
                break
            elif online_choice == "3":
                break  # メインメニューに戻る
            else:
                print("無効な入力です。もう一度選択してください。")

async def create_room(websocket):
    password = None
    set_password = input("パスワードを設定しますか？(y/n): ")
    if set_password.lower() == 'y':
        password = input("パスワードを入力してください：")

    request = {
        "type": "create_room_request",
        "data": {
            "password": password
        }
    }
    await websocket.send(json.dumps(request))

    response = await websocket.recv()
    data = json.loads(response)
    room_id = data["data"]["room_id"]
    password_set = data["data"]["password_set"]

    print(f"ルームを作成しました。ルーム番号：{room_id}")
    if password_set:
        print("パスワードが設定されています。")

async def join_room(websocket):
    room_id = input("ルーム番号を入力してください：")

    request = {
        "type": "join_room_request",
        "data": {
            "room_id": room_id
        }
    }
    await websocket.send(json.dumps(request))

    response = await websocket.recv()
    data = json.loads(response)

    if not data["data"]["success"]:
        if data["data"]["message"] == "パスワードが必要です。":
            password = input("パスワードを入力してください：")
            request["data"]["password"] = password
            await websocket.send(json.dumps(request))
            response = await websocket.recv()
            data = json.loads(response)

    if data["data"]["success"]:
        print("ルームに参加しました")
    else:
        print(f"ルームに参加できませんでした：{data['data']['message']}")
        # ルーム参加に失敗した場合、オンライン対戦メニューに戻る
        return await online_mode()

async def game_loop(websocket):
    # ゲーム進行を管理するループ
    player_symbol = None
    board = Board()
    try:
        while True:
            response = await websocket.recv()
            data = json.loads(response)
            message_type = data.get("type")
            payload = data.get("data")

            if message_type == "game_start":
                print(payload["message"])
                player_symbol = payload["player_symbol"]
                print(f"あなたのシンボルは '{player_symbol}' です")
            elif message_type == "game_update":
                board.cells = payload["board"]
                current_turn_symbol = payload["current_turn"]
                board.display()
                if current_turn_symbol == player_symbol:
                    print("あなたの手番です")
                    position = await get_player_move(websocket, board)
                    if position == 'q':
                        await forfeit_game(websocket)
                        break
                else:
                    print("相手の手番です。お待ちください。")
            elif message_type == "game_over":
                board.display()
                result = payload["result"]
                if result == "win":
                    print("あなたの勝ちです！")
                elif result == "lose":
                    print("あなたの負けです。")
                else:
                    print("引き分けです。")
                break
    except websockets.exceptions.ConnectionClosed:
        print("サーバーとの接続が切れました。ゲームを終了します。")

async def get_player_move(websocket, board):
    while True:
        move = input("マスを選択してください（棄権する場合は 'q' を入力）: ")
        if move.lower() == 'q':
            return 'q'
        if move in board.cells and board.is_cell_empty(move):
            request = {
                "type": "move",
                "data": {
                    "position": move
                }
            }
            await websocket.send(json.dumps(request))
            return move
        else:
            print("無効な入力です。もう一度入力してください。")

async def forfeit_game(websocket):
    request = {
        "type": "forfeit",
        "data": {}
    }
    await websocket.send(json.dumps(request))
    print("あなたは棄権しました。ゲームを終了します。")
