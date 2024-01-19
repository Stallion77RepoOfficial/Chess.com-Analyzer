import websocket
import json
import threading

user_pgn = input("Lütfen PGN hamlelerinizi girin: ")

ws_url = "wss://analysis.chess.com/"

request_data = {
    "action": "gameAnalysis",
    "game": {"pgn": user_pgn},
    "options": {
        "caps2": True,
        "depth": 18,
        "engineType": "stockfish16 nnue",
        "source": {
            "gameId": "",
            "gameType": "",
            "url": "",
            "token": "", 
            "client": "web",
            "userTimeZone": "Europe/Istanbul"
        },
        "strength": "Fast",
        "tep": {
            "ceeDebug": False,
            "classificationv3": True,
            "lang": "tr_TR",
            "speechv3": True
        }
    }
}

def on_message(ws, message):
    print("Bir mesaj alındı...")
    with open("response.txt", "a") as f:
        f.write(message + "\n")
    response_data = json.loads(message)
    if "progress" in response_data and response_data["progress"] >= 1:
        print("Analiz tamamlandı.")
        ws.close()

def on_error(ws, error):
    print(f"Hata: {error}")

def on_close(ws, close_status_code, close_msg):
    print("### Bağlantı kapandı ###")

def on_open(ws):
    def run(*args):
        ws.send(json.dumps(request_data))
        print("İstek gönderildi...")
    threading.Thread(target=run).start()

if __name__ == "__main__":
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp(ws_url,
                              on_open=on_open,
                              on_message=on_message,
                              on_error=on_error,
                              on_close=on_close)

    ws.run_forever()
