import numpy as np
import matplotlib.pyplot as plt
from math import pi
from matplotlib.ticker import FuncFormatter
from matplotlib.widgets import RadioButtons

# =========================================================
# FÍSICA PARA CIENCIAS DE LA COMPUTACIÓN
# DDB - Parte 1
# Campo eléctrico de una barra infinita cargada
# Método numérico: Regla del trapecio
# =========================================================

# =========================================================
# CONSTANTES FÍSICAS
# =========================================================

epsilon0 = 8.85e-12
k = 9.00e9

# =========================================================
# PARÁMETROS DEL PROBLEMA
# =========================================================

lam = 40.0e-9

# Límite superior de integración.
# Se aproxima la barra infinita como:
# integral de -∞ a +∞ ≈ 2 integral de 0 a L
L = 100.0 # m representa la longitud de la barra usada para aproximar la barra infinita

dy = 0.0100 # Paso de integración (intervalo entre puntos en y)

N = int(L / dy) # Número de intervalos para la integración

x_values = np.linspace(2.00, 80.0, 200) # Valores de x desde 2.00 m hasta 80.0 m, con 200 puntos

# =========================================================
# LISTAS PARA ALMACENAR RESULTADOS
# =========================================================

E_numerico = []
E_teorico = []

# =========================================================
# FORMATO CON TRES CIFRAS SIGNIFICATIVAS Y COMA DECIMAL
# =========================================================

def formato_3_cifras(valor, posicion=None):
    """
    Muestra los valores de los ejes con tres cifras significativas
    y coma decimal.
    """

    if valor < 10:
        texto = f"{valor:.2f}"

    elif valor < 100:
        texto = f"{valor:.1f}"

    else:
        texto = f"{valor:.0f}"

    return texto.replace(".", ",")


def formato_tabla(valor):
    """
    Formato para la tabla de resultados con tres cifras significativas
    y coma decimal.
    """
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

    y = np.linspace(0, L, N + 1) # Valores de y desde 0 hasta L, con N+1 puntos (incluyendo el límite superior)

    f = (2 * k * lam * x) / ((y**2 + x**2)**(3/2)) # Función a integrar para el campo eléctrico, considerando la simetría de la barra

    integral = 0

    for i in range(N):

        area_trapecio = ((f[i] + f[i + 1]) / 2) * dy # Área del trapecio para el intervalo [y[i], y[i+1]]

        integral += area_trapecio

    E_numerico.append(integral)

    E_teo = lam / (2 * pi * epsilon0 * x) # Campo eléctrico teórico para una barra infinita cargada a distancia x

    E_teorico.append(E_teo)

E_numerico = np.array(E_numerico)
E_teorico = np.array(E_teorico)

# =========================================================
# ERROR PORCENTUAL
# =========================================================

error = np.abs((E_teorico - E_numerico) / E_teorico) * 100 # Error porcentual entre el método numérico y el modelo teórico

# =========================================================
# TABLA DE RESULTADOS PARA CONSOLA
# =========================================================

print("\n======================================================")
print("                TABLA DE RESULTADOS")
print("======================================================")
print(f"{'x (m)':<12}{'E Numérico (N/C)':<22}{'E Teórico (N/C)':<22}{'Error %':<12}")

for i in range(0, len(x_values), 20):

    print(
        f"{formato_tabla(x_values[i]):<12}"
        f"{formato_tabla(E_numerico[i]):<22}"
        f"{formato_tabla(E_teorico[i]):<22}"
        f"{formato_tabla(error[i]):<12}"
    )

# =========================================================
# VENTANA ÚNICA: GRÁFICA + BOTONES + TABLA
# =========================================================

fig = plt.figure(figsize=(13, 8))

# Gráfica principal centrada y más arriba
# [izquierda, abajo, ancho, alto]
ax = fig.add_axes([0.33, 0.42, 0.62, 0.48])

# Casillero de botones, separado de la gráfica
ax_botones = fig.add_axes([0.05, 0.62, 0.22, 0.22])

botones = RadioButtons(
    ax_botones,
    (
        "Método numérico",
        "Modelo teórico",
        "Comparación",
        "Trapecios"
    )
)

ax_botones.set_title("Seleccione la gráfica", fontsize=10, fontweight="bold")

# Zona de tabla más abajo y separada del eje x
ax_tabla = fig.add_axes([0.05, 0.05, 0.90, 0.22])
ax_tabla.axis("off")

# =========================================================
# TABLA DENTRO DE LA VENTANA
# =========================================================

indices_tabla = np.linspace(0, len(x_values) - 1, 6, dtype=int)

datos_tabla = []

for i in indices_tabla:

    datos_tabla.append([
        formato_tabla(x_values[i]),
        formato_tabla(E_numerico[i]),
        formato_tabla(E_teorico[i]),
        formato_tabla(error[i])
    ])

tabla = ax_tabla.table(
    cellText=datos_tabla,
    colLabels=[
        "x (m)",
        "E numérico (N/C)",
        "E teórico (N/C)",
        "Error porcentual (%)"
    ],
    cellLoc="center",
    loc="center"
)

tabla.auto_set_font_size(False)
tabla.set_fontsize(9)
tabla.scale(1, 1.25)

ax_tabla.text(
    0.5,
    1.05,
    "Tabla de resultados del campo eléctrico para valores representativos de x",
    ha="center",
    va="bottom",
    fontsize=11,
    fontweight="bold",
    transform=ax_tabla.transAxes
)

# =========================================================
# FORMATO GENERAL DE LAS GRÁFICAS
# =========================================================

def aplicar_formato(titulo):
    """
    Aplica formato formal a cada gráfica.
    """

    ax.set_title(titulo, fontsize=13, fontweight="bold", pad=8)

    ax.set_xlabel("Posición x (m)", fontsize=11, labelpad=8)

    ax.set_ylabel("Campo eléctrico E (N/C)", fontsize=11)

    ax.grid(True)

    ax.legend(loc="best", fontsize=9)

    ax.xaxis.set_major_formatter(FuncFormatter(formato_3_cifras))

    ax.yaxis.set_major_formatter(FuncFormatter(formato_3_cifras))

    ax.tick_params(axis="both", labelsize=10)

    for borde in ax.spines.values():
        borde.set_linewidth(1.5)

    fig.canvas.draw_idle()

# =========================================================
# FUNCIONES DE GRAFICACIÓN
# =========================================================

def graficar_numerico():

    ax.clear()

    ax.plot(
        x_values,
        E_numerico,
        linewidth=2.5,
        label="Método numérico: regla del trapecio"
    )

    aplicar_formato(
        "Gráfico campo eléctrico vs posición (Método numérico)"
    )


def graficar_teorico():

    ax.clear()

    ax.plot(
        x_values,
        E_teorico,
        linewidth=2.5,
        label="Modelo teórico: barra infinita"
    )

    aplicar_formato(
        "Gráfico campo eléctrico vs posición (Modelo teórico)"
    )


def graficar_comparacion():

    ax.clear()

    ax.plot(
        x_values,
        E_numerico,
        linewidth=2.5,
        label="Método numérico: regla del trapecio"
    )

    ax.plot(
        x_values,
        E_teorico,
        linestyle="--",
        linewidth=2.5,
        label="Modelo teórico: barra infinita"
    )

    aplicar_formato(
        "Gráfico campo eléctrico vs posición (Método numérico y modelo teórico)"
    )

def graficar_trapecios():

    ax.clear()

    # Valor fijo de x para mostrar cómo se aplica la regla del trapecio
    x_muestra = 2.00

    # Intervalo mostrado para la variable de integración y
    L_muestra = 20.0

    # Paso visual para los trapecios.
    # Se usa un paso grande solo para que los trapecios se distingan.
    dy_trapecio = 0.1

    # Puntos finos para dibujar la función suavemente
    y_suave = np.linspace(0, L_muestra, 1000)

    f_suave = (
        2 * k * lam * x_muestra
    ) / ((y_suave**2 + x_muestra**2)**(3/2))

    # Puntos gruesos para construir los trapecios
    y_trap = np.arange(0, L_muestra + dy_trapecio, dy_trapecio)

    f_trap = (
        2 * k * lam * x_muestra
    ) / ((y_trap**2 + x_muestra**2)**(3/2))

    # Dibujar trapecios sin alterar la curva real
    for i in range(len(y_trap) - 1):

        # Vértices del trapecio:
        # (y_i, 0), (y_i, f_i), (y_{i+1}, f_{i+1}), (y_{i+1}, 0)
        xs = [
            y_trap[i],
            y_trap[i],
            y_trap[i + 1],
            y_trap[i + 1]
        ]

        ys = [
            0,
            f_trap[i],
            f_trap[i + 1],
            0
        ]

        ax.fill(
            xs,
            ys,
            alpha=0.22,
            edgecolor="red",
            linewidth=1.2,
            label="Trapecios de integración" if i == 0 else None
        )

        # Líneas verticales rojas, como en el esquema del enunciado
        ax.plot(
            [y_trap[i], y_trap[i]],
            [0, f_trap[i]],
            color="red",
            linewidth=1
        )

    # Última línea vertical
    ax.plot(
        [y_trap[-1], y_trap[-1]],
        [0, f_trap[-1]],
        color="red",
        linewidth=1
    )

    # Dibujar la función real encima de los trapecios
    ax.plot(
        y_suave,
        f_suave,
        linewidth=3,
        label="Integrando del campo eléctrico"
    )

    ax.set_title(
        "Representación de la regla del trapecio aplicada al integrando del campo eléctrico",
        fontsize=13,
        fontweight="bold",
        pad=8
    )

    ax.set_xlabel(
        "Posición sobre la barra, y (m)",
        fontsize=11,
        labelpad=8
    )

    ax.set_ylabel(
        "Integrando f(y) (N/C·m)",
        fontsize=11
    )

    ax.grid(True)

    ax.legend(loc="best", fontsize=9)

    ax.xaxis.set_major_formatter(FuncFormatter(formato_3_cifras))
    ax.yaxis.set_major_formatter(FuncFormatter(formato_3_cifras))

    ax.tick_params(axis="both", labelsize=10)

    for borde in ax.spines.values():
        borde.set_linewidth(1.5)

    fig.canvas.draw_idle()

# =========================================================
# CAMBIO DE GRÁFICA CON BOTONES
# =========================================================

def cambiar_grafica(opcion):

    if opcion == "Método numérico":
        graficar_numerico()

    elif opcion == "Modelo teórico":
        graficar_teorico()

    elif opcion == "Comparación":
        graficar_comparacion()
    elif opcion == "Trapecios":
        graficar_trapecios()

botones.on_clicked(cambiar_grafica)

# Gráfica inicial
graficar_numerico()

# =========================================================
# ANÁLISIS
# =========================================================

print("\n======================================================")
print("                     ANÁLISIS")
print("======================================================")

print("""
1. El campo eléctrico disminuye al aumentar la distancia x, 
   lo cual concuerda con el modelo teórico E = λ/(2πε0x).

2. El método numérico aproxima correctamente el comportamiento
   del modelo teórico, ya que ambas gráficas presentan una tendencia
   decreciente de tipo inversamente proporcional.

3. Las diferencias entre el método numérico y el modelo teórico se deben
   a la discretización de la integral mediante la regla del trapecio y a que
   la barra infinita se aproxima usando un límite finito L = 100,0 m.

4. Para valores pequeños de x, la aproximación numérica es más cercana
   al modelo teórico. Para valores grandes de x, el error puede aumentar
   porque la longitud finita usada en la integración representa peor
   a una barra infinita.

5. Si se disminuye Δy o se aumenta el valor de L, la aproximación numérica
   mejora, aunque también aumenta el costo computacional.
""")

plt.show()
