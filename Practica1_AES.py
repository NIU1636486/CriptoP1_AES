import numpy as np
import pandas as pd

# MATRIUS AUXILIARS

sbox = [
        [0x63, 0x7c, 0x77, 0x7b, 0xf2, 0x6b, 0x6f, 0xc5, 0x30, 0x01, 0x67, 0x2b, 0xfe, 0xd7, 0xab, 0x76],
        [0xca, 0x82, 0xc9, 0x7d, 0xfa, 0x59, 0x47, 0xf0, 0xad, 0xd4, 0xa2, 0xaf, 0x9c, 0xa4, 0x72, 0xc0],
        [0xb7, 0xfd, 0x93, 0x26, 0x36, 0x3f, 0xf7, 0xcc, 0x34, 0xa5, 0xe5, 0xf1, 0x71, 0xd8, 0x31, 0x15],
        [0x04, 0xc7, 0x23, 0xc3, 0x18, 0x96, 0x05, 0x9a, 0x07, 0x12, 0x80, 0xe2, 0xeb, 0x27, 0xb2, 0x75],
        [0x09, 0x83, 0x2c, 0x1a, 0x1b, 0x6e, 0x5a, 0xa0, 0x52, 0x3b, 0xd6, 0xb3, 0x29, 0xe3, 0x2f, 0x84],
        [0x53, 0xd1, 0x00, 0xed, 0x20, 0xfc, 0xb1, 0x5b, 0x6a, 0xcb, 0xbe, 0x39, 0x4a, 0x4c, 0x58, 0xcf],
        [0xd0, 0xef, 0xaa, 0xfb, 0x43, 0x4d, 0x33, 0x85, 0x45, 0xf9, 0x02, 0x7f, 0x50, 0x3c, 0x9f, 0xa8],
        [0x51, 0xa3, 0x40, 0x8f, 0x92, 0x9d, 0x38, 0xf5, 0xbc, 0xb6, 0xda, 0x21, 0x10, 0xff, 0xf3, 0xd2],
        [0xcd, 0x0c, 0x13, 0xec, 0x5f, 0x97, 0x44, 0x17, 0xc4, 0xa7, 0x7e, 0x3d, 0x64, 0x5d, 0x19, 0x73],
        [0x60, 0x81, 0x4f, 0xdc, 0x22, 0x2a, 0x90, 0x88, 0x46, 0xee, 0xb8, 0x14, 0xde, 0x5e, 0x0b, 0xdb],
        [0xe0, 0x32, 0x3a, 0x0a, 0x49, 0x06, 0x24, 0x5c, 0xc2, 0xd3, 0xac, 0x62, 0x91, 0x95, 0xe4, 0x79],
        [0xe7, 0xc8, 0x37, 0x6d, 0x8d, 0xd5, 0x4e, 0xa9, 0x6c, 0x56, 0xf4, 0xea, 0x65, 0x7a, 0xae, 0x08],
        [0xba, 0x78, 0x25, 0x2e, 0x1c, 0xa6, 0xb4, 0xc6, 0xe8, 0xdd, 0x74, 0x1f, 0x4b, 0xbd, 0x8b, 0x8a],
        [0x70, 0x3e, 0xb5, 0x66, 0x48, 0x03, 0xf6, 0x0e, 0x61, 0x35, 0x57, 0xb9, 0x86, 0xc1, 0x1d, 0x9e],
        [0xe1, 0xf8, 0x98, 0x11, 0x69, 0xd9, 0x8e, 0x94, 0x9b, 0x1e, 0x87, 0xe9, 0xce, 0x55, 0x28, 0xdf],
        [0x8c, 0xa1, 0x89, 0x0d, 0xbf, 0xe6, 0x42, 0x68, 0x41, 0x99, 0x2d, 0x0f, 0xb0, 0x54, 0xbb, 0x16]
        ]


rcon = np.array(
    [[0x01, 0x00, 0x00, 0x00],
     [0x02, 0x00, 0x00, 0x00],
     [0x04, 0x00, 0x00, 0x00],
    [0x08, 0x00, 0x00, 0x00],
    [0x10, 0x00, 0x00, 0x00],
    [0x20, 0x00, 0x00, 0x00],
    [0x40, 0x00, 0x00, 0x00],
    [0x80, 0x00,0x00, 0x00],
    [0x1b, 0x00,0x00, 0x00],
    [0x36, 0x00, 0x00, 0x00],])


# FUNCIONS AUXILIARS
def hex_to_dec(cadena):
    decimal_array = [int(hex_number, 16) for hex_number in cadena]
    return np.array(decimal_array)

def dec_to_hex(llista):
    original_text = [(hex(c)[:2]+hex(c)[2:].zfill(2)) for c in llista]
    return np.array(original_text)

def printHex(val):
    return print('{:02x}'.format(val), end=' ')

def print_matrix_in_hex(matrix):
    for i in range(matrix.shape[0]):
        for j in range(matrix.shape[1]):
            printHex(matrix[i][j])
        print()

# FUNCIONS AES

def sub_bytes(state):
    llista = []
    for value in state:
    
        if value[-2] == "x":
            j = 0
        else:
            j = int(value[-2], 16)

        i = int(value[-1], 16)
        value = sbox[j][i]
    
        llista.append(value)
    return llista



def shift_rows(matrix):
    for i in range(matrix.shape[0]):
        matrix[i] = np.roll(matrix[i], -i)
    return matrix




def mul_mixColumns(a, b, c, d):
    # copiat i modificat de stack overflow
    col_final = np.zeros(4 , dtype = 'int64')
    col_final[0] = (gmul(a, 2) ^ gmul(b, 3) ^ gmul(c, 1) ^ gmul(d, 1))
    col_final[1] = (gmul(a, 1) ^ gmul(b, 2) ^ gmul(c, 3) ^ gmul(d, 1))
    col_final[2] = (gmul(a, 1) ^ gmul(b, 1) ^ gmul(c, 2) ^ gmul(d, 3))
    col_final[3] = (gmul(a, 3) ^ gmul(b, 1) ^ gmul(c, 1) ^ gmul(d, 2))

    return col_final

def gmul(a, b):
    if b == 1:
        return a
    tmp = (a << 1) & 0xff
    if b == 2:
        return tmp if a < 128 else tmp ^ 0x1b
    if b == 3:
        return gmul(a, 2) ^ a



def mixColumns(original_matrix):
    for i in range(original_matrix.shape[1]):
        columna = original_matrix[:,i]
        original_matrix[:,i] = mul_mixColumns(columna[0],columna[1],columna[2],columna[3])
    return original_matrix


def AddRoundKey(shift, key):
    return shift^key


def key_schedule(clau, iter ):
    matrix_key_schedule = np.zeros((4,4))
    columna_ult = clau[:,3]
    col =  np.roll(columna_ult, -1)
    col_subbytes = (sub_bytes((col)))
    col = (col_subbytes ) ^ (rcon[iter]) ^ (hex_to_dec (clau[:,0]))

    matrix_key_schedule[:,0]= (col)
    for i in range (1,4):
        matrix_key_schedule[:,i] =  (matrix_key_schedule[:,i-1].astype(int))^hex_to_dec(clau[:,i])
    nova_matrix_key_schedule = [[0]*4 for i in range(4)]
    for i in range (4):
        for j in range (4):
            nova_matrix_key_schedule[i][j] = int(matrix_key_schedule[i][j])
    return np.array(nova_matrix_key_schedule)



# # MAIN

def encriptar_aes(input_str: str, clau):
    original_text = [hex(ord(c)) for c in input_str]
    original_text = np.array(original_text).reshape(4, 4)
    print("---INPUT---\n")
    print(original_text)

 
    clau_hex = [hex((c)) for c in clau]
    clau = np.array(clau_hex).reshape(4, 4)
    print("\n---CLAU---\n")
    print(clau)
    # print(clau)

    #   ROUND 0
    array = AddRoundKey(hex_to_dec(original_text.flatten()), hex_to_dec(clau.flatten()))
    

    # print("ROUND 0")

    # ROUND 1 - 9 


    for i in range (9):
        matriu= dec_to_hex(array)
        llista = sub_bytes(matriu)
        matriu = np.array(llista).reshape(4, 4)
        matriu = shift_rows(matriu)
        matriu = mixColumns(matriu)
        matriu_key_schedule = key_schedule(clau, i)
        clau = matriu_key_schedule.flatten()

        array = AddRoundKey(matriu.flatten(), clau)
        clau_hex = [hex((c)) for c in clau]
        clau = np.array(clau_hex).reshape(4, 4)
        matriu = np.array(array).reshape(4, 4)

    # ROUND 10
    llista = sub_bytes(dec_to_hex(array))
    matriu = np.array(llista).reshape(4, 4)
    matriu = shift_rows(matriu)
    matriu_key_schedule = key_schedule(clau, i+1)
    clau = matriu_key_schedule.flatten()
    array = AddRoundKey(matriu.flatten(), clau)
    matriu = np.array(array).reshape(4, 4)
    matriu = dec_to_hex(array).reshape(4, 4)
    print("\n\n")
    print("---OUTPUT---\n")
    print(matriu)

if __name__ == "__main__":
    clau = np.array([43, 40, 171, 9,
        126, 174, 247, 207,
        21, 210, 21, 79,
        22, 166, 136, 60])
    encriptar_aes("PolRiuXiscaCompa", clau)