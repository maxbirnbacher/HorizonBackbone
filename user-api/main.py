from pymongo import MongoClient
from fastapi import FastAPI, Request, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import usermodel
from datetime import timedelta

# Define the access token expiry time in minutes
ACCESS_TOKEN_EXPIRE_MINUTES = 30


# Initialize the MongoDB client
client = MongoClient("mongodb://mongo:27017/")
db = client["database"]
connections = db["users"]

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app = FastAPI()

# API endpoints to provide user management functionality
# list all users
@app.get('/users/list-users')
async def list_users():
    user_list = []

    # Query MongoDB for a list of users
    for user in connections.find():
        user_list.append(user)

    # Return the list of users
    return {'user_list': user_list}

# register a new user
@app.post('/users/signup')
async def register_user(user: usermodel.UserHashedPassword):
    print(user.username, user.hashedPassword)

    # check if the user already exists
    if connections.find_one({"username": user.username}):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User already exists")

    # Insert the user into MongoDB
    user_id = connections.insert_one(user.dict()).inserted_id

    # Create the access token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = usermodel.UserInDB.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires)

    return {
        'message': 'User registered successfully',
        'user_id': str(user_id),
        'access_token': access_token,
        'token_type': 'bearer'
    }

# return a user token for login
app.post('/users/login')
async def login_user(form_data: OAuth2PasswordRequestForm = Depends()):
    print(form_data)
    # retrieve the user from the database
    user = connections.find_one({"username": form_data.username})
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password")

    # verify the password
    if not user.verify_password(form_data.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password")

    # create the access token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = user.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires)

    return {"access_token": access_token, "token_type": "bearer"}
