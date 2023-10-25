import os
import pty
import subprocess
import websockets

# Create a shell session and connect it to the WebSocket
async def start_shell(websocket):
    master, slave = pty.openpty()
    p = subprocess.Popen(['/bin/bash'], preexec_fn=os.setsid, stdout=slave, stderr=slave, stdin=slave)

    while True:
        try:
            # Read data from the WebSocket
            data = await websocket.receive_text()

            # Send user input to the VM
            os.write(master, data.encode('utf-8'))

            # Read the VM's response
            vm_response = os.read(master, 1024).decode('utf-8')

            # Send the VM's response back to the WebSocket
            await websocket.send_text(vm_response)
        except websockets.ConnectionClosed:
            os.killpg(os.getpgid(p.pid), 15)  # Terminate the shell process
            break
