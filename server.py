import asyncio
import hashlib
import json
import random
import string
import websockets
from board import Board
from constants import PLAYER_SYMBOLS

# ルーム情報を保持
rooms = {}

# クライアントごとの接続情報を保持
clients = {}

async def handler(websocket, path):
    # クライアントを識別するためのIDを生成
    client_id = id(websocket)
    clients[client_id] = {
        "websocket": websocket,
        "room_id": None,
        "player": None
    }
    try:
        async for message in websocket:
            data = json.loads(message)
            message_type = data.get("type")
            payload = data.get("data")
            
            if message_type == "create_room_request":
                await create_room(websocket, client_id, payload)
            elif message_type == "join_room_request":
                await join_room(websocket, client_id, payload)
            elif message_type == "move":
                await handle_move(client_id, payload)
            elif message_type == "forfeit":
                await handle_forfeit(client_id)
                
    except websockets.exceptions.ConnectionClosed:
        print(f"クライアント{client_id}が接続を切断しました。")
        await handle_disconnect(client_id)
        
async def create_room(websocket, client_id, payload):
    # 4桁のランダムなルームIDを生成
    while True:
        room_id = ''.join(random.choices(string.digits, k=4))
        if room_id not in rooms:
            break
        
    password = payload.get("password")
    password_hash = hashlib.sha256(password.encode()).hexdigest() if password else None
    
    # ルーム情報を作成
    rooms[room_id] = {
        "players": [client_id],
        "password": password_hash,
        "board": Board(),
        "current_turn": client_id,
        "game_over": False
    }
    
    clients[client_id]["room_id"] = room_id
    clients[client_id]["player_symbol"] = PLAYER_SYMBOLS[0] 
    
    response = {
        "type": "create_room_response",
        "data": {
            "room_id": room_id,
            "password_set": bool(password)
        }
    }
    await websocket.send(json.dumps(response))
    print(f"ルーム{room_id}が作成されました。")
    
async def join_room(websocket, client_id, paylaod):
    room_id = paylaod.get("room_id")
    password = paylaod.get("password")
    
    if room_id not in rooms:
        response = {
            "type": "join_room_response",
            "data": {
                "success": False,
                "message": "指定されたルームが見つかりません。"
            }
        }
        await websocket.send(json.dumps(response))
        return
    
    room = rooms[room_id]
    
    # パスワードの確認
    if room["password"]:
        if not password:
            response = {
                "type": "join_room_response",
                "data": {
                    "success": False,
                    "message": "パスワードが必要です。"
                }
            }
            await websocket.send(json.dumps(response))
            return
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        if password_hash != room["password"]:
            response = {
                "type": "join_room_response",
                "data": {
                    "success": False,
                    "message": "パスワードが間違っています。"
                }
            }
            await websocket.send(json.dumps(response))
            return
        
    # プレイヤーを追加
    if len(room["players"]) >= 2:
        response = {
            "type": "join_room_response",
            "data": {
                "success": False,
                "message": "このルームは満員です。"
            }
        }
        await websocket.send(json.dumps(response))
        return
    
    room["players"].append(client_id)
    clients[client_id]["room_id"] = room_id
    clients[client_id]["player_symbol"] = PLAYER_SYMBOLS[1]
    
    response = {
        "type": "join_room_response",
        "data": {
            "success": True,
            "message": "ルームに参加しました"
        }
    }
    await websocket.send(json.dumps(response))
    print(f"プレーヤー{client_id}がルーム{room_id}に参加しました。")
    
    # ゲーム開始の通知
    await start_game(room_id)
    
async def start_game(room_id):
    room = rooms[room_id]
    for player_id in room["players"]:
        websocket = clients[player_id]["websocket"]
        response = {
            "type": "game_start",
            "data": {
                "message": "ゲームを開始します",
                "player_symbol": clients[player_id]["player_symbol"]
            }
        }
        await websocket.send(json.dumps(response))
    print(f"ルーム{room_id}でゲームを開始します。")
    # 最初のゲーム状態を送信
    await send_game_update(room_id)
    
async def handle_move(client_id, payload):
    position = payload.get("position")
    room_id = clients[client_id]["room_id"]
    room = rooms.get(room_id)
    
    if room is None or room["game_over"]:
        return
    
    if room["current_turn"] != client_id:
        return
    
    board = room["board"]    
    symbol = clients[client_id]["player_symbol"]
    
    # 無効な手の場合は何もしない
    if not board.is_cell_empty(position):
        return 
    
    board.update_cell(position, symbol)
    
    # 勝敗判定
    winner = check_winner(board)
    if winner or not board.get_empty_cells():
        room["game_over"] = True
        await send_game_over(room_id, winner)
        return 
    
    # 手番の交代
    other_player_id = [pid for pid in room["players"] if pid != client_id][0]
    room["current_turn"] = other_player_id
    
    # ゲーム状態の更新を送信
    await send_game_update(room_id)
    
async def send_game_update(room_id):
    room = rooms[room_id]
    board = room["board"]
    for player_id in room["players"]:
        websocket = clients[player_id]["websocket"]
        response = {
            "type": "game_update",
            "data": {
                "board": board.cells,
                "current_turn": clients[room["current_turn"]]["player_symbol"]
            }
        }
        await websocket.send(json.dumps(response))
        
async def send_game_over(room_id, winner_symbol):
    room = rooms[room_id]
    for player_id in room["players"]:
        websocket = clients[player_id]["websocket"]
        player_symbol = clients[player_id]["player_symbol"]
        if winner_symbol == player_symbol:
            result = "win"
        elif winner_symbol is None:
            result = "draw"
        else:
            result = "lose"
        response = {
            "type": "game_over",
            "data": {
                "result": result
            }
        }
        await websocket.send(json.dumps(response))
        
    # ゲーム終了後、ルームを削除
    del rooms[room_id]
    print(f"ルーム{room_id}を削除しました。")
    
def check_winner(board):
    winning_patterns = [
        ['a1', 'a2', 'a3'],
        ['b1', 'b2', 'b3'],
        ['c1', 'c2', 'c3'],
        ['a1', 'b1', 'c1'],
        ['a2', 'b2', 'c2'],
        ['a3', 'b3', 'c3'],
        ['a1', 'b2', 'c3'],
        ['a3', 'b2', 'c1']
    ]
    for pattern in winning_patterns:
        symbols = [board.cells[pos] for pos in pattern]
        if symbols[0] != ' ' and symbols.count(symbols[0]) == 3:
            return symbols[0]
    return None

async def handle_forfeit(client_id):
    room_id = clients[client_id]["room_id"]
    room = rooms.get(room_id)

    if room is None:
        return
    
    room["game_over"] = True
    other_player_id = [pid for pid in room["players"] if pid != client_id][0]
    
    # 棄権したプレイヤーには敗北を通知
    webocket = clients[client_id]["websocket"]
    response = {
        "type": "game_over",
        "data": {
            "result": "lose"
        }
    }
    await websockets.send(json.dumps(response))
    
    # 相手プレイヤーには勝利を通知
    websocket = clients[other_player_id]["websocket"]
    response = {
        "type": "game_over",
        "data": {
            "result": "win"
        }
    }
    await websocket.send(json.dumps(response))
    
    # ゲーム終了後、ルームを削除
    del rooms[room_id]
    print(f"クライアント{client_id}が棄権したため、ルーム{room_id}を削除します。")
    
async def handle_disconnect(client_id):
    # クライアントの接続所法を削除
    client_info = clients.get(client_id)
    if client_info:
        room_id = client_info.get("room_id")
        if room_id and room_id in rooms:
            await handle_forfeit(client_id)
        del clients[client_id]
    print(f"クライアント{client_id}の接続情報を削除しました。")
        
async def main():
    async with websockets.serve(handler, "localhost", 8765):
        print("サーバーを起動しました。")
        await asyncio.Future() # 永久ループ
        
if __name__ == "__main__":
    asyncio.run(main())