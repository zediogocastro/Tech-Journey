import asyncio
import websockets
import random
import json

async def stock_price(websocket):
    print("Client connected")
    try:
        while True:
            price = round(random.uniform(100, 200), 2)
            message = json.dumps({"symbol": "AAPL", "price": price})
            await websocket.send(message)
            await asyncio.sleep(3)
    except websockets.ConnectionClosed:
        print("Client disconnected")

async def run_server():
    async with websockets.serve(stock_price, "0.0.0.0", 8765):
        print("WebSocket server started on ws://localhost:8765")
        await asyncio.Future()  # Run forever

# 🔁 This is the sync wrapper for Poetry
def main():
    asyncio.run(run_server())