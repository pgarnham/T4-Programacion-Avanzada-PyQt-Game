import sys
from PyQt5.QtWidgets import QApplication, QGraphicsView, QGraphicsScene
from PyQt5.QtCore import QRectF, Qt, pyqtSignal
from PyQt5.QtGui import QPen, QBrush
from PyQt5 import QtGui, QtCore
from PyQt5 import uic
from threading import Thread
from time import sleep


class Paint(QGraphicsView):
    def __init__(self):
        QGraphicsView.__init__(self)
        self.setSceneRect(QRectF(self.viewport().rect()))
        self.scene = QGraphicsScene()
        self.setBackgroundBrush(QtGui.QBrush( QtGui.QColor(0,0,0), QtCore.Qt.SolidPattern))
        self._x = 1
        self._y = 1
        self.rumbo_fijo = (1, 1)
        self.direcciones = [(1, 4), (2, 3), (3, 2), (4, 1), (5, 0), (4, -1),
                            (3, -2), (2, -3), (1, -4), (0, -5), (-1, -4),
                            (-2, -3), (-3, -2), (-4, -1), (-5, 0), (-4, 1),
                            (-3, 2), (-2, 3), (-1, 4), (0, 5)]
        self._direccion = 0
        self.tarea = Thread(name="Thread 1", target=self.avanzar, daemon=True)
        self.setScene(self.scene)
        self.tarea.start()

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
        if tupla[0] > 0:
            rumbo_x = 1
        elif tupla[0] < 0:
            rumbo_x = -1
        elif tupla[0] == 0:
            rumbo_x = 0
        if tupla[1] > 0:
            rumbo_y = 1
        elif tupla[1] < 0:
            rumbo_y = -1
        elif tupla[1] == 0:
            rumbo_y = 0
        self.rumbo_fijo = (rumbo_x, rumbo_y)
        self.tools((self.x, self.y))

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

    def tools(self, e):
        pen = QPen(Qt.red)
        brush = QBrush(Qt.red)
        self.scene.addItem(self.scene.addEllipse(e[0], e[1], 6, 6, pen, brush))
        self.setScene(self.scene)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Left:
            self.avanzar_curva("L")
        elif event.key() == Qt.Key_Right:
            self.avanzar_curva("R")

    def avanzar(self):
        """Metodo para avanzar sin hacer una curva."""
        while True:
            sleep(0.05)
            self.x += self.rumbo_fijo[0]
            self.y += self.rumbo_fijo[1]
            self.tools((self.x, self.y))


nombre_juego, clase_juego = uic.loadUiType("qtdesigner/juego.ui")


class VentanaJuego(nombre_juego, clase_juego):

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.paint = Paint()
        self.layout_juego.addWidget(self.paint)
        self.senal.connect(self.paint.avanzar_curva)


app = QApplication(sys.argv)
juego = VentanaJuego()
juego.show()
app.exec_()
