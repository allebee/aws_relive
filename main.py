from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from starlette.responses import HTMLResponse
from starlette.middleware.cors import CORSMiddleware
import uvicorn
import asyncio

app = FastAPI()

# Enable CORS to allow access from the frontend (if running on a different domain)
app.add_middleware(
    CORSMiddleware,
    # You should restrict this to your frontend domain in production
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount the static files directory for serving HTML, CSS, and JavaScript
app.mount("/static", StaticFiles(directory="static"), name="static")

# Define the WebSocket route


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            frame = await websocket.receive_text()
            await websocket.send_bytes(frame)
            # You can process the received frames here if needed
    except WebSocketDisconnect:
        pass

# Define a route to serve your HTML page


@app.get("/", response_class=HTMLResponse)
async def get_html():
    with open("static/index.html", "r") as html_file:
        content = html_file.read()
    return HTMLResponse(content)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
