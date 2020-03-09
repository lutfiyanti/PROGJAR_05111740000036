import socket

TARGET_IP = "192.168.43.21"
TARGET_PORT = 5006

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.sendto(bytes('Lutfiyanti'.encode()),(TARGET_IP,TARGET_PORT))