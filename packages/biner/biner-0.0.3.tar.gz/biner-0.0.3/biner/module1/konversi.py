# FUNGSI 1
def biner_to_integer(n: int) -> int:
    """
    Mengonversi bilangan biner dalam bentuk integer menjadi bilangan bulat (desimal).

    Parameter:
    biner (int): Bilangan biner dalam bentuk integer. Contoh: 1011

    Return:
    int: Bilangan bulat hasil konversi dari bilangan biner.

    Contoh:
    >>> konversi_biner_ke_desimal(1011)
    11
    """
    return int(str(n), 2)
  

# FUNGSI 2
def integer_to_biner(n: int) -> str:
    """
    Membulatkan angka desimal ke bilangan bulat terdekat dan
    mengonversinya menjadi bilangan biner dalam bentuk string dengan minimal 4 digit (padding dengan leading zeroes jika diperlukan).

    Parameter:
    - integer (int): Bilangan desimal yang akan dibulatkan dan dikonversi.

    Mengembalikan:
    - str: Representasi biner dari bilangan bulat hasil pembulatan
      tanpa prefiks '0b', dikembalikan sebagai string dengan minimal 4 digit.
    """
    bulat = round(n)
    biner = bin(bulat)[2:]  # Menghapus '0b' dari hasil biner
    biner_berpadding = biner.zfill(4)  # Menambahkan padding leading zero jika kurang dari 4 digit
    return biner_berpadding