"""Dibujos y movimiento eso espero."""

import sys
from PyQt5.QtWidgets import QApplication, QDialog, QGraphicsView, QGraphicsScene, QGridLayout, QPushButton, QComboBox
from PyQt5.QtCore import QPointF, QRectF, Qt, pyqtSignal
from PyQt5.QtGui import QPen, QBrush
from PyQt5 import uic


class Paint(QGraphicsView):
    move_signal = pyqtSignal(tuple)
    def __init__(self):
        QGraphicsView.__init__(self)
        self.setSceneRect(QRectF(self.viewport().rect()))
        self.scene = QGraphicsScene()
        self.isPaint = False
        self.isDelete = False
        self.isClear = False
        self.isObject = None
        self.startX = None
        self.startY = None

    def tools(self, e):
        if self.isPaint:
            pen = QPen(Qt.black)
            brush = QBrush(Qt.SolidPattern)
            self.scene.addItem(self.scene.addEllipse(
                e.x(), e.y(), 5, 5, pen, brush))
            self.setScene(self.scene)
        if self.isDelete:
            items = self.items(e.x(), e.y())
            for item in items:
                self.scene.removeItem(item)

    def keyPressEvent(self, event):
        """Que hacer si se aprieta cierto botón."""
        if event.key() == Qt.Key_Right:
            self.move_signal.emit((None, None))
        elif event.key() == Qt.Key_Left:
            self.move_signal.emit((None, None))

    # def mousePressEvent(self, event):
    #     e = QPointF(self.mapToScene(event.pos()))
    #     self.tools(e)
    #     self.startX = e.x()
    #     self.startY = e.y()

    # def mouseReleaseEvent(self, event):
    #     e = QPointF(self.mapToScene(event.pos()))
    #     self.paintObject(e)

    # def mouseMoveEvent(self, event):
    #     e = QPointF(self.mapToScene(event.pos()))
    #     self.tools(e)
