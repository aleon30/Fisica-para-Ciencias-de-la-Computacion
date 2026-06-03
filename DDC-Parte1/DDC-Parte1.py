import numpy as np
import matplotlib.pyplot as plt

# Parámetros

longitud = 3.00
tension = 125
densidadLineal = 0.00400
amplitud = 3.00
modo = 4
dx = 0.0100

# Numero de onda y frecuencia angular

longitudOnda = 2 * longitud / modo
numeroOnda = 2 * np.pi / longitudOnda
frecuencia = np.sqrt(tension / densidadLineal) * modo / (2 * longitud)
omega = 2 * np.pi * frecuencia

# Función de superposicion

def superposicion(x, t):
    return 2 * amplitud * np.sin(numeroOnda * x) * np.sin(omega * t)
