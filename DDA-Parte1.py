import matplotlib.pyplot as plt
import numpy as np
"""
Si no tienen las librerias, instálenlas con estos comandos en el cmd:
pip install matplotlib
pip install numpy
"""

#------------------------------------------------------------------------------
g=9.81

def integrando(y, L, H):
    """
    Integrando de la fuerza total:
    80*g*L*(0.250*y³ - y + 10.0)*(H - y)
    """
    return 80.0 * g * L * (0.250 * y**3 - y + 10.0) * (H - y)

def fuerza_trapecio(L, H, n):
    """
    Calcula la fuerza total usando el método del trapecio.
    """
    a = 0.0 # El límite inferior de integración es 0, ya que la fuerza se calcula desde la base del dique hasta la altura del fluido.
    b = H # El límite superior de integración es la altura del fluido, H.
    h = (b - a) / n # El tamaño del paso de integración

    suma = integrando(a, L, H) + integrando(b, L, H) # La suma de los valores en los extremos de la integración
    
    # Se suman los valores del integrando en los puntos intermedios, multiplicados por 2, ya que el método del trapecio requiere que se dupliquen los términos intermedios.
    for i in range(1, n):
        yi = a + i * h
        suma += 2.0 * integrando(yi, L, H)

    return (h / 2.0) * suma # El resultado final de la integración usando el método del trapecio.

def fuerza_teorica(L, H):
    """
    Ecuación teórica dada en el enunciado:
    FTotal = 80*g*L*(0.0125*H³ - H/6 + 5)*H²
    """
    return 80.0 * g * L * (0.0125 * H**3 - H / 6.0 + 5.0) * H**2

def porcentaje_error(valor_aprox, valor_teorico):
    return abs((valor_teorico - valor_aprox) / valor_teorico) * 100.0

# -----------------------------
# Lectura de datos
# -----------------------------

# Lectura de la longitud
longitud = float(input("Ingrese la Longitud del dique, L(m): "))
while longitud < 1.5 or longitud > 3.5:
    longitud = float(input("Error. Ingrese Longitud en el intervalo [1.50, 3.50] m: "))

#Lectura de la altura
altura = float(input("Ingrese la Altura del nivel del fluido, H(m): "))
while altura < 1 or altura > 4.8:
    altura = float(input("Error. Ingrese Altura en el intervalo [1.00, 4.80] m: "))

#Lectura de la cantidad de trapecios
n = int(input("Ingrese la cantidad de trapecios n: "))
while n <= 0:
    n = int(input("Error. Ingrese un n entero positivo: "))

# -----------------------------
# Cálculos para un valor de H
# -----------------------------
F_trap = fuerza_trapecio(longitud, altura, n)
F_teo = fuerza_teorica(longitud, altura)
error = porcentaje_error(F_trap, F_teo)

print("\n--- RESULTADOS ---")
print(f"L = {longitud:.2f} m")
print(f"H = {altura:.2f} m")
print(f"n = {n}")
print(f"Fuerza total (trapecio) = {F_trap:.6f} N")
print(f"Fuerza total (teórica)  = {F_teo:.6f} N")
print(f"Porcentaje de error     = {error:.6f} %")

if error <= 2.0:
    print("La cantidad de trapecios elegida es válida (error <= 2.0%).")
else:
    print("La cantidad de trapecios elegida NO es válida (error > 2.0%).")

# -----------------------------
# Gráfica FTotal vs H
# -----------------------------
H_vals = np.linspace(1.0, 4.8, 200) # Se calculan los valores de la fuerza total para cada valor de H usando ambos métodos (trapecio y teórico)
F_trap_vals = np.array([fuerza_trapecio(longitud, h_val, n) for h_val in H_vals]) # Se calcula la fuerza total usando el método del trapecio para cada valor de H en el rango especificado.
F_teo_vals = np.array([fuerza_teorica(longitud, h_val) for h_val in H_vals]) # Se calcula la fuerza total usando la ecuación teórica para cada valor de H en el rango especificado.

plt.figure(figsize=(9, 6))
plt.plot(H_vals, F_trap_vals, label=f"Método del trapecio (n={n})")
plt.plot(H_vals, F_teo_vals, label="Ecuación teórica", linestyle="--")
plt.xlabel("Altura del fluido H (m)")
plt.ylabel("Fuerza total F (N)")
plt.title("Fuerza total sobre el dique vs altura H")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()
#-------------------------------------------------------------------------------------------

# Definir la función de fuerza en función de la altura y, con la longitud y altura del dique
#def fuerza(L, H, y):
#   return 80.0*9.81*L*(0.250*y**3-y+10.0)*(H-y)
# Se establecen valores para y desde el 0 hasta la altura del dique
#ejeX = np.linspace(0, altura, 1000)
#plt.plot(ejeX, fuerza(longitud, altura, ejeX))
#plt.show()