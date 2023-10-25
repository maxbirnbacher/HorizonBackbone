from fastapi import FastAPI, File, HTTPException, UploadFile, Request, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse, StreamingResponse
from gridfs import GridFS
from pymongo import MongoClient
from pydantic import BaseModel
from fastapi.templating import Jinja2Templates
from typing import List
from utils.shell import start_shell
import aiosubprocess
import websockets
import subprocess
import os

app = FastAPI()

templates = Jinja2Templates(directory="templates")  # Create a templates directory

# Initialize the MongoDB client
client = MongoClient("mongodb://mongo:27017/")
db = client["mydatabase"]
connections = db["connections"]
fs = GridFS(db)

class FileResponse(BaseModel):
    filename: str

# websocket ConnectionManager class
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    async def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_shell_output(self, websocket: WebSocket, message: str):
        await websocket.send_text(message)

    async def receive_shell_command(self, websocket: WebSocket):
        command = await websocket.receive_text()
        return command
    
    def is_connected(self, websocket: WebSocket):
        return websocket in self.active_connections

manager = ConnectionManager()


# index route
@app.get('/')
async def index(request: Request):
    return templates.TemplateResponse('index.html', {'request': request})

# render the upload form in an HTML template
@app.post('/upload')
async def upload_file(file: UploadFile = File(...)):
    if not file:
        return {'error': 'No file part'}

    if file.filename == '':
        return {'error': 'No selected file'}

    # Save the file to MongoDB GridFS
    with fs.new_file(filename=file.filename) as grid_file:
        grid_file.write(file.file.read())

    return {'message': 'File uploaded successfully', 'filename': file.filename}

# render the upload form in an HTML template
@app.get('/list-files')
async def list_files():
    file_list = []  # This will store a list of files and directories

    # Query MongoDB's GridFS for a list of files
    for grid_file in fs.find():
        file_list.append(grid_file.filename)

    return file_list

# render the file list in an HTML template
@app.get('/list-files-view')
async def list_files_view(request: Request):
    file_list = await list_files()
    return templates.TemplateResponse('list_files.html', {'request': request, 'file_list': file_list})

# render the file content in an HTML template
@app.get('/file/{filename}')
async def file_content(request: Request, filename: str):
    # Retrieve the file content from MongoDB GridFS
    grid_file = fs.find_one({"filename": filename})
    if not grid_file:
        return HTMLResponse(content="File not found", status_code=404)

    # Check if the file has a supported file extension
    supported_extensions = ['.txt', '.pdf', '.conf', '.json']
    file_extension = os.path.splitext(filename)[1]
    if file_extension not in supported_extensions:
        return templates.TemplateResponse('unsupported_file.html', {'request': request, 'filename': filename})

    content = grid_file.read()

    # Render the content in an HTML template
    return templates.TemplateResponse('file_content.html', {'request': request, 'filename': filename, 'content': content.decode()})

# download the file
@app.get('/download/{filename}')
async def download_file(filename: str):
    # Retrieve the file content from MongoDB GridFS
    grid_file = fs.find_one({"filename": filename})
    if not grid_file:
        return HTMLResponse(content="File not found", status_code=404)

    # Return the file data as a response
    return StreamingResponse(grid_file, media_type='application/octet-stream')

active_websockets = {}

@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    await websocket.accept()

    # Store the WebSocket connection for future reference
    active_websockets[client_id] = websocket

    try:
        while True:
            data = await websocket.receive_text()

            # Process the command or data received from the web terminal here.
            # You can execute commands, run scripts, etc., on the server.

            # For demonstration, let's echo the data back to the terminal.
            await websocket.send_text(f"You said: {data}")
    except WebSocketDisconnect:
        # WebSocket disconnected, remove it from the dictionary
        del active_websockets[client_id]

@app.get("/terminal/{client_id}")
def terminal(request: Request, client_id: int):
    # Replace `client_id` with the appropriate value
    return templates.TemplateResponse("terminal.html", {"request": request, "client_id": client_id})

# send the command to the reverse shell
@app.post("/send-command")
async def send_command(command: str):
    return await manager.receive_shell_command(command)

# receive the command from the reverse shell
@app.get("/receive-command")
async def receive_command():
    return await manager.send_shell_output()


