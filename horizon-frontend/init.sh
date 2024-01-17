#!/bin/bash

# Wait for the server to start
sleep 10

# Create the admin account
curl -X POST http://10.0.0.9:8002/users/register \
    -H "Content-Type: application/json" \
    -d '{
        "username": "admin",
        "password": "admin"
    }'