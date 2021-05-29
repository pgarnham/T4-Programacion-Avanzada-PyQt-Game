"""Recordatorio para Examen Programación Avanzada."""

######################################################

# Discard --> metodo de un Set para eliminar un elemento,
# sin que tire error si no está.

from functools import reduce


mi_set = {1, 2, 3}

otro_set = {3, 4, 5}

1 in mi_set  # para ver si está en el set
mi_set | otro_set  # union de conjuntos (sets)

mi_set & otro_set  # intersección de conjuntos (sets)

mi_set - otro_set  # diferencia de conjuntos (sets)
#  también sirve el metodo difference.

mi_set ^ otro_set  # diferencia de conjuntos (sets)
# también sirve el metodo symmetric_difference

#  tambien podemos usar <= >= ==.

#####################################################

strings = ['Señores pasajeros', 'Disculpen', 'mi']
mapeo = map(lambda x: x.lower(), strings)

lista_nros = [1, 2, 3, 4, 5, 6]
filtrado_impares = filter(lambda x: x % 2 != 0, lista_nros)

reduce(lambda x, y: x + y, lista_nros)  # se puede usar un cero al final
# para eliminar el error si es un iterable vacío.


#####################################################


