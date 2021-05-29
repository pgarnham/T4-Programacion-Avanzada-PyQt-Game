# :space_invader: :video_game: :space_invader: Tarea 04 DCCurve :space_invader: :video_game: :space_invader:

### ``pgarnham``

## Consideraciones generales :pencil:

* Es una buena idea correr mi programa en la consola :smile:

* En toda la tarea use un Font externo para darle un toque mas retro. el archivo del font se puede instalar ejecutando la linea 18 del modulo ``funciones.py``, que esta originalmente comentado para no ser invasivo. Tambien puede ser instalado a mano, el archivo esta en la carpeta ``arcade_classic_pizz``.

-------

### Cosas no completadas   :x:


* No cree el juego en si, solo el mob¿vimiento con las flechas izquierda y derecha, por temas de tiempo :cry:

* :a: Por ende, no hay ningun poder o choque controlado, solo las curvas :smile:

* No alcancé a revisar el funcionamiento del servidor en computadores distintos, pero si se corren varias veces en distintas consolas (en un solo pc), funciona correctamente el dialogo entre salas de espera.


-------

## Ejecución :computer:
* primero hay que ejecutar el servidor, y dejarlo corriendo en segundo plano  ```servidor.py```

* Luego hay que correr el modulo  ```ventanas.py``` las veces que se desee para tener mas usuarios.

* Los archivos terminados en ``*_rc.py`` son para el correcto funcionamiento de los archivos ``ui`` y no los pude dejar en una carpeta aparte (perdon por el desorden).

* En la carpeta ``qtdesigner`` deje los archivos ``ui`` y las imagenes que use en el diseño. :wink:

* La carpeta ``pacman sprites`` Deje los sprites que pensaba usar para el juego, pero que no alcancé a implementar :cry:


-------

## Librerías :books:
### Librerías externas utilizadas
La lista de librerías externas que utilicé fue la siguiente:


```python

import PyQt5
from hashlib import sha256
from threading import Thread
from os import urandom
from time import sleep
from numpy import empty
import pickle
import socket
import json
from datetime import datetime
import random
import sys
from datetime import datetime, timedelta

```
###### (PyQt5 y sus infinitos derivados...)
-------

### Librerías propias
Por otro lado, los módulos que fueron creados fueron los siguientes:

#### ```ventanas.py```   *Contiene:*
  Corresponde basicamente al ``Frontend``, pero le puse nombre ventanas, no sabría decir porqué :smile:.

#### ```funciones.py```   *Contiene:*
  Corresponde al ``Backend``. Tiene al cliente y a la clase que permite realizar las curvas y el movimiento. Se comunica a traves de señales con el frontend. (Perdon nuevamente por el nombre :smile:).

#### ```servidor.py```   *Contiene:*
  Corresponde simplemente al servidor, que se comunica con el cliente ubicado en el Backend.

#### ```usuarios.txt```   *Contiene:*
  Es un archivo que contiene un diccionario serializado, con el usuario, la sal y la contraseña encriptada. Fue creado en un principio con un diccionario vacío, pero esa parte del codigo fue comentado, puesto que ahora el archivo ya existe (fue subido). Este codigo está en ``funciones.py`` (lineas 21-23).


-------

## Supuestos y consideraciones adicionales :bulb:
Los supuestos que realicé durante la tarea son los siguientes:

1. El servidor no maneja el inicio de sesion. Considere que esta opcion era mas segura. Solo se puede acceder al servidor una vez que se tenga una cuenta creada y se ingrese correctamente la contraseña.


2. En *general* usé  ``Docstring``, por lo que las funciones deberían ser autoexplicativas.


...

-------




## Referencias de código externo :book: :wink: :boat:


* Para realizar las curvas y dibujo use codigo de ejemplos de esta pagina. http://zetcode.com/gui/pyqt5/painting/
  + Específicamente lo usé para la clase ``PaintPath`` implementada en el modulo ``funciones.py``, entre las lineas 115 y 199


-------

## Descuentos :smile:

* Intenté cumplir con **PEP 8** siempre, linea a linea. Agregué Docstrings a todas las funciones y métodos, pero a su vez no comenté practicamente ninguna linea.

* Usé muy pocas variables no aclarativas, pero también fue en pocas ocasiones, y para variables que se usaban muy poco, o un par de contadores auxiliares.
