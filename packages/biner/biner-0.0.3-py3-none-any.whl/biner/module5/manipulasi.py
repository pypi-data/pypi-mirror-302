def shift_bit(n: int, jumlah_pergeseran: int, arah: str) -> str:
    """
    Menggeser bit dari bilangan bulat ke kiri atau kanan dengan jumlah pergeseran yang ditentukan,
    dan mengembalikan hasil dengan padding minimal 4 digit biner.

    Args:
    - a (int): Bilangan bulat yang akan digeser.
    - jumlah_pergeseran (int): Jumlah bit yang akan digeser.
    - arah (str): Arah pergeseran, 'kiri' atau 'kanan'.

    Returns:
    - str: Representasi biner hasil pergeseran dengan minimal 4 digit.
    """
    arah = arah.lower()

    if arah == 'kiri':
        hasil_shift = n << jumlah_pergeseran
    elif arah == 'kanan':
        hasil_shift = n >> jumlah_pergeseran
    else:
        raise ValueError("Arah pergeseran harus 'kiri' atau 'kanan'.")
    
    return bin(hasil_shift)[2:].zfill(4)  # Menghilangkan '0b' dan menambahkan padding minimal 4 digit



def inverse_bit(n):
	biner_a = bin(n)[2: ]
	# print(f'Bilangan biner: {biner_a}')
	# # pada bagian ini, bilangan bulat akan diubah ke bilangan biner terlebih dahulu. Jika
	# # bilangannya sudah menjadi biner, maka bilangan tersebut langsung keluar
	bits = biner_a
	# variabel baru untuk membalikkan bilangan biner
	inverse = ''
	# Sengaja dikasi string kosong agar dapat menyimpan hasil inverse biner tadi

	for i in bits:
	# melakukan perulangan tergantung dari jumlah bilangan binernya

		if i == '0':
			inverse += '1'
		# kalau bilangan binernya adalah 0, maka yang disimpan di variabel inverse adalah 1
			
		else:
			inverse += '0'
		# kalau bilangan binernya adalah 1, maka yang disimpan di variabel inverse adalah 1
			
	return (inverse)
