"""Experimento 1: verificación del método de Euler en casos con solución de referencia.

Cubre la sección 5 de la consigna:
  - Caso 1, crecimiento lineal: x' = 1, x(0) = 0, referencia x(t) = t, 0 <= t <= 10,
    h en {1, 0.5, 0.1}. Figura `exp1-lineal`: referencia y las tres aproximaciones.
  - Caso 2, decrecimiento exponencial: x' = -x, x(0) = 1, referencia x(t) = e^{-t},
    0 <= t <= 10, h en {1, 0.5, 0.1, 0.01}. Figura `exp1-exponencial`: referencia y las
    cuatro aproximaciones en una misma gráfica.

Las figuras se guardan en informe/figuras/; la consola solo imprime un resumen corto.
"""
import comun  # noqa: F401  (aplica el estilo de las figuras al importarse)
from metodos import euler  # noqa: F401


def correr() -> None:
    """Corre el experimento 1 y guarda sus figuras. Imprime un resumen corto."""
    print("Experimento 1 (verificación): [PENDIENTE] todavía no implementado.")
