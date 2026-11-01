"""Experimento 2: error, tamaño del paso y comparación de Euler con Euler mejorado.

Cubre las Actividades 2 y 3 de la consigna, ambas sobre x' = -x, x(0) = 1, 0 <= t <= 10:
  - Error absoluto E_n para h en {1, 0.5, 0.1, 0.05, 0.01}. Figura `exp2-error-vs-t` (E_n
    contra t, una curva por h, eje y logarítmico) y tabla `exp2-error-por-h` con h, número
    de pasos, error final y error máximo.
  - Euler contra Euler mejorado para h en {1, 0.5, 0.1}. Tabla `exp2-metodos` con método, h,
    valor final, error final y pasos (seis filas), y figura `exp2-orden` (error final contra
    h en escala log-log, que muestra el orden de cada método).

Las figuras se guardan en informe/figuras/ y las tablas en informe/tablas/.
"""
import comun  # noqa: F401
from metodos import euler, euler_mejorado, error_absoluto  # noqa: F401


def correr() -> None:
    """Corre el experimento 2 y guarda sus figuras y tablas. Imprime un resumen corto."""
    print("Experimento 2 (error y métodos): [PENDIENTE] todavía no implementado.")
