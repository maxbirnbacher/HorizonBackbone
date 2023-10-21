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

- [X] List Files
- [x] Simple Webinterface
- [x] File Download
- [ ] Delete File(s)
- [ ] Make a better UI for the Webinterface
- [ ] Add C2 Server

## Setup & Start

Clone the repository and run `docker-compose build` to build the images.

Start the stack with `docker-compose up -d` and you are good to go.

## Usage

### Dashboard **UNDER DEVELOPMENT, NOT IMPLEMENTED**

After starting the stack you can access the Webinterface by accessing `http://SERVER_IP_OR_DOMAIN:8000` in your browser.

### Data Exfiltration

To exfiltrate data you can use the '/upload' endpoint.

You can see your uploaded files under `http://SERVER_IP_OR_DOMAIN:8000/list-files-view`.

![DataExfil](https://github.com/maxbirnbacher/HorizonBackbone/assets/66524685/39b7923c-8328-4672-8dc7-5f75cc725565)

If you click on the filename you can access the file and download it.

![FileView](https://github.com/maxbirnbacher/HorizonBackbone/assets/66524685/75e3ff57-d2e7-45da-8c4d-8f8beffb0653)

### API

You can find all the API endpoints in the under `http://SERVER_IP_OR_DOMAIN:8000/docs`.





