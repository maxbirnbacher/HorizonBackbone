# Use an official Node.js runtime as the base image
FROM node:18

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy package.json and package-lock.json to the container
COPY package*.json ./

# Install project dependencies
RUN npm install

# Copy the rest of the project files to the container
COPY . .

# Copy the bin/www file into the container
COPY ./bin/www /usr/src/app/bin/www

# Copy the init script into the container
COPY init.sh /usr/src/app/init.sh

# Make the init script executable
RUN chmod +x /usr/src/app/init.sh

# Expose the port your Express app is listening on
EXPOSE 3000

# Start the Express app
CMD /usr/src/app/init.sh && npm start