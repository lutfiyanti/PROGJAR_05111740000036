import socket
import os
import sys
import json
import pickle
import time

#host
HOST = "127.0.0.1"

# input port
if len(sys.argv) != 2:
    print(usage)
    sys.exit(0)

if len(sys.argv) > 1:
    PORT = int(sys.argv[1])


# function to receive client data and processing json format
def getRecv(sconn, tcpsize):
    # listen to socket
    recv = sconn.recv(tcpsize)
    # load data with json format
    recv = json.loads(pickle.loads(recv))
    # if response got ok, than get data
    if recv['response'] == 'ok':
        data = recv['data']
    # server error, response not ok 
    else:
        print('server error, bye')
        # exit program
        exit()
    # return data
    return data

# function to create json formate before sending to client
def createJSON(response, data):
    data = {
        'response' : response,
        'data' : data,
    }
    return pickle.dumps(json.dumps(data))

# prepare socket
s = socket.socket()
# connect socket
s.connect((HOST, PORT))
# get current directory of server
cur_dir = getRecv(s, 1024)

while True:
    # show input on terminal
    cmd = input(""+str("ftp@ ") + str(cur_dir) + " > ")
    # send inputed string
    s.send(createJSON('ok', cmd))
    # split string by space
    s_cmd = cmd.split(" ")
    # get command
    cm = s_cmd[0]

    # if any argument on command, use for get and put command
    try:
        fname = s_cmd[1]
    except:
        fname = ""

    if cm == "bye":
        exit()
    elif cmd != 'ls':
        print (cm+" NO such command, use ls command")
    else:
        # get server response
        data= getRecv(s, 102400)

        # looping data from client
        for i in data['files']:
            # convert size to Kb
            size= i['size'] / 1000
            size= str(size)
            # print
            print(str(i['name'])+"\t\t"+size+" Kb")
