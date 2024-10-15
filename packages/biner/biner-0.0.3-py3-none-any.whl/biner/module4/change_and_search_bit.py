# FUNGSI 1
def ganti_bit(n: int, posisi: int, nilai: int) -> str:
    """
    Mengganti bit pada posisi tertentu di angka dengan nilai (0 atau 1), mengembalikan hasil dengan minimal 4 digit biner.
    
    Args:
    angka (int): Angka target
    posisi (int): Posisi bit yang ingin diganti (dimulai dari 0)
    nilai (int): Nilai bit yang baru (0 atau 1)
    
    Returns:
    str: Angka baru setelah bit diganti dalam bentuk biner dengan minimal 4 digit
    """
    mask = 1 << posisi
    if nilai == 1:
        hasil = n | mask  # Set bit to 1
    else:
        hasil = n & ~mask  # Set bit to 0
    return bin(hasil)[2:].zfill(4)  # Menghilangkan '0b' dan menambahkan padding 4 digit


# FUNGSI 2
def cari_bit(n: int, posisi: int) -> str:
    """
    Mencari nilai bit pada posisi tertentu di angka, mengembalikan hasil dengan minimal 4 digit biner.
    
    Args:
    angka (int): Angka target
    posisi (int): Posisi bit yang ingin dicari (dimulai dari 0)
    
    Returns:
    str: Nilai bit (0 atau 1) dalam bentuk biner dengan minimal 4 digit
    """
    bit = (n >> posisi) & 1
    return bin(bit)[2:].zfill(4)  # Menghilangkan '0b' dan menambahkan padding 4 digit