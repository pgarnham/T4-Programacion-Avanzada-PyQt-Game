"""Archivo con funciones o utilidades."""

from hashlib import sha256
from threading import Thread
from os import urandom  # startfile
from PyQt5.QtGui import QPen, QPainter, QPainterPath
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import QObject, pyqtSignal, Qt
from time import sleep
from numpy import empty
import pickle
import socket
import json
from datetime import datetime
import random


# startfile("arcade_classic_pizz\ARCADECLASSIC.TTF")


# diccionario = {}
# with open("usuarios.txt", "bw") as file:
#     pickle.dump(diccionario, file)

HOST = "localhost"
PORT = 8084


def gensecuencia(password, salt):
    """Genera la secuencia a partir de la contraseña."""
    salt = urandom(8)
    b_password = password.encode()
    secuence = salt + b_password
    encriptado = sha256(secuence).digest()
    return encriptado, salt


def recuperar_secuencia(password, salt):
    """Recupera la secuencia para luego comparar."""
    b_pass = password.encode()
    secuence = salt + b_pass
    encriptado = sha256(secuence).digest()
    return encriptado


def crear_usuario(usuario, contrasena):
    """Funcion para crear un usuario."""
    sec, salt = gensecuencia(contrasena, None)
    with open("usuarios.txt", "br") as file:
        diccionario = pickle.load(file)
        diccionario[usuario] = (salt, sec)
    with open("usuarios.txt", "bw") as file:
        pickle.dump(diccionario, file)


def check_user_exist(usuario):
    """Revisa si existe el usuario."""
    with open("usuarios.txt", "rb") as file:
        diccionario = pickle.load(file)
        if usuario in diccionario.keys():
            return True
    return False


def check_correct_pass(user, contrasena):
    """Revisa que la contrasena sea correcta."""
    with open("usuarios.txt", "br") as file:
        diccionario = pickle.load(file)
        salt = diccionario[user][0]
        sec_o = diccionario[user][1]
    sec_i = recuperar_secuencia(contrasena, salt)
    if sec_o == sec_i:
        return True
    return False


class IniciarSesion(QObject):
    """docstring for IniciarSesion"""
    signal = pyqtSignal(bool)

    def __init__(self, parent):
        super().__init__()
        self.signal.connect(parent.jugar_method)

    def checkeos(self, lista):
        user = lista[0]
        password = lista[1]
        correcto = False
        if check_user_exist(user):
            if check_correct_pass(user, password):
                correcto = True
        self.signal.emit(correcto)


class RegistrarUsuario(QObject):
    """docstring for IniciarSesion"""
    signal = pyqtSignal(tuple)

    def __init__(self, parent):
        super().__init__()
        self.signal.connect(parent.iniciarse)

    def checkeos(self, tupla):
        user, pass_1, pass_2 = tupla
        existe = True
        correcto = False
        if not check_user_exist(user):
            existe = False
            if pass_1 == pass_2:
                crear_usuario(user, pass_1)
                correcto = True
        self.signal.emit((correcto, existe))


class PaintPath(QWidget):

    def __init__(self):
        QWidget.__init__(self)
        self._x = 17
        self._y = 17
        self.rumbo_fijo = (1, 1)
        self.direcciones = [(1, 4), (2, 3), (3, 2), (4, 1), (5, 0), (4, -1),
                            (3, -2), (2, -3), (1, -4), (0, -5), (-1, -4),
                            (-2, -3), (-3, -2), (-4, -1), (-5, 0), (-4, 1),
                            (-3, 2), (-2, 3), (-1, 4), (0, 5)]
        self._direccion = 0
        self.tarea = Thread(name="Thread 1", target=self.avanzar, daemon=True)
        self.tarea.start()
        self.anterior = (16, 16)
        self.actual = (17, 17)
        self.dimension = (488, 648)
        self.matrix = empty(self.dimension)
        self.path = QPainterPath()
        self.path.moveTo(16, 16)

    @property
    def direccion(self):
        return self._direccion

    @direccion.setter
    def direccion(self, arg):
        self._direccion = arg
        if self._direccion > 19:
            self._direccion = 0
        elif self._direccion < 0:
            self._direccion = 19

    def avanzar_curva(self, senal):
        """Metodo para que el personaje avance siempre."""
        if senal == "L":
            self.direccion -= 1
        elif senal == "R":
            self.direccion += 1
        tupla = self.direcciones[self.direccion]
        self.x += tupla[0]
        self.y += tupla[1]
        self.rumbo_fijo = self.direcciones[self.direccion]
        self.actual = (self.x, self.y)
        self.path.lineTo(self.actual[0], self.actual[1])
        self.path.moveTo(self.actual[0], self.actual[1])
        self.update()

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, arg):
        self._x = arg

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, arg):
        self._y = arg

    def avanzar(self):
        """Metodo para avanzar sin hacer una curva."""
        while True:
            sleep(0.05)
            self.x += self.rumbo_fijo[0]
            self.y += self.rumbo_fijo[1]
            self.actual = (self.x, self.y)
            self.path.lineTo(self.actual[0], self.actual[1])
            self.path.moveTo(self.actual[0], self.actual[1])
            self.update()

    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        # lista_colores = [Qt.yellow, Qt.black, Qt.blue, Qt.red, Qt.lightGray]
        # color_elegido = random.choice(lista_colores)
        pen = QPen(Qt.red, 10, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin)
        qp.setPen(pen)
        qp.setRenderHint(QPainter.Antialiasing)
        qp.drawPath(self.path)
        qp.end()


class Cliente(QObject):
    signal_actualizar = pyqtSignal(str)
    senal_clientes = pyqtSignal(list)
    senal_poderes = pyqtSignal(list)
    senal_velocidad = pyqtSignal(int)
    senal_puntaje = pyqtSignal(int)
    senal_jefe = pyqtSignal(bool)
    senal_jugar = pyqtSignal(list)
    senal_contar = pyqtSignal(bool)
    '''
    Esta es la clase encargada de conectarse con el
     servidor e intercambiar información
    '''

    def __init__(self, parent):
        super().__init__()
        self.socket_cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.parent = parent
        self.senal_jefe.connect(self.parent.elegir_ventana)
        self.host = HOST
        self.port = PORT
        try:
            self.socket_cliente.connect((self.host, self.port))
            print("Cliente conectado exitosamente al servidor")

            self.conectado = True

            escuchar_server = Thread(target=self.escuchar, daemon=True)
            escuchar_server.start()
            print("Escuchando al servidor...")

        except ConnectionRefusedError:
            self.terminar_conexion()

    def conectar_parent(self):
        """Conectar al parent."""
        self.signal_actualizar.connect(self.parent.actualizar_chat)
        self.senal_clientes.connect(self.parent.actualizar_clientes)
        self.senal_poderes.connect(self.parent.actualizar_poderes)
        self.senal_velocidad.connect(self.parent.actualizar_velocidad)
        self.senal_puntaje.connect(self.parent.actualizar_puntaje)
        self.senal_jugar.connect(self.parent.jugar)
        self.senal_contar.connect(self.parent.cuenta_regresiva)

    def escuchar(self):
        '''
        Este método es usado en el thread y la idea es que reciba lo que
        envía el servidor. Implementa el protocolo de agregar los primeros
        4 bytes, que indican el largo del mensaje
        '''
        print("estamos escuchando")
        while self.conectado:
            try:
                # Recibimos los 4 bytes del largo
                largo_msj_byt = self.socket_cliente.recv(4)
                largo_mensaje = int.from_bytes(largo_msj_byt, byteorder="big")

                contenido_mensaje_bytes = bytearray()

                # Recibimos el resto de los datos
                while len(contenido_mensaje_bytes) < largo_mensaje:
                    contenido_mensaje_bytes += self.socket_cliente.recv(256)

                # Decodificamos y pasamos a pickle el mensaje
                contenido_mensaje = contenido_mensaje_bytes.decode("utf-8")
                mensaje_decodificado = json.loads(contenido_mensaje)

                # Manejamos el mensaje
                self.manejar_comando(mensaje_decodificado)

            except ConnectionResetError:
                self.terminar_conexion()

    def manejar_comando(self, diccionario):
        '''
        Este método toma el mensaje decodificado de la forma:
        {"status": tipo del mensaje, "data": información}
        '''
        if diccionario["status"] == "mensaje":
            data = diccionario["data"]
            user = data["usuario"]
            cont = data["contenido"]
            user = f"({datetime.now().hour}:{datetime.now().minute}) {user}"
            self.signal_actualizar.emit(f"{user}: {cont}")

        if diccionario["status"] == "usuarios":
            self.senal_clientes.emit(diccionario["data"])
            if len(diccionario["data"]) == 1:
                self.senal_jefe.emit(True)
            else:
                self.senal_jefe.emit(False)
            self.lista_usuarios = diccionario["data"]

        if diccionario["status"] == "nuevo_poder":
            self.senal_poderes.emit(diccionario["data"])

        if diccionario["status"] == "cambio_velocidad":
            self.senal_velocidad.emit(diccionario["data"])

        if diccionario["status"] == "cambio_puntaje":
            self.senal_puntaje.emit(diccionario["data"])

        if diccionario["status"] == "queremos_jugar":
            self.senal_jugar.emit(self.lista_usuarios)

        if diccionario["status"] == "vamos_a_contar":
            self.senal_contar.emit(True)

    def send(self, mensaje):
        '''
        Este método envía la información al servidor.
        Recibe un mensaje del tipo:
        {"status": tipo del mensaje, "data": información}
        '''
        # Codificamos y pasamos a bytes
        mensaje_codificado = json.dumps(mensaje)
        cont_msj_byt = mensaje_codificado.encode("utf-8")

        # Tomamos el largo del mensaje y creamos 4 bytes de esto
        len_msj_byt = len(cont_msj_byt).to_bytes(4, byteorder="big")
        # Enviamos al servidor
        self.socket_cliente.send(len_msj_byt + cont_msj_byt)

    def terminar_conexion(self):
        print("Conexión terminada")
        self.connected = False
        self.socket_cliente.close()
        exit()
