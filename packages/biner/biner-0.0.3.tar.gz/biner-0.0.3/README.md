## PACKAGE BINER ##

Package Biner merupakan sebuah package yang dirancang khusus untuk mengubah suatu bilangan bulat ke bilangan biner. Fungsi ini juga dapat menganalisis bilangan biner dan melakukan operasi penjumlahan dan logika dasar dengan bilangan biner. Dengan fungsi ini, pengguna dapat dengan mudah mengonversi dan menganalisis serta melakukan operasi penjumlahan dan logika dasar bilangan biner.

## FITUR UTAMA ##
1.  Module 1 adalah Konversi bilangan. 
    Fungsi ini bertujuan untuk mengonversi bilangan bulat ke biner dan sebaliknya.

2.  Module 2 adalah Operasi Dasar Bilangan Biner. 
    Fungsi ini dapat melakukan operasi penjumlahan, pengurangan, perkalian, dan pembagian dengan menginputkan bilangan bulat kemudian mengoperasikan bilangan biner dari  
    bilangan bulat yang dimasukkan.

3.  Module 3 adalah Operasi logika. 
    Fungsi ini dapat mengoperasikan bilangan biner menggunakan AND, OR, dan XOR.

4.  Module 4 adalah penggantian dan pencarian. 
    Fungsi ini dapat mencari dan mengganti bagian dari representasi biner, seperti mengganti bit tertentu dengan nilai baru.

5.  Module 5 adalah Manipulasi Bit. 
    Fungsi ini dapat melakukan operasi manipulasi Bit, seperti penggeseran dan pembalikan.

6.  Module 6 adalah Analisis dan Statistik. 
    Fungsi ini dapat menganalisis bilangan biner, seperti menghitung jumlah bit yang disetel.

## INSTALASI ##
Langkah-langkah Install Package biner di Pip

1. Pastikan Python dan Pip Terinstal
Sebelum menginstall package, pastikan Anda sudah menginstal Python dan pip di sistem Anda. Untuk memeriksa apakah sudah terinstal, buka terminal atau command prompt dan jalankan perintah berikut:
```
python --version
pip --version
```

2. Install Package biner
Setelah memastikan Python dan pip sudah terpasang, Anda dapat menginstall package biner dengan perintah berikut di terminal:
```
pip install biner
```

3. Verifikasi Installasi
Setelah proses instalasi selesai, Anda bisa memverifikasi apakah package biner sudah terinstal dengan menjalankan perintah berikut:
```
pip show biner
```

## CARA PENGGUNAAN ##
Untuk menggunakan package ini, pastikan Anda sudah mengimpor package biner ke dalam kode Python Anda:
```
import biner
```
1. Modul Konversi
Modul ini menyediakan fungsi untuk mengonversi bilangan biner ke integer dan bilangan bulat ke biner.

Fungsi:
  - biner_to_integer(n)
  - integer_to_biner(n)
    
Contoh penggunaan:
```
hasil = biner.biner_to_integer(1101)
print(hasil)  # Output: 13
```

2. Modul Operasi
Modul ini menyediakan fungsi untuk operasi aritmatika dasar pada bilangan biner yang dihasilkan dari bilangan bulat.
Fungsi:

  - operasi_tambah(n1, n2)
  - operasi_kurang(n1, n2)
  - operasi_kali(n1, n2)
  - operasi_bagi(n1, n2)

contoh penggunaan:
```
hasil = biner.operasi_tambah(4,2)
print(hasil)  # Output: 0110
```

3. Modul Operasi Logika
Modul ini menyediakan fungsi untuk operasi logika pada bilangan biner.

Fungsi:
  - operasi_and(n1, n2)
  - operasi_or(n1, n2)
  - operasi_xor(n1, n2)

contoh penggunaan:
```
hasil = biner.operasi_and(13, 15)
print(hasil)   # output : 1101
```

4. Modul Ganti dan Cari Bit
Modul ini menyediakan fungsi untuk mengganti dan mencari bit pada posisi tertentu.

Fungsi:
  - ganti_bit(n, posisi, nilai)
  - cari_bit(n, posisi)

contoh penggunaan:
```
hasil = biner.ganti_bit(10, 2, 1)
print(hasil)   # output : 1110
```

5. Modul Manipulasi
Modul ini menyediakan fungsi untuk manipulasi bit seperti shift dan inverse.

Fungsi:
  - shift_bit(n, jumlah_pergeseran, arah)
  - inverse_bit(n)

contoh penggunaan:
```
hasil = biner.shift_bit(10,2,"kanan")
print(hasil)   # output : 0010
```

6. Modul Analisis
Modul ini menyediakan fungsi untuk analisis bit seperti menghitung jumlah bit yang disetel, panjang bit, dan lainnya.

Fungsi:
  - setbits(n)
  - unsetbits(n)
  - bitlength(n)
  - parity(n)
  - hamming(n1, n2)

contoh penggunaan:
```
hasil = biner.setbits(10)
print(hasil)   # output : 2
```








