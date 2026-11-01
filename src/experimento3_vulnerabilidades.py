"""Experimento 3: modelo de remediación de vulnerabilidades V' = -kV y sus variantes.

Cubre las Actividades 4, 5 y 6 de la consigna:
  - Organizaciones A, B y C (V0 = 1000; k = 0.1, 0.3, 0.7), 0 <= t <= 20, Euler con h en
    {1, 0.5, 0.1}. Figura `exp3-organizaciones`: tres paneles, uno por organización, cada
    uno con la referencia V0 e^{-kt} (línea continua negra) y las tres aproximaciones de
    Euler. Se eligió un panel por organización y no un solo panel con las tres, porque con
    doce curvas en un mismo eje las de h = 0.5 y h = 0.1 se pegan a la referencia y no se
    distinguen; en paneles separados se ve, para cada k, cómo las aproximaciones se acercan
    a la referencia al reducir h. Tabla `exp3-valores`: una fila por (organización, h) con el
    valor aproximado y el error absoluto en t = 5, 10, 15, más una fila con la referencia
    por organización.
  - Modelo discreto V_{n+1} = (1 - hk) V_n con hk > 1: k = 0.7, V0 = 1000, h en {1, 2, 3},
    0 <= t <= 30, es decir hk en {0.7, 1.4, 2.1}. Con hk = 0.7 la sucesión decrece y se
    mantiene positiva; con hk = 1.4 alterna el signo con amplitud decreciente; con hk = 2.1
    alterna el signo y diverge. Se usa `euler` tal cual, porque un paso de Euler sobre
    V' = -kV es exactamente V_{n+1} = (1 - hk) V_n. Figura `exp3-estabilidad` en dos paneles:
    con hk = 2.1 la sucesión llega a |V_10| ≈ 2594 y, en un solo eje, aplastaría las otras
    dos curvas (que caen por debajo de 100 en pocos pasos). El panel izquierdo muestra
    hk = 0.7 y hk = 1.4; el derecho, hk = 2.1. Los dos tienen la referencia V0 e^{-kt} y
    una línea horizontal en V = 0 para que se vean los valores negativos. Las tres
    sucesiones se calculan hasta t = 30, pero el eje del panel izquierdo se recorta a
    0 <= t <= 15: después de t ≈ 12 las dos sucesiones valen menos de 1 en valor absoluto
    y mostrar el resto del intervalo solo achica la zona donde se ve la oscilación.
  - Aparición de nuevas vulnerabilidades V' = λ - kV con V0 = 1000, k = 0.3 y λ en
    {0, 50, 100, 200}, Euler con h = 0.1 (el paso de menor error de los usados en la
    Actividad 4), 0 <= t <= 20. Figura `exp3-lambda`: V(t) por λ con el equilibrio λ/k
    marcado como línea horizontal punteada del mismo color. Tabla `exp3-equilibrio`: λ,
    λ/k, el valor simulado en t = 20 y la diferencia entre ambos. Acá no hay solución de
    referencia: la consigna no la da y en este trabajo no se resuelven ecuaciones
    analíticamente, así que solo se compara con el equilibrio.

Las figuras se guardan en informe/figuras/ y las tablas en informe/tablas/. La consola solo
imprime un resumen corto: los valores en t = 5, 10, 15 de la Actividad 4 con h = 1, los
primeros seis términos de cada sucesión de la Actividad 5 y el valor final de cada λ.
"""
import matplotlib.pyplot as plt
import numpy as np

import comun
from metodos import euler, error_absoluto

V0 = 1000.0

# Actividad 4
ORGANIZACIONES = {"A": 0.1, "B": 0.3, "C": 0.7}
PASOS_ORGANIZACIONES = [1.0, 0.5, 0.1]
T_FINAL_ORGANIZACIONES = 20.0
TIEMPOS_TABLA = [5.0, 10.0, 15.0]

# Actividad 5
K_ESTABILIDAD = 0.7
PASOS_ESTABILIDAD = [1.0, 2.0, 3.0]
T_FINAL_ESTABILIDAD = 30.0
T_FINAL_ESTABILIDAD_PANEL_IZQ = 15.0  # solo el eje del panel izquierdo; se simula hasta 30

# Actividad 6
K_LAMBDA = 0.3
LAMBDAS = [0.0, 50.0, 100.0, 200.0]
PASO_LAMBDA = 0.1
T_FINAL_LAMBDA = 20.0

ESTILO_POR_PASO = {
    1.0: dict(color="C0", linestyle="--", marker="o", markersize=3.5, markevery=1),
    0.5: dict(color="C1", linestyle="-.", marker="s", markersize=3, markevery=2),
    0.1: dict(color="C2", linestyle=":"),
}


def referencia_exponencial(k: float):
    """Devuelve la solución de referencia V(t) = V0 e^{-kt} para la tasa k dada."""
    return lambda t: V0 * np.exp(-k * t)


def campo_remediacion(k: float):
    """Devuelve f(t, V) = -kV, el lado derecho del modelo de remediación."""
    return lambda t, v: -k * v


def campo_con_aparicion(lam: float, k: float):
    """Devuelve f(t, V) = λ - kV, el modelo con aparición de nuevas vulnerabilidades."""
    return lambda t, v: lam - k * v


def indice_del_tiempo(tiempos: np.ndarray, t_objetivo: float, h: float) -> int:
    """Índice n tal que t_n está a menos de h/2 de t_objetivo.

    No se compara con igualdad de flotantes: t0 + n*h puede diferir de t_objetivo en unas
    unidades de redondeo. Si ningún t_n queda a esa distancia, el objetivo no cae sobre la
    malla y se levanta un error en vez de devolver un vecino silenciosamente.
    """
    n = int(round((t_objetivo - tiempos[0]) / h))
    if n < 0 or n >= len(tiempos) or abs(tiempos[n] - t_objetivo) >= h / 2:
        raise ValueError(f"t = {t_objetivo} no está en la malla de paso {h}")
    return n


def etiqueta_paso(h: float) -> str:
    """Etiqueta de leyenda para un paso h, en modo matemático."""
    return f"Euler, $h = {h:g}$"


def actividad_organizaciones() -> None:
    """Actividad 4: organizaciones A, B y C con Euler para tres pasos. Figura y tabla."""
    fig, ejes = plt.subplots(1, 3, figsize=(10, 3.6), sharey=True)
    malla_referencia = np.linspace(0.0, T_FINAL_ORGANIZACIONES, 400)
    filas = []
    print("  Actividad 4, Euler con h = 1 (valor aproximado / referencia):")
    for eje, (nombre, k) in zip(ejes, ORGANIZACIONES.items()):
        referencia = referencia_exponencial(k)
        eje.plot(malla_referencia, referencia(malla_referencia), color="black",
                 label=r"Referencia $V_0 e^{-kt}$")
        fila_referencia = [f"{nombre} ($k = {k:g}$)", "ref."]
        for t_obj in TIEMPOS_TABLA:
            fila_referencia += [comun.formato_decimal(referencia(t_obj), 1), "--"]
        filas.append(fila_referencia)
        for h in PASOS_ORGANIZACIONES:
            tiempos, valores, _ = euler(campo_remediacion(k), V0, 0.0,
                                        T_FINAL_ORGANIZACIONES, h)
            errores = error_absoluto(referencia, tiempos, valores)
            eje.plot(tiempos, valores, label=etiqueta_paso(h), linewidth=1.3,
                     **ESTILO_POR_PASO[h])
            fila = [f"{nombre} ($k = {k:g}$)", f"${h:g}$"]
            resumen = []
            for t_obj in TIEMPOS_TABLA:
                n = indice_del_tiempo(tiempos, t_obj, h)
                fila += [comun.formato_decimal(valores[n], 1),
                         comun.formato_decimal(errores[n], 2)]
                resumen.append(f"V({t_obj:g}) = {valores[n]:.1f} / {referencia(t_obj):.1f}")
            filas.append(fila)
            if h == 1.0:
                print(f"    {nombre} (k = {k:g}): " + ", ".join(resumen))
        eje.set_title(f"Organización {nombre} ($k = {k:g}$)")
        eje.set_xlabel("$t$ (días)")
        eje.set_xlim(0, T_FINAL_ORGANIZACIONES)
    ejes[0].set_ylabel("$V(t)$ (equipos vulnerables)")
    ejes[0].legend()
    fig.tight_layout()
    comun.guardar_figura(fig, "exp3-organizaciones")

    encabezados = ["Org.", "$h$", "$V(5)$", "$E(5)$", "$V(10)$", "$E(10)$",
                   "$V(15)$", "$E(15)$"]
    comun.guardar_tabla(filas, encabezados, "exp3-valores", alineacion="l" + "r" * 7)


def actividad_estabilidad() -> None:
    """Actividad 5: el modelo discreto con hk < 1, 1 < hk < 2 y hk > 2. Figura y consola."""
    fig, (eje_izq, eje_der) = plt.subplots(1, 2, figsize=(10, 3.8))
    malla_referencia = np.linspace(0.0, T_FINAL_ESTABILIDAD, 400)
    referencia = referencia_exponencial(K_ESTABILIDAD)
    sucesiones = {}
    print(f"  Actividad 5, V_(n+1) = (1 - hk) V_n con k = {K_ESTABILIDAD:g}, "
          "primeros seis términos:")
    for h in PASOS_ESTABILIDAD:
        tiempos, valores, _ = euler(campo_remediacion(K_ESTABILIDAD), V0, 0.0,
                                    T_FINAL_ESTABILIDAD, h)
        sucesiones[h] = (tiempos, valores)
        hk = h * K_ESTABILIDAD
        primeros = ", ".join(f"{v:.1f}" for v in valores[:6])
        print(f"    h = {h:g} (hk = {hk:.1f}): {primeros}")

    paneles = [(eje_izq, PASOS_ESTABILIDAD[:2], r"$hk < 2$", T_FINAL_ESTABILIDAD_PANEL_IZQ),
               (eje_der, PASOS_ESTABILIDAD[2:], r"$hk > 2$", T_FINAL_ESTABILIDAD)]
    for eje, pasos, titulo, t_max in paneles:
        eje.plot(malla_referencia, referencia(malla_referencia), color="black",
                 label=r"Referencia $V_0 e^{-kt}$")
        eje.axhline(0.0, color="gray", linewidth=0.8)
        for h in pasos:
            tiempos, valores = sucesiones[h]
            hk = h * K_ESTABILIDAD
            eje.plot(tiempos, valores, color=f"C{PASOS_ESTABILIDAD.index(h)}",
                     linewidth=0.9, marker="o", markersize=4,
                     label=f"$h = {h:g}$ ($hk = {hk:.1f}$)")
        eje.set_title(titulo)
        eje.set_xlabel("$t$ (días)")
        eje.set_xlim(0, t_max)
        eje.legend()
    eje_izq.set_ylabel("$V_n$ (equipos vulnerables)")
    fig.tight_layout()
    comun.guardar_figura(fig, "exp3-estabilidad")


def actividad_lambda() -> None:
    """Actividad 6: V' = λ - kV para cuatro valores de λ, con el equilibrio λ/k. Figura y tabla."""
    fig, eje = plt.subplots(figsize=(7, 4))
    filas = []
    print(f"  Actividad 6, V' = λ - kV con k = {K_LAMBDA:g}, h = {PASO_LAMBDA:g}:")
    for i, lam in enumerate(LAMBDAS):
        tiempos, valores, _ = euler(campo_con_aparicion(lam, K_LAMBDA), V0, 0.0,
                                    T_FINAL_LAMBDA, PASO_LAMBDA)
        equilibrio = lam / K_LAMBDA
        color = f"C{i}"
        eje.plot(tiempos, valores, color=color, label=rf"$\lambda = {lam:g}$")
        eje.axhline(equilibrio, color=color, linestyle=":", linewidth=1.2)
        final = valores[-1]
        filas.append([f"${lam:g}$", comun.formato_decimal(equilibrio, 1),
                      comun.formato_decimal(final, 1),
                      comun.formato_decimal(final - equilibrio, 1)])
        print(f"    λ = {lam:g}: equilibrio λ/k = {equilibrio:.2f}, V(20) = {final:.2f}")
    eje.set_xlabel("$t$ (días)")
    eje.set_ylabel("$V(t)$ (equipos vulnerables)")
    eje.set_xlim(0, T_FINAL_LAMBDA)
    eje.set_xticks(np.arange(0, T_FINAL_LAMBDA + 1, 5))
    eje.set_ylim(bottom=0)
    eje.plot([], [], color="gray", linestyle=":", linewidth=1.2,
             label=r"Equilibrio $\lambda / k$")
    eje.legend(loc="upper right")
    fig.tight_layout()
    comun.guardar_figura(fig, "exp3-lambda")

    encabezados = [r"$\lambda$", r"$\lambda / k$", "$V(20)$", r"$V(20) - \lambda / k$"]
    comun.guardar_tabla(filas, encabezados, "exp3-equilibrio", alineacion="rrrr")


def correr() -> None:
    """Corre el experimento 3 y guarda sus figuras y tablas. Imprime un resumen corto."""
    print("Experimento 3 (vulnerabilidades):")
    actividad_organizaciones()
    actividad_estabilidad()
    actividad_lambda()
    print("  Guardadas: exp3-organizaciones, exp3-estabilidad, exp3-lambda (figuras); "
          "exp3-valores, exp3-equilibrio (tablas).")
