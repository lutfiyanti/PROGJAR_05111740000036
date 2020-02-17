import sys
import socket

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = ('localhost', 30000)
print(f"connecting to {server_address}")
sock.connect(server_address)


try:
    amount_received = 0
    # Send data
    message = 'file_request.txt'
    print(f"sending {message} as request")
    sock.sendall(message.encode())
    
    # Look for the response
    mtr = open("file_recieved.txt","wb")

    amount_expected = len(message)
    if amount_received < amount_expected:
        data_terima = sock.recv(64)
        amount_received += len(data_terima)
        mtr.write(data_terima)
        print("File Received")
    else:
        print("File not Received")
finally:
    print("closing")
    sock.close()