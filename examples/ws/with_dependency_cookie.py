from fastapi import FastAPI, WebSocket, Cookie, Depends, Query, status
from fastapi.responses import HTMLResponse

from typing import Optional

static_html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>WebSocket Chat</h1>
        <form action="" onsubmit="sendMessage(event)">
            <label>Item ID: <input type="text" id="itemId" autocomplete="off" value="item1"/></label>
            <label>Token: <input type="text" id="token" autocomplete="off" value="some-key-token"/></label>
            <button onclick="connect(event)">Connect</button>
            <hr>
            <label>Message: <input type="text" id="messageText" autocomplete="off"/></label>
            <button>Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
        var ws = null;
            function connect(event) {
                var itemId = document.getElementById("itemId")
                var token = document.getElementById("token")
                ws = new WebSocket("ws://localhost:8000/items/" + itemId.value + "/ws?token=" + token.value);
                ws.onmessage = function(event) {
                    var messages = document.getElementById('messages')
                    var message = document.createElement('li')
                    var content = document.createTextNode(event.data)
                    message.appendChild(content)
                    messages.appendChild(message)
                };
                event.preventDefault()
            }
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

app = FastAPI()

@app.get("/")
async def get():
    return HTMLResponse(static_html)

# endpoint invocation will check if
# token/cookie is injected into ws-controller object first
async def get_cookie_or_token(
    ws: WebSocket,
    session: Optional[str] = Cookie(None),
    token: Optional[str] = Query(None),
):
    if (session is None and token is None):
        await ws.close(code=status.WS_1008_POLICY_VIOLATION)

    return session or token

# with dependency injected, ready to use cookie/token
@app.websocket("/items/{item_id}/ws")
async def ws_endpoint(
    ws: WebSocket,
    item_id: str,
    q: Optional[str] = None,
    cookie_or_token: str = Depends(get_cookie_or_token),
):
    await ws.accept()
    while True:
        data = await ws.receive_text()
        await ws.send_text(f"Cookie/token: {cookie_or_token}")
        if (q is not None):
            await ws.send_text(f"Query param: {q}")

        await ws.send_text(f"Msg text: [{data}] for item: [{item_id}]")
