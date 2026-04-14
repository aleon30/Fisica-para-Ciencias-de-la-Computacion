import matplotlib.pyplot as plt
import numpy as np
"""
Si no tienen las librerias, instálenlas con estos comandos en el cmd:
pip install matplotlib
pip install numpy
"""

# Definir la función de fuerza en función de la altura y, con la longitud y altura del dique
def fuerza(L, H, y):
    return 80.0*9.81*L*(0.250*y**3-y+10.0)*(H-y)

# Lectura de la longitud
longitud = float(input("Ingrese la longitud del dique, L(m): "))
while longitud < 1.5 or longitud > 3.5:
    longitud = float(input("La longitud debe estar en el intervalo [1,50; 3,50]: "))

#Lectura de la altura
altura = float(input("Ingrese la altura del nivel del fluido, H(m): "))
while altura < 1 or altura > 4.8:
    altura = float(input("La altura debe estar en el intervalo [1,00; 4,80]: "))

# Se establecen valores para y desde el 0 hasta la altura del dique
ejeX = np.linspace(0, altura, 1000)
plt.plot(ejeX, fuerza(longitud, altura, ejeX))
plt.show()
