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

    # command is ls
    if cm == "ls":
        # get server response
        data= getRecv(s, 102400)

        # looping data from client
        for i in data['files']:
            # convert size to Kb
            size= i['size'] / 1000
            size= str(size)
            # print
            print(str(i['name'])+"\t\t"+size+" Kb")

    # command is get
    if cm == "get":
        # if get all files
        if fname == ".":
            # get how many file to download
            ssize = getRecv(s, 1024)
            # tell the server if client ready
            s.send(createJSON('ok', 'ready to download'))
            for i in range(int(ssize)):
                # get file name
                fff_name = getRecv(s, 1024)
                # tell the server if client ready
                s.send(createJSON('ok', 'ready to download'))
                # create file with filename
                with open(fff_name, 'wb') as f:
                    # get part of file
                    data = s.recv(1024)
                    # looping to write file
                    while True:
                        # write to file
                        f.write(data)
                        # tell the server if client ready
                        s.send(createJSON('ok', 'got part of file'))
                        # get part of file again
                        data = s.recv(1024)
                        # if got not part of file, but $end$, there is a 
                        # notification from server that all part of files have been sent
                        # not using json format cause it can be part of file
                        if data.decode("utf-8") == "$end$":
                            print(fff_name+" has been downloaded")
                            break
        # if file name inputed, only get 1 files
        else:
            # get status file from server, exists or not exists
            should_try = getRecv(s, 1024)
            # file exists
            if should_try == "$present$":
                # tell the server if client ready
                s.send(createJSON('ok', 'ok'))
                # create file with filename
                with open(fname, 'wb') as f:
                    # get part of file
                    data = s.recv(1024)
                    # looping to write file
                    while True:
                        # write to file
                        f.write(data)
                        # tell the server if client ready
                        s.send(createJSON('ok', 'got part of file'))
                        # get part of file again
                        data = s.recv(1024)
                        # if got not part of file, but $end$, there is a 
                        # notification from server that all part of files have been sent
                        # not using json format cause it can be part of file
                        if data.decode("utf-8") == "$end$":
                            print(fname+" has been downloaded")
                            break
            # file not exists
            else:
                print(should_try)

    if cm == "put":
        if fname == ".":
            # get current path
            path = os.getcwd()
            # get array of all files
            all_files = [f for f in os.listdir(path)
                         if os.path.isfile(os.path.join(path, f))]
            # count files
            ssize = len(all_files)
            # send to server how many files to upload
            s.send(createJSON('ok', ssize))
            # waiting client ready
            n = getRecv(s, 1024)
            # looping files
            for a_file in all_files:
                # tell server filename to upload
                s.send(createJSON('ok', a_file))
                # waiting client ready
                n = getRecv(s, 1024)
                # read file
                with open(str(a_file), "rb") as f:
                    # read part of file
                    l = f.read(1024)
                    # looping part of file
                    while (l):
                        # send part of file via socket
                        s.send(l)
                        # waiting server got part of file
                        n = getRecv(s, 1024)
                        # read part of file again
                        l = f.read(1024)
                    s.send(str.encode("$end$"))
                print(str(a_file)+' was uploaded to server')
        else:
            # if empty fname
            if fname == "":
                # send to server status file not exist
                s.send(createJSON('ok', 'notOk'))
                print("provide a filename")
            # if file is exists
            elif os.path.exists(fname):
                # send to server status file exist
                s.send(createJSON('ok', 'ok'))
                # get current path
                cur_path = os.getcwd()
                # waiting client ready
                n = getRecv(s, 1024)
                # read file
                with open(str(fname), "rb") as f:
                    # read part of file
                    l = f.read(1024)
                    # looping part of file
                    while (l):
                        # send part of file via socket
                        s.send(l)
                        # waiting server got part of file
                        n = getRecv(s, 1024)
                        # read part of file again
                        l = f.read(1024)
                    s.send(str.encode("$end$"))
                print(str(fname)+' was uploaded to server')
                # if file is exists
            else:
                # send to server status file not exist
                s.send(createJSON('ok', 'notOk'))
                print("No Such file ", fname)

    if cm == "bye":
        break
    else:
        print (cm+" NO such command, use get, put, ls command")
