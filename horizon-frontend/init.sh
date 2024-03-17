#!/bin/bash

# generate a random plaintext password for the admin account consisting of 3 4-letter random strings
password=$(cat /dev/urandom | tr -dc 'a-z' | fold -w 4 | head -n 3 | paste -sd- -)

echo "Admin username: admin"
echo "Admin password: $password"

# hash the password
hashed_password=$(echo -n "$password" | openssl dgst -sha256)

# Create the admin account
curl -X POST http://user-api:8002/users/signup \
    -H "Content-Type: application/json" \
    -d '{
        "username": "admin",
        "hashed_password": "'"$hashed_password"'"
    }'