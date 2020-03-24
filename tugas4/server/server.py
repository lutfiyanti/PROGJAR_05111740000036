import os
import socket
import sys
import json
import pickle
from threading import Thread

# host
HOST = "127.0.0.1"

# input port
if len(sys.argv) != 2:
    print(usage)
    sys.exit(0)

if len(sys.argv) > 1:
    PORT = int(sys.argv[1])


# function to create socket
def create_socket():
    try:
        global HOST
        global PORT
        global sd
        sd = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error as e:
        print("Socket creation error ", str(e))


# function to bind port
def bind_socket():
    try:
        global HOST
        global PORT
        global sd

        sd.bind((HOST, PORT))
        sd.listen(5)
        print("Socket binded to port", PORT, "listeninig")
    except socket.error as e:
        print("Error in binding socket ", str(e), "\nRetrying...")
        bind_socket()


# function to listening socket on port, and waiting to client connection
def socket_accept():
    while True:
        conn, address = sd.accept()
        print("Connection established: Ip: ", address[0], ":", address[1])
        try:
            Thread(target=send_data, args=(conn, address)).start()
        except:
            print("error in creating thread")

# function to create json formate before sending to client
def createJSON(response, data):
    data = {
        'response' : response,
        'data' : data,
    }
    return pickle.dumps(json.dumps(data))

# function to receive client data and processing json format
def getRecv(sconn, tcpsize):
    # listen to socket
    recv = sconn.recv(tcpsize)
    # load data with json format
    recv = json.loads(pickle.loads(recv))
    # if response got ok, than get data
    if recv['response'] == 'ok':
        data = recv['data']
    # error
    else:
        data = ''
    # return data
    return data

def handleLs(conn):
    # get list file in directory
    datas = os.listdir()
    # create json variable
    files = []
    # looping file
    for d in datas:
        #get name file
        d = str(d)
        tmp={
            'name': d,
            'size': os.path.getsize(d), # get file size
        }
        files.append(tmp) # insert to json variable
    if len(files) < 1: 
        files = 'Folder Empty'
    # prepare variable for client
    json = {
        'files' : files
    }
    # send to client
    conn.send(createJSON('ok', json))


def handleGet(conn, filename):
    # get all file
    if filename == ".":
        # get path client
        path = os.getcwd()
        # get array of all files
        all_files = [f for f in os.listdir(path)
                     if os.path.isfile(os.path.join(path, f))]
        # count all files
        ssize = len(all_files)
        # send to client
        conn.send(createJSON('ok', ssize))
        # waiting to client ready to download file
        n = getRecv(conn, 1024)
        for a_file in all_files:
            # send file name to client
            conn.send(createJSON('ok', str(a_file)))
            # waiting to client ready to download file
            n = getRecv(conn, 1024)
            with open(str(a_file), "rb") as f:
                # read file
                l = f.read(1024)
                while (l):
                    # send part of file via socket
                    conn.send(l)
                    # waiting to client download part of file
                    n = getRecv(conn, 1024)
                    # read file again
                    l = f.read(1024)
                # tell client if all part of file have been sent
                conn.send(str.encode("$end$"))
                f.close()
        return
    # get one files
    else:
        cur_path = os.getcwd()
        # check if file exists
        if os.path.exists(filename):
            print('onok')
            # tell client if file exists
            conn.send(createJSON('ok', "$present$"))
            # waiting to client ready to download file
            istry = getRecv(conn, 1024)
            if istry == "ok":
                # open file
                with open(filename, "rb") as f:
                    # open file
                    f = open(filename, 'rb')
                    # read file
                    l = f.read(1024)
                    while (l):
                        # send part of file via socket
                        conn.send(l)
                        # waiting to client download part of file
                        n = getRecv(conn, 1024)
                        # read file again
                        l = f.read(1024)
                    # tell client if all part of file have been sent
                    conn.send(str.encode("$end$"))
                    f.close()
            return
        # file not exists
        else:
            conn.send(createJSON('ok', filename+" not exists"))
            return


def handlePut(conn, filename):
    # put all files
    if filename == ".":
        # get how many files to upload
        ssize = getRecv(conn, 1024)
        # tell client that server is ready
        conn.send(createJSON('ok', 'ready to upload'))
        for i in range(int(ssize)):
            # get filename
            fff_name = getRecv(conn, 1024)
            # tell client that server is ready
            conn.send(createJSON('ok', 'ready to upload'))
            # prepare file
            with open(fff_name, 'wb') as f:
                # got part of file
                data = conn.recv(1024)
                # looping part of file
                while True:
                    # write part of file
                    f.write(data)
                    # tell client that server is got part of file
                    conn.send(createJSON('ok', 'got part of file'))
                    # if got not part of file, but $end$, there is a 
                    # notification from server that all part of files have been sent
                    # not using json format cause it can be part of file
                    data = conn.recv(1024)
                    if data.decode("utf-8") == "$end$":
                        print(str(fff_name)+' was uploaded')
                        break
        return
    # put one files
    else:
        status = getRecv(conn, 1024)
        if status == 'notOk':
            return
        else :
            # tell client that server is ready
            conn.send(createJSON('ok', 'ready to upload'))
            # read file
            with open(filename, 'wb') as f:
                # got part of file
                data = conn.recv(1024)
                # looping part of file
                while True:
                    # write part of file
                    f.write(data)
                    # tell client that server is got part of file
                    conn.send(createJSON('ok', 'got part of file'))
                    # if got not part of file, but $end$, there is a 
                    # notification from server that all part of files have been sent
                    # not using json format cause it can be part of file
                    data = conn.recv(1024)
                    if data.decode("utf-8") == "$end$":
                        print(str(filename)+' was uploaded')
                        break
            return

# function to listen client and prepare client command
def send_data(conn, a):
    # get current directory
    send_dir = os.getcwd()
    # send current directory to client
    conn.send(createJSON('ok', send_dir))
    while True:
        # get client command
        data = getRecv(conn, 1024)
        # split string by space
        r_cmd = data.split(" ")
        # get command
        cmd = r_cmd[0]
        print(r_cmd)
        
        # if any argument on command, use for get and put command
        try:
            filename = r_cmd[1]
        except:
            pass
        # command is ls
        if(cmd == "ls"):
            handleLs(conn)
        # command is get
        elif(cmd == "get"):
            if filename == '':
                d = "filename is empty"
            else:
                handleGet(conn, filename)
        # command is put
        elif(cmd == "put"):
            if filename == '':
                d = "filename is empty"
            else:
                handlePut(conn, filename)
        # no command
        else:
            d = "NO such command, use get, put, ls command"


# function main
def main():
    create_socket()
    bind_socket()
    socket_accept()

# run program
main()