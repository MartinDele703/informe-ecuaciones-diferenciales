# Informe de Ecuaciones Diferenciales (Cálculo Aplicado)

Vocabulario compartido del trabajo "Simulación numérica de sistemas dinámicos aplicada a
ciberseguridad" de Cálculo Aplicado (UCU, 2026-2): un informe académico en LaTeX más su código
Python. Este archivo es un glosario, no una especificación.

## Language

### La consigna

**Consigna**:
El PDF de la cátedra que define el trabajo
(`material/Simulacion_numerica_de_ecuaciones_diferenciales.pdf`). Tiene seis actividades
numeradas, una investigación sobre gestión de vulnerabilidades, una lista de limitaciones y un
análisis global.
_Avoid_: tarea, ejercicio, letra

**Actividad**:
Cada bloque numerado de la consigna (Actividad 1 a 6). Se usa solo para hablar entre nosotros y
en `docs/REQUISITOS.md`. En el informe **no** aparecen: los resultados se organizan por fenómeno.
_Avoid_: parte, ejercicio, punto, ítem

**Experimento**:
Cada módulo de código: 1 verificación (casos lineal y exponencial), 2 error y comparación de
métodos, 3 gestión de vulnerabilidades. Es una agrupación nuestra, no de la consigna.

**Pregunta de la consigna**:
Cada pregunta suelta de las secciones 5, 6, 7, 8.2, 9, 11.1, 12 y 13. Todas se responden en
Discusión o Conclusiones, sin numerarlas ni citarlas como preguntas.

### Los métodos

**Método de Euler**:
La recurrencia `x_{n+1} = x_n + h f(t_n, x_n)`, `t_n = t_0 + nh`. Es la función `euler` de
`src/metodos.py`. Usa la pendiente al comienzo de cada intervalo.
_Avoid_: Euler explícito (no hay otro en el trabajo), integrador

**Euler mejorado**:
El método de la consigna: predicción con Euler y corrección con el promedio de las pendientes
inicial y predicha. En la bibliografía se lo llama método de Heun; en el informe se usa "Euler
mejorado" y se menciona el otro nombre una vez en el Marco teórico. Es la función
`euler_mejorado`.
_Avoid_: predictor-corrector a secas, Runge-Kutta 2 (es un caso de RK2, pero la consigna no lo
llama así)

**Tamaño del paso (h)**:
El incremento de tiempo entre dos valores consecutivos de la sucesión. Es lo que se varía en
todos los experimentos.
_Avoid_: delta, resolución, incremento

**Número de pasos**:
Cuántas iteraciones hace el método para ir de `t_0` a `t_f`: `round((t_f − t_0)/h)`. Es la medida
de costo computacional del trabajo.
_Avoid_: iteraciones (se acepta en citas de la consigna), evaluaciones

**Solución de referencia**:
La expresión exacta que la consigna da sin pedir que se deduzca: `x = t`, `x = e^{−t}`,
`V = V_0 e^{−kt}`. Es contra lo que se mide el error.
_Avoid_: solución analítica, solución exacta, valor real

**Error absoluto (E_n)**:
`|x(t_n) − x_n|` entre la solución de referencia y la aproximación en el instante `t_n`.
_Avoid_: error a secas, desviación, residuo

**Error final**:
`E_N` en el último instante del intervalo. **Error máximo**: `max_n E_n` sobre todo el intervalo.
Las tablas de la consigna piden los dos.

**Orden del método**:
Cómo escala el error con `h`: Euler es de orden 1 (el error final baja proporcional a `h`),
Euler mejorado es de orden 2 (proporcional a `h²`). Se usa en Discusión para explicar las
pendientes de la figura log-log.

### El modelo de vulnerabilidades

**Modelo de remediación**:
`V' = −kV`, `V(0) = V_0`. `V(t)` es la cantidad de equipos vulnerables; `k > 0` es la **rapidez
de remediación**.
_Avoid_: modelo de decaimiento, modelo exponencial (ese es el nombre de la solución, no del modelo)

**Organización A, B, C**:
Los tres escenarios de la consigna: `V_0 = 1000` y `k = 0.1`, `0.3`, `0.7` respectivamente.

**Modelo discreto**:
La ecuación en diferencias `V_{n+1} = (1 − hk) V_n` que resulta de aplicar Euler al modelo de
remediación. Es una **sucesión geométrica** de razón `1 − hk` y expresión explícita
`V_n = V_0 (1 − hk)^n`.

**Estabilidad**:
Comportamiento del modelo discreto según `hk`: con `0 < hk < 1` decrece y se mantiene positivo;
con `hk = 1` llega a cero en un paso; con `1 < hk < 2` oscila con signo alternado y amplitud
decreciente; con `hk ≥ 2` diverge. "Tiene sentido" para la cantidad de equipos solo si `hk < 1`.
_Avoid_: convergencia (es otra cosa: que la aproximación tienda a la referencia cuando `h → 0`)

**Tasa de aparición (λ)**:
El término constante del modelo `V' = λ − kV`: equipos nuevos que se vuelven vulnerables por
unidad de tiempo. **Equilibrio**: `V* = λ/k`, el valor al que tiende `V(t)`.
_Avoid_: fuente, entrada, inyección

### Ciberseguridad

**Vulnerabilidad**:
Debilidad en un sistema que un atacante puede explotar. **Parche**: la actualización que la
corrige. **Remediación**: el proceso de aplicar la corrección; su **tiempo de remediación** es lo
que el parámetro `k` resume.

**CVE**:
Common Vulnerabilities and Exposures, el catálogo público de vulnerabilidades con identificador
único (MITRE). **CVSS**: Common Vulnerability Scoring System, la escala de severidad (FIRST). Se
usan en el Marco teórico y en las limitaciones (no todas las vulnerabilidades son igual de graves).

**MITRE ATT&CK**:
Base de conocimiento de tácticas y técnicas de atacantes. **T1190, Exploit Public-Facing
Application**: la técnica que la consigna pide investigar; explota vulnerabilidades en servicios
expuestos a Internet. **Superficie de ataque**: el conjunto de puntos por los que un atacante
puede entrar; los equipos sin parchear la agrandan.

### El informe

**Informe**:
El PDF académico que se entrega, compilado desde LaTeX. Sigue la Guía de informe académico:
Resumen, Introducción, Marco teórico, Metodología, Resultados, Discusión, Conclusiones,
Bibliografía.
_Avoid_: entrega, documento, trabajo (cuando se refiere al PDF)

**Trabajo**:
El conjunto informe + código. Es lo que la rúbrica evalúa en tres **dimensiones**: fondo, forma y
código.

**Figura**:
Gráfico generado por el código, numerado correlativamente, con pie de figura autocontenido
debajo. Se cita en el texto por número.

**Tabla**:
Datos tabulados, numerados correlativamente, con título encima y notas debajo. Se exportan desde
el código, nunca se pegan capturas de consola.
_Avoid_: cuadro (aunque LaTeX en español lo imprima así por defecto)

## Flagged ambiguities

- **"Error"** a secas es ambiguo entre error absoluto en un instante, error final y error máximo.
  Siempre se dice cuál.
- **"Estabilidad" y "convergencia"** se confunden. Estabilidad es qué hace el método con un `h`
  dado (oscila, diverge); convergencia es que el error tienda a cero cuando `h → 0`. La consigna
  pide las dos cosas en lugares distintos (Actividad 5 y Actividad 2).
- **"Iteraciones" y "pasos"**: la consigna usa las dos palabras para lo mismo. En el informe se
  usa "pasos", salvo al citar textualmente.
- **"Euler mejorado" y "Heun"**: el mismo método. El informe usa el nombre de la consigna.

## Example dialogue

**Dev:** ¿Dónde va la tabla de Euler contra Euler mejorado?
**Experto:** Es un resultado del experimento 2. La tabla va en la subsección de Resultados sobre
comparación de métodos, y por qué Euler mejorado gana con el mismo `h` (orden 2 contra orden 1) se
explica en Discusión.
**Dev:** ¿Y la pregunta de si tiene sentido una cantidad negativa de equipos?
**Experto:** Es una pregunta de la consigna sobre estabilidad del modelo discreto. La figura con
`hk > 1` va en Resultados; que los valores negativos son un artefacto del método y no del
fenómeno va en Discusión, junto a la condición `hk < 1`.
