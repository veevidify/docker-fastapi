from typing import List

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse

class ConnManager:
    def __init__(self):
        self.active_ws_conns: List[WebSocket] = []

    async def connect(self, ws: WebSocket):
        await ws.accept()
        self.active_ws_conns.append(ws)

    def disconnect(self, ws: WebSocket):
        self.active_ws_conns.remove(ws)

    async def send_msg(self, msg: str, ws: WebSocket):
        await ws.send_text(msg)

    async def broadcast(self, msg: str):
        # send sequentially
        for conn in self.active_ws_conns:
            await conn.send_text(msg)

static_html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>WebSocket Chat</h1>
        <h2>Your ID: <span id="ws-id"></span></h2>
        <form action="" onsubmit="sendMessage(event)">
            <input type="text" id="messageText" autocomplete="off"/>
            <button>Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
            var client_id = Date.now()
            document.querySelector("#ws-id").textContent = client_id;
            var ws = new WebSocket(`ws://localhost:8000/ws/${client_id}`);
            ws.onmessage = function(event) {
                var messages = document.getElementById('messages')
                var message = document.createElement('li')
                var content = document.createTextNode(event.data)
                message.appendChild(content)
                messages.appendChild(message)
            };
            function sendMessage(event) {
                var input = document.getElementById("messageText")
                ws.send(input.value)
                input.value = ''
                event.preventDefault()
            }
        </script>
    </body>
</html>
"""

manager = ConnManager()
app = FastAPI()

@app.get("/")
async def root():
    return HTMLResponse(static_html)

@app.websocket("/ws/{client_id}")
async def ws_controller(ws: WebSocket, client_id: int):
    await manager.connect(ws)
    await manager.broadcast(f"Client #{client_id} has entered the chat.")
    try:
        while True:
            data = await ws.receive_text()
            await manager.send_msg(f"You say: {data}", ws)
            await manager.broadcast(f"Client #{client_id} say: {data}")
    except WebSocketDisconnect:
        manager.disconnect(ws)
        await manager.broadcast(f"Client #{client_id} has left the chat.")

