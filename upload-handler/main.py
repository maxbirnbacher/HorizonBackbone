from fastapi import FastAPI, File, UploadFile
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
fs = GridFS(db)

class FileResponse(BaseModel):
    filename: str

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

@app.get('/list-files')
async def list_files():
    file_list = []  # This will store a list of files and directories

    # Query MongoDB's GridFS for a list of files
    for grid_file in fs.find():
        file_list.append(grid_file.filename)

    return file_list

@app.get('/list-files-view')
async def list_files_view(request: Request):
    file_list = await list_files()
    return templates.TemplateResponse('list_files.html', {'request': request, 'file_list': file_list})