"""Métodos numéricos del trabajo: Euler y Euler mejorado, con las firmas exactas de la consigna.

Los dos devuelven la misma terna: los valores del tiempo, los valores aproximados de x y la
cantidad de pasos realizados. Se acumula paso a paso con un `for`; no se usa ninguna rutina de
integración de biblioteca.

Los tiempos se calculan como t0 + n*h y no acumulando t += h: sumar h muchas veces arrastra
error de redondeo en t y desplaza la comparación con la solución de referencia.
"""
from collections.abc import Callable

import numpy as np

Funcion = Callable[[float, float], float]


def cantidad_de_pasos(t0: float, tf: float, h: float) -> int:
    """Cuántos pasos de tamaño h hacen falta para ir de t0 a tf.

    Se redondea en vez de truncar porque (tf - t0) / h no suele ser entero en punto
    flotante aunque lo sea en papel (10 / 0.1 da 99.99999999999999). Si el cociente
    no es entero más allá de ese error de representación (tolerancia relativa 1e-9),
    se lanza ValueError en vez de redondear en silencio: un último paso más corto o
    un intervalo recortado romperían la comparación con la referencia y el análisis
    de orden. Todos los h del informe dividen exactamente sus intervalos.
    """
    if h <= 0:
        raise ValueError("el tamaño del paso h tiene que ser positivo")
    cociente = (tf - t0) / h
    pasos = round(cociente)
    if abs(cociente - pasos) > 1e-9 * max(1.0, abs(cociente)):
        raise ValueError(f"(tf - t0) / h = {cociente!r} no es entero: el paso h = {h!r} "
                         f"tiene que dividir exactamente el intervalo [{t0!r}, {tf!r}]")
    return pasos


def euler(f: Funcion, x0: float, t0: float, tf: float, h: float):
    """Método de Euler para x'(t) = f(t, x), x(t0) = x0, desde t0 hasta tf con paso h.

    Devuelve (tiempos, valores, pasos): los arreglos t_n y x_n, de longitud pasos + 1, y la
    cantidad de pasos realizados. En cada paso se usa la pendiente al comienzo del intervalo:
    x_{n+1} = x_n + h f(t_n, x_n).
    """
    pasos = cantidad_de_pasos(t0, tf, h)
    tiempos = t0 + h * np.arange(pasos + 1)
    valores = np.empty(pasos + 1)
    valores[0] = x0
    x = x0
    for n in range(pasos):
        x = x + h * f(tiempos[n], x)
        valores[n + 1] = x
    return tiempos, valores, pasos


def euler_mejorado(f: Funcion, x0: float, t0: float, tf: float, h: float):
    """Método de Euler mejorado (Heun) con la misma interfaz que `euler`.

    En cada paso se predice con Euler y se corrige con el promedio de la pendiente inicial y
    la pendiente en el punto predicho:
        x~_{n+1} = x_n + h f(t_n, x_n)
        x_{n+1}  = x_n + (h/2) [f(t_n, x_n) + f(t_{n+1}, x~_{n+1})]
    Cuesta dos evaluaciones de f por paso contra una de Euler.
    """
    pasos = cantidad_de_pasos(t0, tf, h)
    tiempos = t0 + h * np.arange(pasos + 1)
    valores = np.empty(pasos + 1)
    valores[0] = x0
    x = x0
    for n in range(pasos):
        pendiente_inicial = f(tiempos[n], x)
        prediccion = x + h * pendiente_inicial
        pendiente_predicha = f(tiempos[n + 1], prediccion)
        x = x + (h / 2) * (pendiente_inicial + pendiente_predicha)
        valores[n + 1] = x
    return tiempos, valores, pasos


def error_absoluto(referencia: Callable[[np.ndarray], np.ndarray],
                   tiempos: np.ndarray, valores: np.ndarray) -> np.ndarray:
    """Error absoluto E_n = |x(t_n) - x_n| contra la solución de referencia x(t)."""
    return np.abs(referencia(tiempos) - valores)
