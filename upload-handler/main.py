from fastapi import FastAPI, File, UploadFile
import os

app = FastAPI()

# Define the directory where uploaded files will be saved
UPLOAD_FOLDER = '/app/uploads'  # Make sure this path matches the one in your Docker Compose config

@app.post('/upload')
async def upload_file(file: UploadFile = File(...)):
    if not file:
        return {'error': 'No file part'}

    if file.filename == '':
        return {'error': 'No selected file'}

    contents = await file.read()
    filename = os.path.join(UPLOAD_FOLDER, file.filename)
    with open(filename, 'wb') as f:
        f.write(contents)

    return {'message': 'File uploaded successfully', 'filename': file.filename}

# start the server with the 'uvicorn' command
# $ uvicorn main:app --reload