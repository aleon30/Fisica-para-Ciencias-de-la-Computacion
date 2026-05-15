import numpy as np
import matplotlib.pyplot as plt
from math import pi

from matplotlib.ticker import FuncFormatter #para agregar las cifras significativas a las gráficas

# =========================================================
# FÍSICA PARA CIENCIAS DE LA COMPUTACIÓN
# DDB - Parte 1
# Campo eléctrico de una barra infinita cargada
# Método numérico: Regla del trapecio
# =========================================================

# =========================================================
# CONSTANTES FÍSICAS
# =========================================================

epsilon0 = 8.85e-12           # Permitividad eléctrica del vacío (C²/N·m²)
k = 9.00e9                    # Constante de Coulomb (N·m²/C²)

# =========================================================
# PARÁMETROS DEL PROBLEMA
# =========================================================

lam = 40.0e-9                 # Densidad lineal de carga λ (C/m)

# Aproximación de barra infinita
L = 100.0                     # Longitud máxima en y (m)

# Tamaño de cada subintervalo
dy = 0.01     

# Número de trapecios
N = int(L / dy) # 10000 trapecios

# Valores de x pedidos por la guía
x_values = np.linspace(2.00, 80.0, 200)

# =========================================================
# LISTAS PARA ALMACENAR RESULTADOS
# =========================================================

E_numerico = []
E_teorico = []


# =========================================================
# FORMATO DE CIFRAS SIGNIFICATIVAS
# =========================================================

def formato_decimal(valor, posicion):

    if valor < 10:
        texto = f"{valor:.2f}"

    elif valor < 100:
        texto = f"{valor:.1f}"

    else:
        texto = f"{valor:.0f}"

    return texto.replace(".", ",")


# =========================================================
# MÉTODO NUMÉRICO DEL TRAPECIO
# =========================================================

for x in x_values:

    # Extremos de integración
    y = np.linspace(0, L, N + 1)

    # Función de la integral
    f = (2 * k * lam * x) / ((y**2 + x**2)**(3/2))

    # Regla del trapecio
    integral = 0

    for i in range(N):

        area_trapecio = ((f[i] + f[i + 1]) / 2) * dy

        integral += area_trapecio

    # Guardar resultado numérico
    E_numerico.append(integral)

    # Modelo teórico
    E_teo = lam / (2 * pi * epsilon0 * x)

    E_teorico.append(E_teo)

# Convertir a arreglos numpy
E_numerico = np.array(E_numerico)
E_teorico = np.array(E_teorico)

# =========================================================
# ERROR PORCENTUAL
# =========================================================

error = np.abs((E_teorico - E_numerico) / E_teorico) * 100

# =========================================================
# TABLA DE RESULTADOS
# =========================================================

print("\n======================================================")
print("                TABLA DE RESULTADOS")
print("======================================================")

print(f"{'x (m)':<12}{'E Numérico':<18}{'E Teórico':<18}{'Error %':<12}")

for i in range(0, len(x_values), 20):

    print(
        f"{x_values[i]:<12.3g}"
        f"{E_numerico[i]:<18.3g}"
        f"{E_teorico[i]:<18.3g}"
        f"{error[i]:<12.3g}"
    )

# =========================================================
# GRÁFICA 1
# MÉTODO NUMÉRICO
# =========================================================

plt.figure(figsize=(8,5))

plt.plot(x_values, E_numerico)

plt.title("Campo eléctrico vs posición (Método numérico)")
plt.xlabel("Posición x (m)")
plt.ylabel("Campo eléctrico E (N/C)")

plt.grid(True)


plt.gca().xaxis.set_major_formatter(
    FuncFormatter(formato_decimal)
)
plt.gca().yaxis.set_major_formatter(
    FuncFormatter(formato_decimal)
)

plt.tight_layout()

plt.show()

# =========================================================
# GRÁFICA 2
# MODELO TEÓRICO
# =========================================================

plt.figure(figsize=(8,5))

plt.plot(x_values, E_teorico)

plt.title("Campo eléctrico vs posición (Modelo teórico)")
plt.xlabel("Posición x (m)")
plt.ylabel("Campo eléctrico E (N/C)")

plt.grid(True)

plt.gca().xaxis.set_major_formatter(
    FuncFormatter(formato_decimal)
)
plt.gca().yaxis.set_major_formatter(
    FuncFormatter(formato_decimal)
)

plt.tight_layout()

plt.show()

# =========================================================
# GRÁFICA 3
# COMPARACIÓN
# =========================================================

plt.figure(figsize=(8,5))

plt.plot(x_values, E_numerico, label="Método numérico")

plt.plot(x_values, E_teorico, label="Modelo teórico")

plt.title("Comparación entre método numérico y modelo teórico")

plt.xlabel("Posición x (m)")
plt.ylabel("Campo eléctrico E (N/C)")

plt.legend()

plt.grid(True)


plt.gca().xaxis.set_major_formatter(
    FuncFormatter(formato_decimal)
)
plt.gca().yaxis.set_major_formatter(
    FuncFormatter(formato_decimal)
)


plt.tight_layout()

plt.show()

# =========================================================
# ANÁLISIS
# =========================================================

print("\n======================================================")
print("                     ANÁLISIS")
print("======================================================")

print("""
1. El campo eléctrico disminuye al aumentar la distancia x.

2. El método numérico aproxima correctamente
   el modelo teórico.

3. Las pequeñas diferencias observadas se deben
   al proceso de discretización y aproximación
   numérica de la integral.

4. Mientras mayor sea la cantidad de trapecios,
   mejor será la aproximación numérica.
""")

