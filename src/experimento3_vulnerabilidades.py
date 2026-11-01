"""Experimento 3: modelo de remediación de vulnerabilidades V' = -kV y sus variantes.

Cubre las Actividades 4, 5 y 6 de la consigna:
  - Organizaciones A, B y C (V0 = 1000; k = 0.1, 0.3, 0.7), 0 <= t <= 20, Euler con h en
    {1, 0.5, 0.1}. Figura `exp3-organizaciones` (V(t) de referencia y aproximada por
    organización) y tabla `exp3-valores` con el valor aproximado, la referencia
    V0 e^{-kt} y el error en t = 5, 10, 15 para cada organización y cada h.
  - Modelo discreto V_{n+1} = (1 - hk) V_n con hk > 1: valores de h elegidos por nosotros
    (por ejemplo hk = 1.5 y hk = 2.5). Figura `exp3-estabilidad` con la oscilación y los
    valores negativos.
  - Aparición de nuevas vulnerabilidades V' = λ - kV con V0 = 1000, k = 0.3 y λ en
    {0, 50, 100, 200}. Figura `exp3-lambda` (V(t) por λ con el equilibrio λ/k marcado) y
    tabla `exp3-equilibrio` con λ, λ/k y el valor simulado al final del intervalo.

Las figuras se guardan en informe/figuras/ y las tablas en informe/tablas/.
"""
import comun  # noqa: F401
from metodos import euler, error_absoluto  # noqa: F401


def correr() -> None:
    """Corre el experimento 3 y guarda sus figuras y tablas. Imprime un resumen corto."""
    print("Experimento 3 (vulnerabilidades): [PENDIENTE] todavía no implementado.")
