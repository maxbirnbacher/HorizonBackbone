<!-- ```
██╗  ██╗ ██████╗ ██████╗ ██╗███████╗ ██████╗ ███╗   ██╗██████╗  █████╗  ██████╗██╗  ██╗██████╗  ██████╗ ███╗   ██╗███████╗
██║  ██║██╔═══██╗██╔══██╗██║╚══███╔╝██╔═══██╗████╗  ██║██╔══██╗██╔══██╗██╔════╝██║ ██╔╝██╔══██╗██╔═══██╗████╗  ██║██╔════╝
███████║██║   ██║██████╔╝██║  ███╔╝ ██║   ██║██╔██╗ ██║██████╔╝███████║██║     █████╔╝ ██████╔╝██║   ██║██╔██╗ ██║█████╗  
██╔══██║██║   ██║██╔══██╗██║ ███╔╝  ██║   ██║██║╚██╗██║██╔══██╗██╔══██║██║     ██╔═██╗ ██╔══██╗██║   ██║██║╚██╗██║██╔══╝  
██║  ██║╚██████╔╝██║  ██║██║███████╗╚██████╔╝██║ ╚████║██████╔╝██║  ██║╚██████╗██║  ██╗██████╔╝╚██████╔╝██║ ╚████║███████╗
╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝╚═╝╚══════╝ ╚═════╝ ╚═╝  ╚═══╝╚═════╝ ╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝╚═════╝  ╚═════╝ ╚═╝  ╚═══╝╚══════╝
``` -->

# HorizonBackbone

-----------------------------------------------------------------------------------

**THIS PROJECT IS MAINLY DEVELOPED FOR EDUCATIONAL PURPOSE! DO NOT USE IT FOR ILLEGAL ACTIVITIES!**

***Go to the [development-microservices](https://github.com/maxbirnbacher/HorizonBackbone/tree/development-microservices) branch for a preview of the microservices version (currently in development and not ready for production).***

The heart of the Horizon Malware Suite and used for all kinds of things.

## Roadmap

- [X] List files
- [x] Simple web-interface
- [x] File download
- [ ] Delete file(s)
- [X] Make a better UI for the web-interface
- [X] C2 Server and API
- [X] Frontend for C2 Server
- [ ] Rewrite API and frontend as microservices (in progress)
- [ ] API & frontend authentication (in progress)
- [ ] Control interface for a [Traverse](https://github.com/maxbirnbacher/Traverse) redirection network
- [ ] Dynamic creation of stagers/droppers
- [ ] Frontend-Dialog for stager/dropper creation
- [ ] File upload for droppers


## Why microservices?

I want to make the whole Horizon Malware Suite as modular as possible. This way you can use the parts you need and don't have to use the whole suite.
Another aspect is that I want to add scalability to the project. If you want to use the whole suite you can just spin up multiple instances of the microservices and use a load balancer to distribute the load.

It will also allow me to develop the different parts of the suite independently from each other. This way I can focus on one part at a time and don't have to worry about breaking other parts of the suite.

Microservices will bring a very big change to the project. For example the frontend will be a NodeJS application that will communicate with the API via REST. I previously used Jinja2 templates to render the frontend. This is why I also need to rewrite parts of the API.

## Setup & Start

Clone the repository and run `docker-compose build` to build the images.

Start the stack with `docker-compose up -d` and you are good to go.

## Usage

### Dashboard (DEPRECATED)

After starting the stack you can access the Webinterface by accessing `http://SERVER_IP_OR_DOMAIN:8000` in your browser.

There you can (*currently*) choose between the Data Exfiltration and the C2 Server.

### Data Exfiltration (DEPRECATED)

To exfiltrate data you can use the '/upload' endpoint.

You can see your uploaded files under `http://SERVER_IP_OR_DOMAIN:8000/list-files-view`.

![DataExfil](https://github.com/maxbirnbacher/HorizonBackbone/assets/66524685/39b7923c-8328-4672-8dc7-5f75cc725565)

If you click on the filename you can access the file and download it.

![FileView](https://github.com/maxbirnbacher/HorizonBackbone/assets/66524685/75e3ff57-d2e7-45da-8c4d-8f8beffb0653)

### C2 Server (DEPRECATED)

The C2 Server is intended for long-term usage. Communication should take place over a long period of time that are non-linear to avoid beacon detection.

The workflow is as follows:

1. Register a new client. This will create a new client in the database and return a unique ID. This ID is used for all further communication with the client. (`http://SERVER_IP_OR_DOMAIN:8000/register`)
2. Queue new commands for the client via the web-interface in the detail view of each client.
3. The client will check for new command(s) after the specified interval and execute it/them. (`http://SERVER_IP_OR_DOMAIN:8000/commands/{connection_id}`)
4. The client will send the results of the command(s) to the server. (`http://SERVER_IP_OR_DOMAIN:8000/output/send/{connection_id}`)
5. The server will store the results in the database and make them available via the web-interface. Hit the refresh button in the detail view of the client to see the output.
6. Unregister the client if you don't need it anymore. (`http://SERVER_IP_OR_DOMAIN:8000/unregister/{connection_id}`) *interface currently in development*

#### Reverse Shell Example

You can find reverse shell examples in my [Reverse Shell Repository](https://github.com/maxbirnbacher/ReverseShells).

At the moment I recommend using the `simpleBeacon2.ps1` script. It is a simple reverse shell that connects to the C2 server and waits for commands.

### API

You can find all the API endpoints at `/docs` on their respective ports.





