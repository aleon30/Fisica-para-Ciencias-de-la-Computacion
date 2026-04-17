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
    Calcular la fuerza total usando el método del trapecio.
    """
    a = 0.0 # El límite inferior de integración es 0, ya que la fuerza se calcula desde la base del dique hasta la altura del fluido.
    b = H # El límite superior de integración es la altura del fluido, H.
    h = (b - a) / n # El tamaño del paso de integración

    suma = integrando(a, L, H) + integrando(b, L, H) # La suma de los valores en los extremos de la integración
    
    # Se suman los valores del integrando en los puntos intermedios, multiplicados por 2, 
    # ya que el método del trapecio requiere que se dupliquen los términos intermedios.
    for i in range(1, n):
        yi = a + i * h
        suma += 2.0 * integrando(yi, L, H)

    return (h / 2.0) * suma

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

longitud = 2.0
altura = 3.0
n = 6
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
H_vals = np.linspace(1.0, altura, 200) # Se genera un rango de valores de H desde 1.0 hasta altura=3.0 con 200 puntos para obtener una curva suave en la gráfica.
F_trap_vals = np.array([fuerza_trapecio(longitud, h_val, n) for h_val in H_vals]) # Se calcula la fuerza total usando el método del trapecio para cada valor de H en el rango especificado.
F_teo_vals = np.array([fuerza_teorica(longitud, h_val) for h_val in H_vals]) # Se calcula la fuerza total usando la ecuación teórica para cada valor de H en el rango especificado.


# Puntos discretos visibles en la gráfica principal
H_trap = np.linspace(1.0, altura, n+1) # Se generan n+1 puntos de H para mostrar en la gráfica (incluyendo los extremos).
F_trap_points = np.array([fuerza_trapecio(longitud, h_val, n) for h_val in H_trap])

# -----------------------------
# Datos para gráfica del integrando
# -----------------------------
y_cont = np.linspace(0.0, altura, 400)
f_cont = integrando(y_cont, longitud, altura)

y_trap = np.linspace(0.0, altura, n + 1)
f_trap = integrando(y_trap, longitud, altura)

# -----------------------------
# Subgráficas
# -----------------------------3.5
fig, axs = plt.subplots(2, 1, figsize=(10, 10))

# ==========================================
# Gráfica 1: Fuerza total vs altura H
# ==========================================
axs[0].plot(H_vals, F_trap_vals, label=f"Método del trapecio (n={n})")
axs[0].plot(H_vals, F_teo_vals, label="Ecuación teórica", linestyle="--")

axs[0].scatter(H_trap, F_trap_points, color="blue", s=25, zorder=3, label="Puntos evaluados")

# Cortes verticales
for i in range(len(H_trap)):
    axs[0].plot([H_trap[i], H_trap[i]], [0, F_trap_points[i]],
                color="gray", linestyle=":", linewidth=0.8)

for i in range(len(H_trap) - 1):
    hh_trap = [H_trap[i], H_trap[i], H_trap[i+1], H_trap[i+1]]
    ff_trapecio = [0, F_trap_points[i], F_trap_points[i+1], 0]

    axs[0].fill(hh_trap, ff_trapecio, 
                color='yellow', 
                edgecolor='darkblue', 
                alpha=0.5)
axs[0].set_xlabel("Altura del fluido H (m)")
axs[0].set_ylabel("Fuerza total F (N)")
axs[0].set_title("Fuerza total sobre el dique vs altura H")
axs[0].grid(True)
axs[0].legend()

# ==========================================
# Gráfica 2: Integrando vs y
# ==========================================
axs[1].plot(y_cont, f_cont, label="Integrando f(y)")

axs[1].scatter(y_trap, f_trap, color="red", s=30, zorder=3, label="Puntos del trapecio")

for i in range(len(y_trap)):
    axs[1].plot([y_trap[i], y_trap[i]], [0, f_trap[i]],
                color="gray", linestyle=":", linewidth=0.8)

for i in range(len(y_trap) - 1):
    x_trap = [y_trap[i], y_trap[i], y_trap[i+1], y_trap[i+1]]
    y_trapecio = [0, f_trap[i], f_trap[i+1], 0]

    axs[1].fill(x_trap, y_trapecio, 
                color='lightblue', 
                edgecolor='red', 
                alpha=0.5)

axs[1].plot(y_trap, f_trap, color="orange", linestyle="--", label="Aproximación trapezoidal")

axs[1].set_xlabel("profundidad del Fluido y (m)")
axs[1].set_ylabel("Fuerza diferencial por unidad de altura f(y)")
axs[1].set_title(f"Integracion de la fuerza para H = {altura:.2f} m")
axs[1].grid(True)
axs[1].legend()

plt.tight_layout()
plt.show()