
import csv
from hashlib import sha256
import numpy as np


def recuperar_secuencia(password, salt):
    """Recupera la secuencia para luego comparar."""
    b_pass = password.encode()
    secuence = salt + b_pass
    encriptado = sha256(secuence).digest()
    return encriptado


def check_correct_pass(user, contrasena):
    """Revisa que la contrasena sea correcta."""
    with open("usuarios.csv", "r") as file:
        dicties = csv.DictReader(file)
        for dicc in dicties:
            if dicc["usuario"] == user:
                salt = dicc["sal"]
                salt = bytes(salt, encoding='utf-8')
                print(salt)
                sec_o = dicc["password"]       
                break
    sec_i = recuperar_secuencia(contrasena, salt)
    if sec_o == sec_i:
        return True
    return False

dimensiones = (488, 648)
matrix = np.zeros(dimensiones)
print(matrix)
print(" ")
matrix[0][0] = 1
print(matrix)
