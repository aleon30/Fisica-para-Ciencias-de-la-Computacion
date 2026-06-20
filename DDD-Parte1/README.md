# DDD - Parte 1: Espejismos y Refracción de la Luz

Simulación numérica de la trayectoria de un rayo de luz en un medio con
índice de refracción variable (gradiente térmico de aire), resuelta con
el método de Runge-Kutta de 4to orden (RK4).

## Objetivo

Obtener la trayectoria continua de un rayo de luz al propagarse por un
medio heterogéneo, y caracterizar el punto de retorno (espejismo inferior)
de forma teórica y simulada, comparando ambos resultados.

## Contenido de la carpeta

| Archivo | Descripción |
|---|---|
| `DD2_Espejo.ipynb` | Notebook principal: resuelve el sistema de EDOs con RK4, calcula y_min teórico/simulado, genera las gráficas y vs x y θ vs x. |
| `animacion.ipynb` | Visualización interactiva (slider) que muestra el rayo avanzando, el ángulo local θ y el efecto óptico del espejismo. |
| `grafica_y_vs_x.png` | Trayectoria del rayo, con el punto de retorno marcado. |
| `grafica_theta_vs_x.png` | Evolución angular del rayo. |

## Cómo ejecutar

Requiere Python 3.10+ con las siguientes librerías:

```bash
pip install numpy matplotlib ipympl
```

1. Abrir `DD2_Espejo.ipynb` y ejecutar todas las celdas en orden. Esto
   genera las gráficas y el archivo `resultados_rk4.npz` (necesario para
   la animación).
2. Abrir `animacion.ipynb` y ejecutar todas las celdas para la
   visualización interactiva con slider.

## Modelo físico

Sistema de ecuaciones diferenciales ordinarias:
dy/dx     = tan(θ)
dθ/dx     = (1/n(y)) · (dn/dy)

con `n(y) = n0 + α·y` (variación lineal del índice de refracción).

## Parámetros utilizados

| Parámetro | Valor | Rango permitido |
|---|---|---|
| n0 | 1,00030 | [1,00025 – 1,00045] |
| α | 5,00×10⁻³ m⁻¹ | [1,00×10⁻³ – 9,00×10⁻³] m⁻¹ |
| θ0 | -0,150 rad | [-0,200 – -0,100] rad |
| y0 | 3,00 m | [1,00 – 5,00] m |
| x0 | 0,00 m | fijo |
| xf | 60,0 m | [40,0 – 90,0] m |
| Δx (h) | 5,00×10⁻³ m | [1,00×10⁻³ – 9,00×10⁻³] m |

Se verifica la condición de existencia del espejismo:
`α > n0·(1-cos θ0) / (y0·cos θ0)` → se cumple (ver salida de consola del notebook).

## Resultados

| Resultado | Valor |
|---|---|
| x_retorno (simulado) | ver salida del notebook al ejecutar |
| y_min (simulado) | ver salida del notebook al ejecutar |
| y_min (teórico) | ver salida del notebook al ejecutar |
| Error porcentual | ver salida del notebook al ejecutar |

*(Estos valores se obtienen directamente al correr `DD2_Espejo.ipynb`, tal
como exige la rúbrica: "los resultados presentados en el reporte se
obtienen directamente al ejecutar el código".)*

## Referencias

- Chapra, S., & Canale, R. (2015). *Métodos numéricos para ingenieros* (7ma ed.). McGraw-Hill Education.
- Sears, F. W., Zemansky, M. W., Young, H. D., & Freedman, R. A. (2018). *Física universitaria* (14a ed., Vol. 2). Pearson Educación.
- Serway, R. A., & Jewett, J. W. (2019). *Física para ciencias e ingeniería* (10a ed., Vol. 2). Cengage Learning.