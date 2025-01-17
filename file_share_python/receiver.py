"""
Server receiver of the file
"""
import socket
import tqdm
import os
import requests


def get_current_ipv6():

    """Get the current external IPv6 address or return None if no connection to the IPify service is possible"""
    try:
        return requests.get("https://api6.ipify.org", timeout=5).text
    except requests.exceptions.ConnectionError as ex:
        return None

# device's IP address
#SERVER_HOST = "2001:1284:f02e:9d6a:5c2:d531:6040:8316"
SERVER_HOST = get_current_ipv6()
SERVER_PORT = 5001

### Printa na tela o endereco ip para poder ser copiado
print(SERVER_HOST)

# receive 4096 bytes each time

BUFFER_SIZE = 1024 * 4 #4KB
SEPARATOR = "<SEPARATOR>"
# create the server socket
# TCP socket

s = socket.socket(socket.AF_INET6, socket.SOCK_STREAM, 0)

# bind the socket to our local address
s.bind((SERVER_HOST, SERVER_PORT))
# enabling our server to accept connections
# 5 here is the number of unaccepted connections that
# the system will allow before refusing new connections
s.listen(5)

print(f"[*] Listening as {SERVER_HOST}:{SERVER_PORT}")

# accept connection if there is any
client_socket, address = s.accept() 
# if below code is executed, that means the sender is connected
print(f"[+] {address} is connected.")

# receive the file infos
# receive using client socket, not server socket
received = client_socket.recv(BUFFER_SIZE).decode()
filename, filesize = received.split(SEPARATOR)
# remove absolute path if there is
filename = os.path.basename(filename)
# convert to integer
filesize = int(filesize)
# start receiving the file from the socket
# and writing to the file stream
progress = tqdm.tqdm(range(filesize), f"Receiving {filename}", unit="B", unit_scale=True, unit_divisor=1024)
with open(filename, "wb") as f:
    while True:
        # read 1024 bytes from the socket (receive)
        bytes_read = client_socket.recv(BUFFER_SIZE)
        if not bytes_read:    
            # nothing is received
            # file transmitting is done
            break
        # write to the file the bytes we just received
        f.write(bytes_read)
        # update the progress bar
        progress.update(len(bytes_read))

# close the client socket
client_socket.close()
# close the server socket
s.close()