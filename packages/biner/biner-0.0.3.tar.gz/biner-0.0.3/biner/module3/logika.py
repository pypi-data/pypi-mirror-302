# FUNGSI 1
def operasi_and(n1: int, n2: int) -> str:
    """
    Melakukan operasi bitwise AND antara dua bilangan bulat, kemudian mengembalikan hasilnya dalam bentuk biner dengan padding minimal 4 bit.

    Parameter:
    n1 (int): Bilangan bulat pertama.
    n2 (int): Bilangan bulat kedua.

    Return:
    str: Hasil operasi AND dalam format biner minimal 4 bit.
    """
    hasil_and = n1 & n2
    return format(hasil_and, '04b')  # Mengembalikan hasil dalam format biner dengan padding minimal 4 bit



# FUNGSI 2
def operasi_or(n1: int, n2: int) -> str:
    """
    Melakukan operasi bitwise OR antara dua bilangan bulat, kemudian mengembalikan hasilnya dalam bentuk biner dengan padding minimal 4 bit.

    Parameter:
    n1 (int): Bilangan bulat pertama.
    n2 (int): Bilangan bulat kedua.

    Return:
    str: Hasil operasi OR dalam format biner minimal 4 bit.
    """
    hasil_or = n1 | n2
    return format(hasil_or, '04b')  # Mengembalikan hasil dalam format biner dengan padding minimal 4 bit


# FUNGSI 3
def operasi_xor(n1: int, n2: int) -> str:
    """
    Melakukan operasi bitwise XOR antara dua bilangan bulat, kemudian mengembalikan hasilnya dalam bentuk biner dengan padding minimal 4 bit.

    Parameter:
    n1 (int): Bilangan bulat pertama.
    n2 (int): Bilangan bulat kedua.

    Return:
    str: Hasil operasi XOR dalam format biner minimal 4 bit.
    """
    hasil_xor = n1 ^ n2
    return format(hasil_xor, '04b')  # Mengembalikan hasil dalam format biner dengan padding minimal 4 bit
