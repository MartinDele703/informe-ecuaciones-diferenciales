"""Experimento 2: error, tamaño del paso y comparación de Euler con Euler mejorado.

Cubre las Actividades 2 y 3 de la consigna, ambas sobre x' = -x, x(0) = 1, 0 <= t <= 10,
con referencia x(t) = e^{-t}:
  - Error absoluto E_n para h en {1, 0.5, 0.1, 0.05, 0.01}. Figura `exp2-error-vs-t` (E_n
    contra t, una curva por h, eje y logarítmico) y tabla `exp2-error-por-h` con h, número
    de pasos, error final y error máximo.
  - Euler contra Euler mejorado para h en {1, 0.5, 0.1}. Tabla `exp2-metodos` con método, h,
    valor final, error final y pasos (seis filas), y figura `exp2-orden` (error final contra
    h en escala log-log, que muestra el orden de cada método). La figura usa los cinco h de la
    Actividad 2 (y no solo los tres de la tabla) para que la tendencia tenga más puntos; las
    rectas guía de pendiente 1 y 2 se anclan en el error con h = 0.01 de cada método, donde
    vale el régimen asintótico.

Las figuras se guardan en informe/figuras/ y las tablas en informe/tablas/. No se miden
tiempos de ejecución: el costo computacional se discute por el número de pasos y de
evaluaciones de f (una por paso en Euler, dos en Euler mejorado).
"""
import matplotlib.pyplot as plt
import numpy as np

import comun
from metodos import euler, euler_mejorado, error_absoluto

X0, T0, TF = 1.0, 0.0, 10.0
PASOS_ACTIVIDAD_2 = [1.0, 0.5, 0.1, 0.05, 0.01]
PASOS_ACTIVIDAD_3 = [1.0, 0.5, 0.1]
METODOS = [("Euler", euler), ("Euler mejorado", euler_mejorado)]


def f(t: float, x: float) -> float:
    """Lado derecho de x' = -x."""
    return -x


def referencia(t: np.ndarray) -> np.ndarray:
    """Solución de referencia x(t) = e^{-t}, tal como la da la consigna."""
    return np.exp(-t)


def etiqueta_h(h: float) -> str:
    """Devuelve h para una leyenda, sin ceros de más (1, 0.5, 0.01)."""
    return f"$h = {h:g}$"


def resolver(metodo, h: float) -> dict:
    """Integra x' = -x con el método dado y devuelve tiempos, valores, pasos y error."""
    tiempos, valores, pasos = metodo(f, X0, T0, TF, h)
    error = error_absoluto(referencia, tiempos, valores)
    return {"tiempos": tiempos, "valores": valores, "pasos": pasos, "error": error}


def figura_error_vs_t(resultados: dict[float, dict]) -> None:
    """Figura `exp2-error-vs-t`: E_n contra t para Euler, una curva por h, eje y logarítmico.

    Se excluye n = 0 porque E_0 = |x(0) - x_0| = 0 siempre, y el cero no se puede dibujar en
    escala logarítmica. Para n >= 1 ningún E_n es cero: con h = 1 la aproximación de Euler
    vale 0 desde el primer paso, así que E_n = e^{-t_n} > 0.
    """
    fig, ax = plt.subplots(figsize=(7, 4))
    for h, r in resultados.items():
        ax.plot(r["tiempos"][1:], r["error"][1:], label=etiqueta_h(h))
    ax.set_yscale("log")
    ax.set_xlabel("$t$")
    ax.set_ylabel(r"Error absoluto $E_n = |x(t_n) - x_n|$")
    ax.set_xlim(T0, TF)
    ax.legend(title="Paso", ncol=2)
    comun.guardar_figura(fig, "exp2-error-vs-t")


def tabla_error_por_h(resultados: dict[float, dict]) -> None:
    """Tabla `exp2-error-por-h`: h, pasos, error final y error máximo para Euler."""
    filas = []
    for h, r in resultados.items():
        filas.append([f"${h:g}$", comun.formato_entero(r["pasos"]),
                      comun.formato_cientifico(r["error"][-1]),
                      comun.formato_cientifico(r["error"].max())])
    comun.guardar_tabla(filas, [r"$h$", "Pasos", r"$E_N$ (en $t = 10$)", r"$\max_n E_n$"],
                        "exp2-error-por-h")


def tabla_metodos(resultados: dict[str, dict[float, dict]]) -> None:
    """Tabla `exp2-metodos`: método, h, valor final x_N, error final y pasos (seis filas).

    El valor final va en notación científica porque la referencia en t = 10 es
    e^{-10} = 4.54e-5 y con decimales fijos se leería como 0.00.
    """
    filas = []
    for nombre, por_h in resultados.items():
        for h in PASOS_ACTIVIDAD_3:
            r = por_h[h]
            filas.append([nombre, f"${h:g}$", comun.formato_cientifico(r["valores"][-1]),
                          comun.formato_cientifico(r["error"][-1]),
                          comun.formato_entero(r["pasos"])])
    comun.guardar_tabla(filas, ["Método", r"$h$", r"$x_N$", r"$E_N$", "Pasos"],
                        "exp2-metodos", alineacion="llrrr")


def figura_orden(resultados: dict[str, dict[float, dict]]) -> None:
    """Figura `exp2-orden`: error final contra h en log-log, con rectas guía de orden 1 y 2.

    Cada recta guía es C h^p anclada en el error con el h más chico del método
    correspondiente: pendiente 1 sobre Euler y pendiente 2 sobre Euler mejorado. Se ancla en
    el h más chico y no en el más grande porque el orden es una propiedad asintótica (h -> 0):
    con h = 1 Euler da x_N = 0 y su error final es e^{-10}, pequeño por casualidad y no por
    precisión, así que una guía anclada ahí no acompañaría a los puntos.
    """
    hs = np.array(sorted(PASOS_ACTIVIDAD_2))
    fig, ax = plt.subplots(figsize=(7, 4))
    marcadores = {"Euler": "o", "Euler mejorado": "s"}
    guias = {"Euler": 1, "Euler mejorado": 2}
    for nombre, por_h in resultados.items():
        errores = np.array([por_h[h]["error"][-1] for h in hs])
        linea, = ax.plot(hs, errores, marker=marcadores[nombre], linestyle="-", label=nombre)
        p = guias[nombre]
        guia = errores[0] * (hs / hs[0]) ** p
        ax.plot(hs, guia, linestyle=":", linewidth=1.0, color=linea.get_color(),
                label=f"pendiente {p}")
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlabel("Paso $h$")
    ax.set_ylabel("Error final $E_N$ (en $t = 10$)")
    ax.legend()
    comun.guardar_figura(fig, "exp2-orden")


def correr() -> None:
    """Corre el experimento 2 y guarda sus figuras y tablas. Imprime un resumen corto."""
    # Actividad 2: Euler con los cinco pasos.
    euler_por_h = {h: resolver(euler, h) for h in PASOS_ACTIVIDAD_2}
    figura_error_vs_t(euler_por_h)
    tabla_error_por_h(euler_por_h)

    # Actividad 3: los dos métodos con los mismos cinco pasos (la tabla usa tres).
    por_metodo = {"Euler": euler_por_h,
                  "Euler mejorado": {h: resolver(euler_mejorado, h) for h in PASOS_ACTIVIDAD_2}}
    tabla_metodos(por_metodo)
    figura_orden(por_metodo)

    print("Experimento 2 (error y métodos): x' = -x, x(0) = 1, 0 <= t <= 10")
    print(f"  {'h':>6}  {'pasos':>5}  {'E_N Euler':>12}  {'E_N Euler mej.':>15}")
    for h in PASOS_ACTIVIDAD_2:
        e1 = euler_por_h[h]["error"][-1]
        e2 = por_metodo["Euler mejorado"][h]["error"][-1]
        print(f"  {h:>6g}  {euler_por_h[h]['pasos']:>5d}  {e1:>12.3e}  {e2:>15.3e}")
    print("  Figuras: exp2-error-vs-t, exp2-orden. Tablas: exp2-error-por-h, exp2-metodos.")
