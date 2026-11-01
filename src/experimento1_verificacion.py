"""Experimento 1: verificación del método de Euler en casos con solución de referencia.

Cubre la sección 5 de la consigna:
  - Caso 1, crecimiento lineal: x' = 1, x(0) = 0, referencia x(t) = t, 0 <= t <= 10,
    h en {1, 0.5, 0.1}. Figura `exp1-lineal`: referencia y las tres aproximaciones.
  - Caso 2, decrecimiento exponencial: x' = -x, x(0) = 1, referencia x(t) = e^{-t},
    0 <= t <= 10, h en {1, 0.5, 0.1, 0.01}. Figura `exp1-exponencial`: referencia y las
    cuatro aproximaciones en una misma gráfica.

Las figuras se guardan en informe/figuras/; la consola solo imprime un resumen corto.
"""
import matplotlib.pyplot as plt
import numpy as np

import comun
from metodos import error_absoluto, euler

T0 = 0.0
TF = 10.0

# Estilo de cada aproximación, indexado por h. Los pasos grandes llevan marcador en cada
# nodo porque tienen pocos puntos; los chicos van como línea discontinua para no tapar la
# referencia, que siempre es la línea continua negra.
ESTILOS = {
    1.0: dict(color="tab:red", linestyle="-", marker="o", markersize=5),
    0.5: dict(color="tab:orange", linestyle="--", marker="s", markersize=4),
    0.1: dict(color="tab:blue", linestyle="--"),
    0.01: dict(color="tab:green", linestyle=":"),
}


def etiqueta_h(h: float) -> str:
    """Etiqueta de leyenda para el paso h, en modo matemático y sin ceros de más."""
    return rf"$h = {h:g}$"


def f_lineal(t: float, x: float) -> float:
    """Lado derecho del caso 1: x' = 1."""
    return 1.0


def referencia_lineal(t: np.ndarray) -> np.ndarray:
    """Solución de referencia del caso 1: x(t) = t."""
    return t


def f_exponencial(t: float, x: float) -> float:
    """Lado derecho del caso 2: x' = -x."""
    return -x


def referencia_exponencial(t: np.ndarray) -> np.ndarray:
    """Solución de referencia del caso 2: x(t) = e^{-t}."""
    return np.exp(-t)


def simular_caso(f, x0: float, referencia, pasos_h: list[float]) -> dict[float, dict]:
    """Corre Euler para cada h y devuelve, por h, tiempos, valores y error absoluto final.

    El resultado es un diccionario {h: {"tiempos", "valores", "pasos", "final",
    "final_ref", "error_final"}}; lo usan tanto la figura como el resumen de consola.
    """
    resultados = {}
    for h in pasos_h:
        tiempos, valores, pasos = euler(f, x0, T0, TF, h)
        errores = error_absoluto(referencia, tiempos, valores)
        resultados[h] = {
            "tiempos": tiempos,
            "valores": valores,
            "pasos": pasos,
            "final": float(valores[-1]),
            "final_ref": float(referencia(tiempos[-1:])[0]),
            "error_final": float(errores[-1]),
        }
    return resultados


def dibujar_caso(ax: plt.Axes, referencia, resultados: dict[float, dict],
                 etiqueta_referencia: str, grosor: float = 1.6) -> None:
    """Dibuja la referencia (línea continua negra) y una curva de Euler por h sobre ax.

    `grosor` es el ancho de las curvas de Euler; la referencia va un poco más gruesa.
    """
    t_fino = np.linspace(T0, TF, 1001)
    ax.plot(t_fino, referencia(t_fino), color="black", linewidth=grosor + 0.6,
            label=etiqueta_referencia, zorder=1)
    for h, res in resultados.items():
        ax.plot(res["tiempos"], res["valores"], label=etiqueta_h(h),
                linewidth=grosor, zorder=2, **ESTILOS[h])
    ax.set_xlabel(r"$t$")
    ax.set_ylabel(r"$x(t)$")
    ax.set_xlim(T0, TF)


def figura_lineal(resultados: dict[float, dict]) -> None:
    """Figura `exp1-lineal`: x' = 1 contra x(t) = t para los tres pasos."""
    fig, ax = plt.subplots(figsize=(7, 4))
    dibujar_caso(ax, referencia_lineal, resultados, r"referencia $x(t) = t$")
    ax.set_ylim(T0, TF)
    ax.legend(loc="upper left")
    comun.guardar_figura(fig, "exp1-lineal")


def figura_exponencial(resultados: dict[float, dict]) -> None:
    """Figura `exp1-exponencial`: x' = -x contra x(t) = e^{-t} para los cuatro pasos.

    Las curvas con h = 0,1 y h = 0,01 se pegan a la referencia en la escala principal. El
    recuadro amplía el tramo final (7 <= t <= 10), donde el error relativo de Euler es mayor
    (crece con t) y las cinco curvas se distinguen, sin cambiar la escala de la gráfica.
    """
    fig, ax = plt.subplots(figsize=(7, 4))
    dibujar_caso(ax, referencia_exponencial, resultados, r"referencia $x(t) = e^{-t}$")
    ax.set_ylim(-0.05, 1.05)
    ax.legend(loc="upper right")

    recuadro = ax.inset_axes([0.47, 0.13, 0.37, 0.4])
    dibujar_caso(recuadro, referencia_exponencial, resultados, "", grosor=1.0)
    recuadro.set_xlim(7.0, 10.0)
    recuadro.set_ylim(0.0, 1.0e-3)
    recuadro.set_xlabel("")
    recuadro.set_ylabel("")
    recuadro.tick_params(labelsize=8)
    recuadro.ticklabel_format(axis="y", style="sci", scilimits=(0, 0), useMathText=True)
    recuadro.yaxis.get_offset_text().set_fontsize(8)
    recuadro.set_title(r"detalle, $7 \leq t \leq 10$", fontsize=9, loc="right")
    ax.indicate_inset_zoom(recuadro, edgecolor="gray")
    comun.guardar_figura(fig, "exp1-exponencial")


def imprimir_resumen(titulo: str, resultados: dict[float, dict]) -> None:
    """Imprime una línea por h con el valor final aproximado, el de referencia y el error."""
    print(f"  {titulo}")
    for h, res in resultados.items():
        print(f"    h = {h:<5g} pasos = {res['pasos']:<5d} x(10) ≈ {res['final']:.6f}  "
              f"ref = {res['final_ref']:.6f}  error final = {res['error_final']:.3e}")


def correr() -> None:
    """Corre el experimento 1 y guarda sus figuras. Imprime un resumen corto."""
    print("Experimento 1 (verificación de Euler contra soluciones de referencia)")
    lineal = simular_caso(f_lineal, 0.0, referencia_lineal, [1.0, 0.5, 0.1])
    figura_lineal(lineal)
    imprimir_resumen("Caso 1, x' = 1, x(0) = 0, referencia x(t) = t:", lineal)

    exponencial = simular_caso(f_exponencial, 1.0, referencia_exponencial,
                               [1.0, 0.5, 0.1, 0.01])
    figura_exponencial(exponencial)
    imprimir_resumen("Caso 2, x' = -x, x(0) = 1, referencia x(t) = exp(-t):", exponencial)
    print("  Figuras: informe/figuras/exp1-lineal.pdf, informe/figuras/exp1-exponencial.pdf")


if __name__ == "__main__":
    correr()
