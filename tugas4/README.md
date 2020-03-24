# Tugas 4

## Soal Tugas 4 :
![1](https://github.com/PutriEndahP/PROGJAR_05111740000039/blob/master/tugas4/soal%20tugas%204.jpeg)

### Dokumentasi Protocol

### Buatlah Dokumentasi dari Protocol tersebut, berisikan :

#### a. Ketentuan Membaca Format: 

```
data = {
        'response' : response,
        'data' : data,
    }
    return pickle.dumps(json.dumps(data))
```
Diatas merupakan format function untuk merubah menajdi Json.

#### b. Daftar Fitur:

  Terdapat tiga fitur di protocol ini, yaitu :
  
  * GET : Fitur yang digunakan untuk mengambil file.
  
  * PUT : Fitur yang digunakan untuk meletakkan file.
  
  * LS : Fitur yang digunakan untuk melihat list file dalam directory.

#### c. Cara Melakukan Request :

  Request dilakukan oleh client, dengan meng-inputkan string yang diminta. Request tersebut selanjutnya akan diterima oleh server dan     akan di proses lebih lanjut.
  
  Berikut ini merupakan source code dari client untuk memasukkan input :
  
  ```
    cmd = input(""+str("ftp@ ") + str(cur_dir) + " > ")
    s.send(createJSON('ok', cmd))
    s_cmd = cmd.split(" ")
    cm = s_cmd[0]

    try:
        fname = s_cmd[1]
    except:
        fname = ""
  ```
  Berikut penjelasannya :
  
  ``` cmd = input(""+str("ftp@ ") + str(cur_dir) + " > ") ``` Digunakan untuk menampilkan input di terminal.
  
  ``` s.send(createJSON('ok', cmd)) ``` Digunakan untuk mengirimkan string input sesuai dengan command yang dituliskan.
  
  ```  s_cmd = cmd.split(" ") ``` Digunakan untuk memecah string inputnya.
  
  ```  cm = s_cmd[0] ``` Untuk mendapatkan command inputnya.
  
  * Request untuk mendapatkan list data :
  
  ``` 
    if cm == "ls":
        data= getRecv(s, 102400)

        for i in data['files']:
            size= i['size'] / 1000
            size= str(size)
            print(str(i['name'])+"\t\t"+size+" Kb")
  ```
  
  Command ls digunakan untuk mendapat list file dalam suatu directory. Kemudian client akan mendapatkan response dari server yang akan     dimasukkan ke variabel bernama data. Selanjutnya akan dilakukan looping data dari client. Ukuran datanya akan dirubah ke Kb dengan       dibagi 1000. Kemudian hasil akan di print. 
  
  * Request untuk mendapat file :
  
  ```
    if cm == "get":
        if fname == ".":
            ssize = getRecv(s, 1024)
            s.send(createJSON('ok', 'ready to download'))
            for i in range(int(ssize)):
                fff_name = getRecv(s, 1024)
                s.send(createJSON('ok', 'ready to download'))
                with open(fff_name, 'wb') as f:
                    data = s.recv(1024)
                    while True:
                        f.write(data)
                        s.send(createJSON('ok', 'got part of file'))
                        data = s.recv(1024)
                        if data.decode("utf-8") == "$end$":
                            print(fff_name+" has been downloaded")
                            break
        else:
            should_try = getRecv(s, 1024)
            if should_try == "$present$":
                s.send(createJSON('ok', 'ok'))
                with open(fname, 'wb') as f:
                    data = s.recv(1024)
                    while True:
                        f.write(data)
                        s.send(createJSON('ok', 'got part of file'))
                        data = s.recv(1024)
                        if data.decode("utf-8") == "$end$":
                            print(fname+" has been downloaded")
                            break
            else:
                print(should_try)
  ```
  
  Command get untuk mendapatkan file dari suatu directory. Untuk mendapatkan semua file dalam sebuah directory bisa menggunakan command   ``` get [.] ```. Tapi jika ingin mendapatkan satu file saja dalam suatu directory menggunakan command ``` get [namafile] ```. Kemudian    server akan mengirimkan request dan client akan mencetak file yang diminta.
  
  * Request untuk meletakkan file :
  
  ```
  if cm == "put":
        if fname == ".":
            path = os.getcwd()
            all_files = [f for f in os.listdir(path)
                         if os.path.isfile(os.path.join(path, f))]
            ssize = len(all_files)
            s.send(createJSON('ok', ssize))
            n = getRecv(s, 1024)
            for a_file in all_files:
                s.send(createJSON('ok', a_file))
                n = getRecv(s, 1024)
                with open(str(a_file), "rb") as f:
                    l = f.read(1024)
                    while (l):
                        s.send(l)
                        n = getRecv(s, 1024)
                        l = f.read(1024)
                    s.send(str.encode("$end$"))
                print(str(a_file)+' was uploaded to server')
        else:
            if fname == "":
                s.send(createJSON('ok', 'notOk'))
                print("provide a filename")
            elif os.path.exists(fname):
                s.send(createJSON('ok', 'ok'))
                cur_path = os.getcwd()
                n = getRecv(s, 1024)
                with open(str(fname), "rb") as f:
                    l = f.read(1024)
                    while (l):
                        s.send(l)
                        n = getRecv(s, 1024)
                        l = f.read(1024)
                    s.send(str.encode("$end$"))
                print(str(fname)+' was uploaded to server')
            else:
                s.send(createJSON('ok', 'notOk'))
                print("No Such file ", fname)
  ```
  
  Command put digunakan untuk meletakkan file ke suatu directory. Dengan command ``` put [filename] ``` maka server akan memproses         permintaan client dan meletakkan file tertentu yang sudah dipilih. Sedangkan jika tidak ada file yang akan di letakkan maka client       akan mencetak pesan bahwa tidak ada file atau " No Such File ".

#### d. Apa Respon yang Didapat : 

  Aksi yang didapat sever setelah mendapat request dari client yaitu akan memproses permintaan client sesuai dengan request nya,           sehingga client akan mendapat respon kembali.
  
  Berikut ini merupakan aksi dari server berdasarkan request client.
  
  * Aksi Server setelah mendapat respon ls :
  
  ```
  def handleLs(conn):
    datas = os.listdir()
    files = []
    for d in datas:
        d = str(d)
        tmp={
            'name': d,
            'size': os.path.getsize(d), # get file size
        }
        files.append(tmp) # insert to json variable
    if len(files) < 1: 
        files = 'Folder Empty'
    json = {
        'files' : files
    }
    conn.send(createJSON('ok', json))
  ```
  
  Fungsi handleLs untuk mengirim respon ke client saat meminta request ls. Pertama, server akan mendapatkan list file dari directory.     Kemudian akan membuat variable Json berupa array bernama files. Dibuat looping untuk files untuk mendapatkan nama file dan file size     nya. Membuat object bernama ``` tmp ``` kemudian dimasukkan ke variable files. Hitung panjang file nya, kalau panjang file 0 maka       tidak ada file maka ``` Folder Empty ```. Buat Json nya dengan parameter files dan isinya files. Selanjutnya dikoneksikan dan dikirim   dengan parameter Json yaitu response dan data.
  
  Function untuk membuat Json :
  
  ```
  def createJSON(response, data):
    data = {
        'response' : response,
        'data' : data,
    }
    return pickle.dumps(json.dumps(data))

  ```
  
  ``` json.dumps ``` digunakan untuk men-serialize untuk memastikan parameter Json tidak rusak.
  
  ``` pickle.dumps ``` merupakan library yang digunakan untuk men-serialize data pada pengiriman yaitu merubah array menjadi string.
  
  
   * Aksi Server setelah mendapat respon get :
   
   ```
   def handleGet(conn, filename):
    if filename == ".":
        path = os.getcwd()
        all_files = [f for f in os.listdir(path)
                     if os.path.isfile(os.path.join(path, f))]
        ssize = len(all_files)
        conn.send(createJSON('ok', ssize))
        n = getRecv(conn, 1024)
        for a_file in all_files:
            conn.send(createJSON('ok', str(a_file)))
            n = getRecv(conn, 1024)
            with open(str(a_file), "rb") as f:
                l = f.read(1024)
                while (l):
                    conn.send(l)
                    n = getRecv(conn, 1024)
                    l = f.read(1024)
                conn.send(str.encode("$end$"))
                f.close()
        return
    else:
        cur_path = os.getcwd()
        if os.path.exists(filename):
            print('onok')
            conn.send(createJSON('ok', "$present$"))
            istry = getRecv(conn, 1024)
            if istry == "ok":
                with open(filename, "rb") as f:
                    f = open(filename, 'rb')
                    l = f.read(1024)
                    while (l):
                        conn.send(l)
                        n = getRecv(conn, 1024)
                        l = f.read(1024)
                    conn.send(str.encode("$end$"))
                    f.close()
            return
        else:
            conn.send(createJSON('ok', filename+" not exists"))
            return
   ```
   
   Server mendapatkan array dari semua file. Kemudian koneksi terhubung danmengirimkan ke client.
   
   
   * Aksi Server setelah mendapat respon put :
   
   ```
   ef handlePut(conn, filename):
    if filename == ".":
        ssize = getRecv(conn, 1024)
        conn.send(createJSON('ok', 'ready to upload'))
        for i in range(int(ssize)):
            fff_name = getRecv(conn, 1024)
            conn.send(createJSON('ok', 'ready to upload'))
            with open(fff_name, 'wb') as f:
                data = conn.recv(1024)
                while True:
                    f.write(data)
                    conn.send(createJSON('ok', 'got part of file'))
                    data = conn.recv(1024)
                    if data.decode("utf-8") == "$end$":
                        print(str(fff_name)+' was uploaded')
                        break
        return
    else:
        status = getRecv(conn, 1024)
        if status == 'notOk':
            return
        else :
            conn.send(createJSON('ok', 'ready to upload'))
            with open(filename, 'wb') as f:
                data = conn.recv(1024)
                while True:
                    f.write(data)
                    conn.send(createJSON('ok', 'got part of file'))
                    data = conn.recv(1024)
                    if data.decode("utf-8") == "$end$":
                        print(str(filename)+' was uploaded')
                        break
            return
   ```
   
   Server mendapatkan filename. Jika proses meletakkan selesai akan mengirimkan pesan " was uploaded ".
   
   
   #### Tampilan Request dan Response :
   
   Isi folder client dan server sebelum request dijalankan
   
   ![3](https://github.com/PutriEndahP/PROGJAR_05111740000039/blob/master/tugas4/Screenshot/isi%20folder%20sebelum%20di%20run.jpg)
   
   1. Fitur ``` ls ```
   
   Request :
   
   - Menjalankan server.py terlebih dahulu.
   
   ![4](https://github.com/PutriEndahP/PROGJAR_05111740000039/blob/master/tugas4/Screenshot/Server%20dijalankan%20dgn%20port%202121.jpg)
   
   - Menginputkan request ls di client_ls.py 
   
   ![5](https://github.com/PutriEndahP/PROGJAR_05111740000039/blob/master/tugas4/Screenshot/client_ls%20dijalankan%20dgn%20port%202121.jpg)
   
   
   Response :
   
   - Client akan menampilkan list file yang ada di server
   
   ![6](https://github.com/PutriEndahP/PROGJAR_05111740000039/blob/master/tugas4/Screenshot/client_ls%20dijalankan%20dgn%20port%202121.jpg)
   
   - Kondisi server setelah Client_ls.py dijalankan
   
   ![7](https://github.com/PutriEndahP/PROGJAR_05111740000039/blob/master/tugas4/Screenshot/server%20setelah%20request%20ls.jpg)
   
   Quit client_ls.py
   
   ![8](https://github.com/PutriEndahP/PROGJAR_05111740000039/blob/master/tugas4/Screenshot/quit%20client_ls.jpg)
   
   
   2. Fitur ``` get ```
   
   Request :
   
   - Menjalankan client_get.py untuk meminta request.
   
   ![9](https://github.com/PutriEndahP/PROGJAR_05111740000039/blob/master/tugas4/Screenshot/client_get%20dijalankan%20dgn%20port%202121.jpg)
   
   Response :
   
   - Server setelah request get dijalankan
   
   ![10](https://github.com/PutriEndahP/PROGJAR_05111740000039/blob/master/tugas4/Screenshot/server%20setelah%20request%20get.jpg)
   
   - Isi folder client setelah get dijalankan
   
   ![11](https://github.com/PutriEndahP/PROGJAR_05111740000039/blob/master/tugas4/Screenshot/isi%20folder%20setelah%20run%20get.jpg)
   
   Quit client_get.py
   
   ![12](https://github.com/PutriEndahP/PROGJAR_05111740000039/blob/master/tugas4/Screenshot/quit%20client_get.jpg)
   
   3. Fitur ``` put ```
   
   Request :
   
   - Menjalankan client_put.py untuk memita request
   
   ![13](https://github.com/PutriEndahP/PROGJAR_05111740000039/blob/master/tugas4/Screenshot/client_put%20dijakankan%20dgn%20port%202121.jpg)
   
   Response :
   
   - Server setelah put dijalankan
   
   ![14](https://github.com/PutriEndahP/PROGJAR_05111740000039/blob/master/tugas4/Screenshot/server%20setelah%20request%20put.jpg)
   
   - Isi folder setelah put dijalankan
   
   ![15](https://github.com/PutriEndahP/PROGJAR_05111740000039/blob/master/tugas4/Screenshot/isi%20folder%20setelah%20run%20put.jpg)
   
   Quit client_put.py
   
   ![16](https://github.com/PutriEndahP/PROGJAR_05111740000039/blob/master/tugas4/Screenshot/quit%20client_put.jpg)
   


  
  



