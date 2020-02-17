import sys
import socket

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = ('localhost', 10000)
print(f"connecting to {server_address}")
sock.connect(server_address)

file_1 = open("file1.txt","rb")
try:
    while True:
        isi = file_1.read(256)
        if not isi:
            break
        sock.send(isi)
    print("file terkirim")
    file_1.close()

finally:
    sock.close()