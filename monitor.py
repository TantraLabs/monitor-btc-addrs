import websocket
import json

def on_message(ws, message):
    message = json.loads(message) 
    if 'x' in message:
        from_addr = message['x']['inputs'][0]['prev_out']['addr']
        to_addr = message['x']['out'][0]['addr']
        value = message['x']['out'][0]['value'] # might need to change units
        hash = message['x']['hash']
        print(f"""
        To: {to_addr}
        From: {from_addr}
        Value: {value}
        Hash: {hash}
        """)
    else:
        print(message)

def on_error(ws, error):
    print(error)

def on_close(ws):
    print("### connection closed ###")

def on_open(ws):
    # to ping
    ws.send(json.dumps({"op":"ping"}))

    # enable to see unconfirmed txs in real-time
    # ws.send(json.dumps({"op":"unconfirmed_sub"}))

    def run(btc_addr):
        
        ws.send(json.dumps({"op":"addr_sub", "addr":f"{btc_addr}"}))
        print(f"Monitoring started for this btc addr: {btc_addr}")

    with open("input.txt") as f:
        addrs = f.readlines()

    if len(addrs)>0:
        for addr in addrs:
            if addr.strip() != "":
                run(addr)

if __name__ == "__main__":
    # websocket.enableTrace(True)
    ws = websocket.WebSocketApp("wss://ws.blockchain.info/inv",
                              on_open = on_open,
                              on_message = on_message,
                              on_error = on_error,
                              on_close = on_close)

    ws.run_forever()