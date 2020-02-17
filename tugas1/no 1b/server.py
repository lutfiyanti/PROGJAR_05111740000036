import sys
import socket
# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Bind the socket to the port
server_address = ('127.0.0.1', 30000)
print(f"starting up on {server_address}")
sock.bind(server_address)
# Listen for incoming connections
sock.listen(1)


while True:
    # Wait for a connection
    print("waiting for a connection")
    connection, client_address = sock.accept()
    print(f"connection from {client_address}")
    
    recieved = connection.recv(64)
    mtr = open(recieved.decode(),"rb")

    print("request diterima")
    # Receive the data in small chunks and retransmit it   
    while True:
        data_rcv=mtr.read(64)
        if not data_rcv : break

        connection.sendall(data_rcv)
        print("send data")

    mtr.close()
    # Clean up the connection
    connection.close()