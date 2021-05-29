import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import pyqtSignal, Qt
from funciones import IniciarSesion, PaintPath, RegistrarUsuario, Cliente
from time import sleep
from datetime import datetime, timedelta

dir_1 = "qtdesigner/bienvenida.ui"
dir_2 = "qtdesigner/iniciar_sesion.ui"
dir_3 = "qtdesigner/crear_usuario.ui"
dir_4 = "qtdesigner/juego.ui"
dir_sala_1 = "qtdesigner/sala_de_espera.ui"
dir_sala_2 = "qtdesigner/sala_comun.ui"
dir_error = "qtdesigner/mensaje_alerta.ui"
nombre_alerta, clase_alerta = uic.loadUiType(dir_error)
nombre_bienvenida, clase_bienvenida = uic.loadUiType(dir_1)
nombre_ingresar, clase_ingresar = uic.loadUiType(dir_2)
nombre_registrar, clase_registrar = uic.loadUiType(dir_3)
nombre_juego, clase_juego = uic.loadUiType(dir_4)
nombre_sala_1, clase_sala_1 = uic.loadUiType(dir_sala_1)
nombre_sala_2, clase_sala_2 = uic.loadUiType(dir_sala_2)


class VentanaBienvenida(nombre_bienvenida, clase_bienvenida):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.boton_ingresar.clicked.connect(self.ingresar)
        self.boton_registrarse.clicked.connect(self.registrar)

    def ingresar(self):
        """Metodo para ingresar con usuario existente."""
        self.hide()
        self.ventana_ingresar = VentanaIngresar()
        self.ventana_ingresar.show()

    def registrar(self):
        """Metodo para ingresar con usuario existente."""
        self.hide()
        self.ventana_registrar = VentanaRegistrar()
        self.ventana_registrar.show()


class VentanaIngresar(nombre_ingresar, clase_ingresar):
    senal = pyqtSignal(list)
    server_signal_2 = pyqtSignal(dict)

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.volver.clicked.connect(self.volver_method)
        self.iniciar.clicked.connect(self.iniciar_method)
        self.iniciar_backend = IniciarSesion(self)
        self.senal.connect(self.iniciar_backend.checkeos)
        self.ch_check.stateChanged.connect(self.state_changed)
        self.usuario = None
        self.abierto = False

    def state_changed(self, int):
        if self.ch_check.isChecked():
            self.pass_in.setEchoMode(self.pass_in.Normal)
        elif not self.ch_check.isChecked():
            self.pass_in.setEchoMode(self.pass_in.Password)

    def volver_method(self):
        """Metodo para volver a la bienvenida."""
        self.hide()
        self.ventana_bienvenida = VentanaBienvenida()
        self.ventana_bienvenida.show()

    def iniciar_method(self):
        """Metodo que se activa para ingresar."""
        self.usuario = self.usuario_ingresado.text()
        contrasena = self.pass_in.text()
        self.senal.emit([self.usuario, contrasena])

    def jugar_method(self, event):
        """Metodo para entrar al juego."""
        if event:
            self.hide()
            self.cliente = Cliente(self)
            self.server_signal_2.connect(self.cliente.send)
            mensaje = {"status": "nuevo_usuario",
                       "data": {"usuario": self.usuario}}
            self.server_signal_2.emit(mensaje)

        else:
            self.error = VentanaAlerta()
            msje = "DATOS INCORRECTOS" + "\n" + "INGRESE NUEVAMENTE"
            self.error.definir_mensaje(msje)
            self.error.show()

    def elegir_ventana(self, event):
        """Metodo para elegir sala de espera."""
        if not self.abierto:
            if event:
                self.sala = SalaEsperaJ(self.usuario, self.cliente)
                self.sala.show()
                self.sala.cambiar_parent()
                self.sala.client.conectar_parent()
                self.abierto = True
            else:
                self.sala = SalaEsperaC(self.usuario, self.cliente)
                self.sala.show()
                self.sala.cambiar_parent()
                self.sala.client.conectar_parent()
                self.abierto = True


class VentanaRegistrar(nombre_registrar, clase_registrar):
    senal = pyqtSignal(tuple)

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.volver.clicked.connect(self.volver_method)
        self.ch_check.stateChanged.connect(self.state_changed)
        self.registrar_backend = RegistrarUsuario(self)
        self.senal.connect(self.registrar_backend.checkeos)
        self.crear_usuario.clicked.connect(self.registrar_method)

    def state_changed(self, int):
        if self.ch_check.isChecked():
            self.pass_1.setEchoMode(self.pass_1.Normal)
            self.pass_2.setEchoMode(self.pass_1.Normal)
        elif not self.ch_check.isChecked():
            self.pass_1.setEchoMode(self.pass_1.Password)
            self.pass_2.setEchoMode(self.pass_1.Password)

    def volver_method(self):
        """Metodo para volver a la bienvenida."""
        self.hide()
        self.ventana_bienvenida = VentanaBienvenida()
        self.ventana_bienvenida.show()

    def registrar_method(self):
        """Metodo para registrar."""
        tupla = (self.usuario_nuevo.text(), self.pass_1.text(),
                 self.pass_2.text())
        self.senal.emit(tupla)

    def iniciarse(self, event):
        """Metodo para volver a iniciar, luego de registrarse."""
        if event == (True, False):
            self.hide()
            self.ventana_ingresar = VentanaIngresar()
            self.ventana_ingresar.show()
        elif event == (False, False):
            self.error = VentanaAlerta()
            msje = "CLAVES  NO  COINCIDEN" + "\n" + "CORRIJA..."
            self.error.definir_mensaje(msje)
            self.error.show()
        elif event == (False, True):
            self.error = VentanaAlerta()
            msje = "USUARIO YA EXISTE" + "\n" + "ELIJA OTRO"
            self.error.definir_mensaje(msje)
            self.error.show()
        elif event == (True, True):
            self.error = VentanaAlerta()
            msje = "USUARIO YA EXISTE" + "\n" + "ELIJA OTRO"
            self.error.definir_mensaje(msje)
            self.error.show()


class VentanaJuego(nombre_juego, clase_juego):
    senal = pyqtSignal(str)

    def __init__(self, lista, cliente):
        super().__init__()
        self.setupUi(self)
        self.lista_jugadores = lista
        self.client = cliente
        self.paint = PaintPath()
        self.senal.connect(self.paint.avanzar_curva)
        self.juego_layout.addWidget(self.paint)
        self.actualizar_users()

    def actualizar_users(self):
        """Actualiza los labels."""
        self.usuario_1.setText(self.lista_jugadores[0])
        if len(self.lista_jugadores) >= 2:
            self.usuario_2.setText(self.lista_jugadores[1])
        if len(self.lista_jugadores) >= 3:
            self.usuario_3.setText(self.lista_jugadores[2])
        if len(self.lista_jugadores) == 4:
            self.usuario_4.setText(self.lista_jugadores[3])

    def keyPressEvent(self, event):
        """Estan las letras cambiadas por un tema practico."""
        if event.key() == Qt.Key_Left:
            self.senal.emit("R")
        elif event.key() == Qt.Key_Right:
            self.senal.emit("L")


class SalaEsperaJ(nombre_sala_1, clase_sala_1):
    server_signal = pyqtSignal(dict)
    server_signal_2 = pyqtSignal(dict)
    desconect_signal = pyqtSignal()
    counter_signal = pyqtSignal(int)

    def __init__(self, usuario, cliente):
        super().__init__()
        self.setupUi(self)
        # self.usain_nebolt.setChecked(True)
        # self.usain_nebolt.setDisabled(True)
        self.client = cliente
        self.server_signal.connect(self.client.send)
        self.server_signal_2.connect(self.client.send)
        self.desconect_signal.connect(self.client.terminar_conexion)
        self.usuario = usuario
        self.chat_log = ""
        self.enviar_chat.clicked.connect(self.manejo_boton_2)
        mensaje = {"status": "nuevo_usuario",
                   "data": {"usuario": self.usuario}}
        self.server_signal_2.emit(mensaje)
        self.usain_nebolt.stateChanged.connect(self.metodo_poderes)
        self.limpiessa.stateChanged.connect(self.metodo_poderes)
        self.sin_rastro.stateChanged.connect(self.metodo_poderes)
        self.cervessa.stateChanged.connect(self.metodo_poderes)
        self.del_trio.stateChanged.connect(self.metodo_poderes)
        self.nebcoins.stateChanged.connect(self.metodo_poderes)
        self.poderes = [False, False, False, False, False, False]
        self.vel_max.toggled.connect(self.cambiar_velocidad)
        self.vel_rapida.toggled.connect(self.cambiar_velocidad)
        self.vel_media.toggled.connect(self.cambiar_velocidad)
        self.vel_baja.toggled.connect(self.cambiar_velocidad)
        self.velocidad = None
        self.puntos_maximos.valueChanged.connect(self.cambiar_puntaje)
        self.puntaje_maximo = 10
        self.rojo.clicked.connect(self.cambiar_rojo)
        self.rosado.clicked.connect(self.cambiar_rosado)
        self.naranjo.clicked.connect(self.cambiar_naranjo)
        self.celeste.clicked.connect(self.cambiar_celeste)
        self.morado.clicked.connect(self.cambiar_morado)
        self.verde.clicked.connect(self.cambiar_verde)
        self.mi_color = None  # no se si esta bien.
        self.boton_jugar.clicked.connect(self.empezar_contando)
        self.counter_signal.connect(self.actualizar_counter)

    def jugar(self, event):
        """Empezar a jugar."""
        self.juego = VentanaJuego(event, self.client)
        self.hide()
        self.juego.show()

    def juguemos(self):
        """Metodo para empezar a jugar."""
        msje = {"status": "queremos_jugar",
                "data": {"nada": None}}
        sleep(0.1)
        self.server_signal_2.emit(msje)

    def empezar_contando(self):
        msje = {"status": "vamos_a_contar",
                "data": {"nada": None}}
        sleep(0.1)
        self.server_signal_2.emit(msje)

    def cuenta_regresiva(self):
        """Metodo para cuenta regresiva."""
        digito = 10
        tiempo = datetime.now()
        delta_ = timedelta(seconds=1)
        while digito > 0:
            if datetime.now() - tiempo > delta_:
                tiempo = datetime.now()
                digito -= 1
                self.counter_signal.emit(digito)
        self.juguemos()

    def actualizar_counter(self, digito):
        """Se actualiza el counter."""
        self.counter.setText(str(digito))
        self.counter.repaint()

    def cambiar_parent(self):
        """Metodo para cambiar el parent del cliente."""
        self.client.parent = self

    def cambiar_rojo(self):
        """Metodo para cambiar color."""
        self.rojo.setDisabled(True)

    def cambiar_rosado(self):
        """Metodo para cambiar color."""
        self.rosado.setDisabled(True)

    def cambiar_naranjo(self):
        """Metodo para cambiar color."""
        self.naranjo.setDisabled(True)

    def cambiar_celeste(self):
        """Metodo para cambiar color."""
        self.celeste.setDisabled(True)

    def cambiar_verde(self):
        """Metodo para cambiar color."""
        self.morado.setDisabled(True)

    def cambiar_morado(self):
        """Metodo para cambiar color."""
        self.verde.setDisabled(True)

    def cambiar_puntaje(self):
        """Metodo para cambiar el puntaje."""
        self.puntaje_maximo = self.puntos_maximos.value()
        sleep(0.1)
        puntaje = {"status": "cambio_puntaje",
                   "data": self.puntaje_maximo}
        self.server_signal_2.emit(puntaje)

    def cambiar_velocidad(self):
        if self.vel_max.isChecked():
            self.velocidad = 4
        elif self.vel_rapida.isChecked():
            self.velocidad = 3
        elif self.vel_media.isChecked():
            self.velocidad = 2
        elif self.vel_baja.isChecked():
            self.velocidad = 1
        sleep(0.1)
        velocidad = {"status": "cambio_velocidad",
                     "data": self.velocidad}
        self.server_signal_2.emit(velocidad)

    def metodo_poderes(self):
        """Metodo para revisar poder usain nebolt."""
        if self.usain_nebolt.isChecked():
            self.poderes[0] = True
        elif not self.usain_nebolt.isChecked():
            self.poderes[0] = False

        if self.limpiessa.isChecked():
            self.poderes[1] = True
        elif not self.limpiessa.isChecked():
            self.poderes[1] = False

        if self.sin_rastro.isChecked():
            self.poderes[2] = True
        elif not self.sin_rastro.isChecked():
            self.poderes[2] = False

        if self.cervessa.isChecked():
            self.poderes[3] = True
        elif not self.cervessa.isChecked():
            self.poderes[3] = False

        if self.del_trio.isChecked():
            self.poderes[4] = True
        elif not self.del_trio.isChecked():
            self.poderes[4] = False

        if self.nebcoins.isChecked():
            self.poderes[5] = True
        elif not self.nebcoins.isChecked():
            self.poderes[5] = False
        sleep(0.1)
        poderes = {"status": "nuevo_poder",
                   "data": self.poderes}
        self.server_signal_2.emit(poderes)

    def manejo_boton_2(self):
        sleep(0.1)
        mensaje = {"status": "mensaje",
                   "data": {"usuario": self.usuario,
                            "contenido": self.mensaje_chat.text()}}
        self.server_signal.emit(mensaje)
        self.mensaje_chat.setText("")

    def actualizar_chat(self, contenido):
        self.chat_log += f"{contenido}\n"
        self.chat.setText(self.chat_log)

    def keyPressEvent(self, event):
        """Enviar el mensaje presionando Enter."""
        if event.key() == Qt.Key_Return:
            self.manejo_boton_2()

    def actualizar_clientes(self, event):
        """metodo para actualizar los clientes."""
        if len(event) >= 1:
            self.jefe_partida.setText(f"{event[0]} (JEFE)")
        if len(event) >= 2:
            self.usuario_2.setText(event[1])
        if len(event) >= 3:
            self.usuario_3.setText(event[2])
        if len(event) == 4:
            self.usuario_4.setText(event[3])

    def actualizar_poderes(self, event):
        """Actualiza los poderes elegiddos."""
        pass

    def actualizar_velocidad(self):
        """Actualiza la velocidad elegida."""
        pass

    def actualizar_puntaje(self):
        """Metodo para actualizar puntaje elegido."""
        pass

    def elegir_ventana(self):
        """Metodo auxiliar para evitar."""
        pass


class SalaEsperaC(nombre_sala_2, clase_sala_2):
    server_signal = pyqtSignal(dict)
    server_signal_2 = pyqtSignal(dict)
    desconect_signal = pyqtSignal()

    def __init__(self, usuario, cliente):
        super().__init__()
        self.setupUi(self)
        self.usain_nebolt.setDisabled(True)
        self.limpiessa.setDisabled(True)
        self.sin_rastro.setDisabled(True)
        self.cervessa.setDisabled(True)
        self.del_trio.setDisabled(True)
        self.nebcoins.setDisabled(True)
        self.client = cliente
        self.server_signal.connect(self.client.send)
        self.server_signal_2.connect(self.client.send)
        self.desconect_signal.connect(self.client.terminar_conexion)
        self.usuario = usuario
        self.chat_log = ""
        self.enviar_chat.clicked.connect(self.manejo_boton_2)
        mensaje = {"status": "nuevo_usuario",
                   "data": {"usuario": self.usuario}}
        self.server_signal_2.emit(mensaje)

    def jugar(self, event):
        """Empezar a jugar."""
        self.juego = VentanaJuego(event, self.client)
        self.hide()
        self.juego.show()

    def cambiar_parent(self):
        """Metodo para cambiar el parent del cliente."""
        self.client.parent = self

    def manejo_boton_2(self):
        sleep(0.1)
        mensaje = {"status": "mensaje",
                   "data": {"usuario": self.usuario,
                            "contenido": self.mensaje_chat.text()}}
        self.server_signal.emit(mensaje)
        self.mensaje_chat.setText("")

    def actualizar_chat(self, contenido):
        self.chat_log += f"{contenido}\n"
        self.chat.setText(self.chat_log)

    def keyPressEvent(self, event):
        """Enviar el mensaje presionando Enter."""
        if event.key() == Qt.Key_Return:
            self.manejo_boton_2()

    def actualizar_clientes(self, event):
        """metodo para actualizar los clientes."""
        if len(event) >= 1:
            self.jefe_partida.setText(f"{event[0]} (JEFE)")
        if len(event) >= 2:
            self.usuario_2.setText(event[1])
        if len(event) >= 3:
            self.usuario_3.setText(event[2])
        if len(event) == 4:
            self.usuario_4.setText(event[3])

    def actualizar_poderes(self, event):
        """Actualiza los poderes elegiddos."""
        self.usain_nebolt.setChecked(event[0])
        self.limpiessa.setChecked(event[1])
        self.sin_rastro.setChecked(event[2])
        self.cervessa.setChecked(event[3])
        self.del_trio.setChecked(event[4])
        self.nebcoins.setChecked(event[5])

    def actualizar_velocidad(self, event):
        """Actualiza la velocidad elegida."""
        if event == 4:
            self.vel_elegida.setText("VELOCIDAD MAXIMA")
        elif event == 3:
            self.vel_elegida.setText("VELOCIDAD RAPIDA")
        elif event == 2:
            self.vel_elegida.setText("VELOCIDAD MEDIA")
        elif event == 1:
            self.vel_elegida.setText("VELOCIDAD BAJA")

    def actualizar_puntaje(self, event):
        """Metodo para actualizar puntaje elegido."""
        self.ptos_elegidos.setText(f"{event}  PUNTOS")


class VentanaAlerta(nombre_alerta, clase_alerta):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.boton_entendido.clicked.connect(self.esconder_mensaje)

    def definir_mensaje(self, mensaje):
        """Metodo para definir mensaje de alerta."""
        self.mensaje_error.setText(mensaje)

    def esconder_mensaje(self):
        """Metodo para esconder mensaje."""
        self.hide()


if __name__ == '__main__':
    app = QApplication([])
    form = VentanaBienvenida()
    form.show()
    sys.exit(app.exec_())
