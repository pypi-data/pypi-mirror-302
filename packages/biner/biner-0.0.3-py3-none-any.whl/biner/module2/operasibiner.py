#FUNGSI 1
def operasi_tambah(n1: int, n2: int) -> str:
    """
    Menambahkan dua bilangan bulat dan mengembalikan hasilnya dalam bentuk biner dengan minimal 4 digit.

    Args:
        n1 (int): Bilangan bulat pertama.
        n2 (int): Bilangan bulat kedua.

    Returns:
        str: Hasil penjumlahan n1 dan n2 dalam bentuk biner dengan padding minimal 4 digit.
    """
    hasil = bin(n1 + n2)[2:]  # Mengubah hasil penjumlahan ke biner tanpa '0b'
    return hasil.zfill(4)     # Menambahkan padding minimal 4 digit


#FUNGSI 2
def operasi_kurang(n1: int, n2: int) -> str:
    """
    Mengurangkan dua bilangan bulat dan mengembalikan hasilnya dalam bentuk biner dengan minimal 4 digit.

    Args:
        n1 (int): Bilangan bulat pertama.
        n2 (int): Bilangan bulat kedua.

    Returns:
        str: Hasil pengurangan n1 dan n2 dalam bentuk biner dengan padding minimal 4 digit.
    """
    hasil = bin(n1 - n2)[2:]  # Mengubah hasil pengurangan ke biner tanpa '0b'
    return hasil.zfill(4)     # Menambahkan padding minimal 4 digit


# FUNGSI 3
def operasi_kali(n1: int, n2: int) -> str:
    """
    Mengalikan dua bilangan bulat dan mengembalikan hasilnya dalam bentuk biner dengan minimal 4 digit.

    Args:
        n1 (int): Bilangan bulat pertama.
        n2 (int): Bilangan bulat kedua.

    Returns:
        str: Hasil perkalian n1 dan n2 dalam bentuk biner dengan padding minimal 4 digit.
    """
    hasil = bin(n1 * n2)[2:]  # Mengubah hasil perkalian ke biner tanpa '0b'
    return hasil.zfill(4)     # Menambahkan padding minimal 4 digit


# FUNGSI 4
def operasi_bagi(n1: int, n2: int) -> str:
    """
    Membagi dua bilangan bulat dan mengembalikan hasilnya dalam bentuk biner dengan minimal 4 digit.

    Args:
        n1 (int): Bilangan bulat pembilang.
        n2 (int): Bilangan bulat penyebut.

    Returns:
        str: Hasil pembagian n1 dan n2 dalam bentuk biner dengan padding minimal 4 digit.
    """
    hasil = bin(n1 // n2)[2:]  # Mengubah hasil pembagian ke biner tanpa '0b'
    return hasil.zfill(4)      # Menambahkan padding minimal 4 digit
