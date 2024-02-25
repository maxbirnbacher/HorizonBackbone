from fastapi import FastAPI, File, UploadFile, Request
from fastapi.responses import HTMLResponse, StreamingResponse
from gridfs import GridFS
from pymongo import MongoClient
import base64

app = FastAPI()

# Initialize the MongoDB client
client = MongoClient("mongodb://mongo:27017/")
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

    # Convert base64 string to bytes and yield
    def decode_base64(file_data):
        for chunk in file_data:
            yield base64.b64decode(chunk)

    # Create a streaming response with the decoded file
    return StreamingResponse(decode_base64(grid_file), media_type='application/octet-stream')

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
