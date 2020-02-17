import sys
import socket
# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Bind the socket to the port
server_address = ('127.0.0.1', 10000)
print(f"starting up on {server_address}")
sock.bind(server_address)
# Listen for incoming connections
sock.listen(1)


while True:
    # Wait for a connection
    print("waiting for a connection")
    connection, client_address = sock.accept()

    print(f"connection from {client_address}")
    file_2 = open("file2.txt","wb")
   
    # Receive the data in small chunks and retransmit it
    amount_received = 0
    while True:
        isi = connection.recv(256)
        amount_received += len(isi)
    
        if isi:
            file_2.write(isi)
        else: break

    file_2.close()
    print('File recieved')
    # Clean up the connection
    connection.close()