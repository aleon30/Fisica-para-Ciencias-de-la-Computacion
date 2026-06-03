import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib.widgets import RadioButtons

#  PARÁMETROS DEL SISTEMA

L = 2.50
tension = 150
densidad_lineal= 8.00e-3 
amplitud = 2.00e-2
n_modo = 7
dx = 1.00e-2

# Antinodo de refrencia
x_antinodo_ref = 0.54

# MAGNITUDES DERIVADAS

velocidad = np.sqrt(tension / densidad_lineal)
k_n    = n_modo * np.pi / L
omega  = k_n * velocidad
f_osc  = omega / (2 * np.pi)
T_per  = 1.00 / f_osc

# MALLA ESPACIAL Y TEMPORAL

dt = 0.90 * dx / velocidad
# Número de Courant
a = velocidad * dt / dx 

# Tiempo de estabilización: la onda recorre 100 veces la longitud de la cuerda
t_estab = 100 * L / velocidad

# Los 5 instantes de muestreo según la fórmula:
#   t_k = t_estab + (k-1) · T/4   para k = 1,2,3,4,5
t_muestras = [t_estab + (k - 1) * T_per / 4 for k in range(1, 6)]

# Tiempo total de simulación
T_sim  = t_muestras[-1]

nx = round(L / dx) + 1
x = np.linspace(0, L, nx)

idx_antinodo    = int(round(x_antinodo_ref / dx))
x_antinodo_real = x[idx_antinodo]

print(f"\nNúmero de Courant (a) = {a:.4f}  {'✓' if a <= 1 else '✗ INESTABLE'}")
print(f" Paso de tiempo (Δt) = {dt:.6f} s")
print(f" Nodos espaciales (nx) = {nx}")
print(f" Tiempo de estabilización = {t_estab:.4f} s")

def desplazamiento_exacto(x_arr, t_val):
    return 2 * amplitud * np.sin(k_n * x_arr) * np.sin(omega * t_val)

def velocidad_exacta(x_arr, t_val):
    return 2 * amplitud * omega * np.sin(k_n * x_arr) * np.cos(omega * t_val)

u_prev = desplazamiento_exacto(x, 0.0)               # nivel n = 0  (t = 0)
u_curr = u_prev + dt * velocidad_exacta(x, 0.0)      # nivel n = 1  (t = Δt)

#  Diferencias finitas de 2do orden

r2           = a ** 2
perfiles     = {}
paso_actual  = 0
t_actual     = dt

# Ordenamos los instantes de muestreo para capturarlos en orden
instantes_pendientes = sorted(t_muestras)
idx_muestra = 0

tiempo_antinodo   = []
amplitud_antinodo = []

while t_actual <= T_sim + dt and idx_muestra < len(instantes_pendientes):

    # ── Verificar si este paso captura un instante de muestreo ────
    t_objetivo = instantes_pendientes[idx_muestra]
    if abs(t_actual - t_objetivo) < dt / 2:
        perfiles[t_objetivo] = u_curr.copy()
        idx_muestra += 1

    # ── Fórmula de avance (nodos interiores) ─────────────────────
    u_next = np.empty(nx)
    u_next[1:-1] = (
          2 * u_curr[1:-1]
        -     u_prev[1:-1]
        + r2 * (u_curr[2:] - 2 * u_curr[1:-1] + u_curr[:-2])
    )

    if t_actual >= t_estab:
        tiempo_antinodo.append(t_actual)
        amplitud_antinodo.append(u_curr[idx_antinodo])

    # ── Condiciones de frontera — extremos fijos (nodos) ─────────
    u_next[0]  = 0.0
    u_next[-1] = 0.0

    u_prev = u_curr
    u_curr = u_next
    t_actual += dt

print(f"Simulación completa. Perfiles capturados: {len(perfiles)}\n")

# (a) Grafico de los perfiles en los instantes de tiempo

COLORES = ['#1a6faf', '#c94040', '#2a9d5c', '#e07b20', '#7b52ab']
ESTILOS = ['-', '--', '-.', ':', (0, (3,1,1,1))]

t_arr = np.array(tiempo_antinodo)
y_arr = np.array(amplitud_antinodo)
t_rel = t_arr - t_estab

fig, ax = plt.subplots(figsize=(12, 5.5))
fig.subplots_adjust(left=0.28)   # espacio a la izquierda para los botones

ax_radio = fig.add_axes([0.02, 0.35, 0.15, 0.30])   # [left, bottom, width, height]
radio = RadioButtons(
    ax_radio,
    labels=["Perfil de onda", "Perfil + antinodo", "Amplitud vs tiempo"],
    activecolor='#1a6faf',
)
for label in radio.labels:
    label.set_fontsize(9)

# ══════════════════════════════════════════════════════════════════
#  FUNCIONES DE DIBUJO PARA CADA VISTA
# ══════════════════════════════════════════════════════════════════

def dibujar_perfil(mostrar_antinodo=False):
    ax.clear()

    for idx, (t_cap, perfil) in enumerate(sorted(perfiles.items())):
        k     = idx + 1
        label = f"$t_{k}$ = {t_cap:.5f} s  [+{(k-1)/4:.2f}T]"
        ax.plot(x, perfil,
                color=COLORES[idx], linestyle=ESTILOS[idx],
                linewidth=1.8, label=label)

    if mostrar_antinodo:
        ax.axvline(x_antinodo_real,
                   color='black', linewidth=1.4, linestyle='--', alpha=0.7,
                   label=f"Antinodo  $x$ = {x_antinodo_real:.2f} m")

    ax.set_title("Perfil de la cuerda en estado estacionario",
                 fontsize=11, pad=10)
    ax.set_xlabel("Posición a lo largo de la cuerda,  $x$  (m)", fontsize=10)
    ax.set_ylabel("Desplazamiento transversal,  $y$  (m)",        fontsize=10)
    ax.axhline(0, color='black', linewidth=0.7)
    ax.set_xlim(0, L)
    ax.set_ylim(-2*amplitud*1.25, 2*amplitud*1.25)

    ax.xaxis.set_major_locator(ticker.MultipleLocator(L / (2 * n_modo)))
    ax.yaxis.set_major_locator(ticker.MultipleLocator(2*amplitud * 0.50))
    ax.xaxis.set_minor_locator(ticker.AutoMinorLocator(4))
    ax.yaxis.set_minor_locator(ticker.AutoMinorLocator(4))
    ax.xaxis.set_major_formatter(ticker.FuncFormatter(lambda v, _: f"{v:.2f}"))
    ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda v, _: f"{v:.4f}"))
    ax.grid(which='major', linestyle='--', linewidth=0.5, alpha=0.6)
    ax.grid(which='minor', linestyle=':',  linewidth=0.3, alpha=0.4)

    ax.legend(
        title=f"Instantes de tiempo:\n$t_{{\\rm estab}}$ = {t_estab:.5f} s",
        title_fontsize=8, fontsize=8,
        loc='upper right', framealpha=0.92, edgecolor='#cccccc',
    )
    fig.canvas.draw_idle()


def dibujar_amplitud():
    ax.clear()

    ax.plot(t_rel, y_arr, color='#1a6faf', linewidth=1.4,
            label=f"$x$ = {x_antinodo_real:.2f} m")
    ax.axhline( 2*amplitud, color='gray', linewidth=0.8,
                linestyle='--', alpha=0.7, label=f"±{2*amplitud:.4f} m")
    ax.axhline(-2*amplitud, color='gray', linewidth=0.8,
                linestyle='--', alpha=0.7)

    for idx, t_cap in enumerate(sorted(perfiles.keys())):
        t_cap_rel = t_cap - t_estab
        i_cercano = np.argmin(np.abs(t_rel - t_cap_rel))

    ax.set_title(
        f"Evolución temporal del desplazamiento en el antinodo $x$ = {x_antinodo_real:.2f} m",
        fontsize=11, pad=10
    )
    ax.set_xlabel(
        f"Tiempo desde el régimen estacionario,  $t - t_{{\\rm estab}}$  (s)",
        fontsize=10
    )
    ax.set_ylabel("Amplitud,  $A$  (m)", fontsize=10)
    ax.set_xlim(0, t_rel[-1])
    ax.set_ylim(-2*amplitud*1.25, 2*amplitud*1.25)

    ax.xaxis.set_major_locator(ticker.MultipleLocator(T_per))
    ax.yaxis.set_major_locator(ticker.MultipleLocator(2*amplitud*0.50))
    ax.xaxis.set_minor_locator(ticker.AutoMinorLocator(4))
    ax.yaxis.set_minor_locator(ticker.AutoMinorLocator(4))
    ax.xaxis.set_major_formatter(ticker.FuncFormatter(lambda v, _: f"{v:.4f}"))
    ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda v, _: f"{v:.4f}"))
    ax.grid(which='major', linestyle='--', linewidth=0.5, alpha=0.6)
    ax.grid(which='minor', linestyle=':',  linewidth=0.3, alpha=0.4)

    fig.canvas.draw_idle()


# ══════════════════════════════════════════════════════════════════
#  CALLBACK DEL RADIO BUTTON
# ══════════════════════════════════════════════════════════════════

def on_radio(label):
    if label == "Perfil de onda":
        dibujar_perfil(mostrar_antinodo=False)
    elif label == "Perfil + antinodo":
        dibujar_perfil(mostrar_antinodo=True)
    elif label == "Amplitud vs tiempo":
        dibujar_amplitud()

radio.on_clicked(on_radio)

# Dibujar la vista inicial
dibujar_perfil(mostrar_antinodo=False)
plt.show()