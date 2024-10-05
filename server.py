# インポート群
import hashlib
import json
import random
import string
import websockets

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
        "board": [" "]*9,
        "current_turn": client_id,
        "game_over": False
    }
    
    clients[client_id]["room_id"] = room_id
    clients[client_id]["player_symbol"] = "x"
    
    response = {
        "type": "create_room_response",
        "data": {
            "room_id": room_id,
            "password_set": bool(password)
        }
    }
    await websocket.send(json.dumps(response))