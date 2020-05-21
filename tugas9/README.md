## Tugas 9

#### Jalankan kedua model tersebut
   * Server_async_http.py di port 45000
   * Server_thread_http.py di port 46000
#### Ujicobalah dengan apache benchmark untuk 1000 request dan konkurensi yang bervariasi
   * Jumlah Request     : 1000
   * Konkurensi         : 1,2,3,4
## Hasil Server Async : port 45000
![teks alt gambar](https://github.com/lutfiyanti/PROGJAR_05111740000036/blob/master/tugas9/Screenshot/async_hasil.JPG)
## Hasil Server Thread : 46000
![teks alt gambar](https://github.com/lutfiyanti/PROGJAR_05111740000036/blob/master/tugas9/Screenshot/thread_hasil.JPG)

#### Kesimpulan
Hasil test dari performance test pada tabel di atas menunjukkan bahwa menggunakan asynchronous server alokasi memory dan cpu akan lebih efisien. Sedangkan jika menggunakan server thread bila semakin banyak client yang melakukan request semakin banyak CPU time yang dibutuhkan dan penggunaan memory juga meningkat.
