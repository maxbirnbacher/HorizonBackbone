#!/bin/bash

# Wait for the server to start
sleep 10

# Create the admin account
curl -X POST http://localhost:8002/users/register \
    -H "Content-Type: application/json" \
    -d '{
        "username": "admin",
        "password": "admin"
    }'