```
██╗  ██╗ ██████╗ ██████╗ ██╗███████╗ ██████╗ ███╗   ██╗██████╗  █████╗  ██████╗██╗  ██╗██████╗  ██████╗ ███╗   ██╗███████╗
██║  ██║██╔═══██╗██╔══██╗██║╚══███╔╝██╔═══██╗████╗  ██║██╔══██╗██╔══██╗██╔════╝██║ ██╔╝██╔══██╗██╔═══██╗████╗  ██║██╔════╝
███████║██║   ██║██████╔╝██║  ███╔╝ ██║   ██║██╔██╗ ██║██████╔╝███████║██║     █████╔╝ ██████╔╝██║   ██║██╔██╗ ██║█████╗  
██╔══██║██║   ██║██╔══██╗██║ ███╔╝  ██║   ██║██║╚██╗██║██╔══██╗██╔══██║██║     ██╔═██╗ ██╔══██╗██║   ██║██║╚██╗██║██╔══╝  
██║  ██║╚██████╔╝██║  ██║██║███████╗╚██████╔╝██║ ╚████║██████╔╝██║  ██║╚██████╗██║  ██╗██████╔╝╚██████╔╝██║ ╚████║███████╗
╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝╚═╝╚══════╝ ╚═════╝ ╚═╝  ╚═══╝╚═════╝ ╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝╚═════╝  ╚═════╝ ╚═╝  ╚═══╝╚══════╝
```

-----------------------------------------------------------------------------------

**THIS SERVICE IS DESIGNED FOR EDUCATIONAL PURPOSE ONLY! DO NOT USE IT FOR ILLEGAL PURPOSES!**

The heart of the Horizon Malware Suite and used for all kinds of things *(currently only for data exfiltration)*.

## Roadmap

- [X] List files
- [x] Simple web-interface
- [x] File download
- [ ] Delete file(s)
- [X] Make a better UI for the web-interface
- [X] C2 Server and API
- [X] Frontend for C2 Server
- [ ] API & frontend authentication
- [ ] Dynamic creation of stagers/droppers
- [ ] Frontend-Dialog for stager/dropper creation
- [ ] File upload for droppers


## Setup & Start

Clone the repository and run `docker-compose build` to build the images.

Start the stack with `docker-compose up -d` and you are good to go.

## Usage

### Dashboard

After starting the stack you can access the Webinterface by accessing `http://SERVER_IP_OR_DOMAIN:8000` in your browser.

There you can (*currently*) choose between the Data Exfiltration and the C2 Server.

### Data Exfiltration

To exfiltrate data you can use the '/upload' endpoint.

You can see your uploaded files under `http://SERVER_IP_OR_DOMAIN:8000/list-files-view`.

![DataExfil](https://github.com/maxbirnbacher/HorizonBackbone/assets/66524685/39b7923c-8328-4672-8dc7-5f75cc725565)

If you click on the filename you can access the file and download it.

![FileView](https://github.com/maxbirnbacher/HorizonBackbone/assets/66524685/75e3ff57-d2e7-45da-8c4d-8f8beffb0653)

### C2 Server

The C2 Server is intended for long-term usage. Communication should take place over a long period of time that are non-linear to avoid beacon detection.

The workflow is as follows:

1. Register a new client. This will create a new client in the database and return a unique ID. This ID is used for all further communication with the client. (`http://SERVER_IP_OR_DOMAIN:8000/register`)
2. Queue new commands for the client via the web-interface in the detail view of each client.
3. The client will check for new command(s) after the specified interval and execute it/them. (`http://SERVER_IP_OR_DOMAIN:8000/commands/{connection_id}`)
4. The client will send the results of the command(s) to the server. (`http://SERVER_IP_OR_DOMAIN:8000/output/send/{connection_id}`)
5. The server will store the results in the database and make them available via the web-interface. Hit the refresh button in the detail view of the client to see the output.
6. Unregister the client if you don't need it anymore. (`http://SERVER_IP_OR_DOMAIN:8000/unregister/{connection_id}`) *interface currently in development*


### API

You can find all the API endpoints in the under `http://SERVER_IP_OR_DOMAIN:8000/docs`.





