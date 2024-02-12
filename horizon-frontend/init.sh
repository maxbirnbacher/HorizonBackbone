#!/bin/bash

# Create the admin account
hashed_password=$(echo -n "admin" | openssl dgst -sha256)
curl -X POST http://localhost:8002/users/register \
    -H "Content-Type: application/json" \
    -d '{
        "username": "admin",
        "hashed_password": "'"$hashed_password"'"
    }'