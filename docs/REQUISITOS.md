# Requisitos del trabajo

Destilado de tres fuentes: la consigna
(`material/Simulacion_numerica_de_ecuaciones_diferenciales.pdf`), la Guía de informe académico
(`material/Guia_de_informe_academico.pdf`) y la rúbrica (`material/Rúbricas para informes.xlsx`).
Cada línea es verificable. Se usa para revisar antes de entregar.

La consigna numera sus actividades del 1 al 6 y además hace preguntas sueltas en las secciones
6, 7, 8.2, 9, 11.1, 12 y 13. Acá se agrupan por módulo de código (experimento) y por sección del
informe, porque el informe **no** se estructura por actividad.

## 1. Qué pide la consigna

### Métodos (`src/metodos.py`)

- [ ] `euler(f, x0, t0, tf, h)` con esa firma exacta (Actividad 1). Recibe la función `f(t, x)`,
      la condición inicial, el tiempo inicial, el tiempo final y el tamaño del paso. Devuelve los
      valores del tiempo, los valores aproximados de `x` y la cantidad de pasos realizados.
- [ ] `euler_mejorado(f, x0, t0, tf, h)` con esa firma exacta (Actividad 3): predicción
      `x̃_{n+1} = x_n + h f(t_n, x_n)` y corrección
      `x_{n+1} = x_n + (h/2) [f(t_n, x_n) + f(t_{n+1}, x̃_{n+1})]`.
- [ ] Error absoluto `E_n = |x(t_n) − x_n|` contra la solución de referencia.
- [ ] Acumulación con `for`, sin rutinas de integración de biblioteca.

### Experimento 1: verificación del método (`src/experimento1_verificacion.py`)

Caso 1, crecimiento lineal: `x' = 1`, `x(0) = 0`, referencia `x(t) = t`, `0 ≤ t ≤ 10`.
- [ ] Euler con `h ∈ {1, 0.5, 0.1}`.
- [ ] Figura: solución de referencia y las tres aproximaciones.
- [ ] Responder: comparación de los resultados y qué efecto tiene disminuir `h` (para `f` constante
      Euler es exacto: las curvas coinciden con la referencia para todo `h`).

Caso 2, decrecimiento exponencial: `x' = −x`, `x(0) = 1`, referencia `x(t) = e^{−t}`, `0 ≤ t ≤ 10`.
- [ ] Euler con `h ∈ {1, 0.5, 0.1, 0.01}`.
- [ ] Figura: referencia y las cuatro aproximaciones en una misma gráfica.
- [ ] Responder: análisis de las diferencias observadas (con `h = 1` la aproximación cae a 0 en un
      paso; con `h` menor se acerca a la exponencial).

### Experimento 2: error, tamaño del paso y comparación de métodos (`src/experimento2_error_metodos.py`)

Actividad 2, sobre `x' = −x`, `x(0) = 1`:
- [ ] Error `E_n` para `h ∈ {1, 0.5, 0.1, 0.05, 0.01}`.
- [ ] Figura: `E_n` en función de `t`, una curva por `h` (escala logarítmica en el eje `y`,
      justificada en Metodología).
- [ ] Tabla: `h`, número de pasos, error final, error máximo, para los cinco `h`.
- [ ] Responder: qué pasa con el error cuando disminuye `h`; qué pasa con el número de
      iteraciones; si existe un compromiso entre precisión y costo computacional; si un paso más
      pequeño siempre es conveniente (error de redondeo acumulado, tiempo de cómputo).

Actividad 3, Euler contra Euler mejorado sobre `x' = −x`, `x(0) = 1`:
- [ ] Tabla: método, `h`, valor final, error final, pasos, para `h ∈ {1, 0.5, 0.1}` y los dos
      métodos (seis filas).
- [ ] Figura opcional pero conveniente: error final contra `h` para ambos métodos en escala
      log-log, que muestra el orden de cada método (pendiente 1 y pendiente 2).
- [ ] Responder: cuál método tiene menor error; si el resultado depende de `h`; cuál requiere
      más operaciones por iteración (Euler mejorado evalúa `f` dos veces); si un método más
      preciso es necesariamente más conveniente en cualquier situación.

### Experimento 3: gestión de vulnerabilidades (`src/experimento3_vulnerabilidades.py`)

Modelo `V' = −kV`, `V(0) = V_0`, referencia `V(t) = V_0 e^{−kt}`.

Actividad 4, organizaciones A (`k = 0.1`), B (`k = 0.3`), C (`k = 0.7`), todas con `V_0 = 1000`,
`0 ≤ t ≤ 20`:
- [ ] Simulación con Euler, `h = 1`, y después `h = 0.5` y `h = 0.1`.
- [ ] Figura: `V(t)` para las tres organizaciones (referencia y aproximación).
- [ ] Tabla: equipos vulnerables aproximados en `t = 5, 10, 15` para cada organización, valor de
      referencia y error, para cada `h`.
- [ ] Responder (8.2): qué representa `k`; cuál organización reduce más rápido los sistemas
      vulnerables; cómo cambia la gráfica cuando aumenta `k`; si es razonable interpretar un `k`
      elevado como mayor capacidad de respuesta; qué factores reales explican valores distintos
      de `k` entre organizaciones.

Actividad 5, modelo discreto `V_{n+1} = (1 − hk) V_n`:
- [ ] Identificar la sucesión (geométrica de razón `1 − hk`) y dar la expresión explícita
      `V_n = V_0 (1 − hk)^n` (va en Marco teórico o Discusión; es la única deducción analítica).
- [ ] Estudiar `lim V_n` según la razón.
- [ ] Determinar para qué valores de `hk` el modelo discreto tiene sentido (`0 < hk < 1`:
      decrece y se mantiene positivo; `hk = 1`: cae a cero en un paso; `1 < hk < 2`: oscila con
      signo alternado y amplitud decreciente; `hk ≥ 2`: diverge).
- [ ] Figura: simulación con `hk > 1` (valores de `h` elegidos por nosotros, por ejemplo
      `hk = 1.5` y `hk = 2.5`) que muestre la oscilación y los valores negativos.
- [ ] Responder: qué ocurre si `hk > 1`; si el método puede producir valores negativos; si tiene
      sentido una cantidad negativa de equipos vulnerables.

Actividad 6, modelo con aparición de nuevas vulnerabilidades `V' = λ − kV`, `V_0 = 1000`,
`k = 0.3`:
- [ ] Simulación con Euler para `λ ∈ {0, 50, 100, 200}` (el `h` lo elegimos y lo justificamos;
      `h = 0.1` es el que menos error tiene de los usados).
- [ ] Figura: `V(t)` para los cuatro `λ`, con el valor de equilibrio `λ/k` marcado.
- [ ] Tabla: `λ`, valor de equilibrio `λ/k`, valor simulado al final del intervalo.
- [ ] Responder: comparación; si el número de equipos vulnerables tiende a disminuir, crecer o
      estabilizarse (se estabiliza en `λ/k`); interpretación para una organización real.

### Investigación: gestión de vulnerabilidades (sección 11; va en Marco teórico y Discusión)

- [ ] Definir con fuente técnica reconocida: vulnerabilidad, parche de seguridad, gestión de
      vulnerabilidades, tiempo de corrección o remediación, CVE, CVSS, priorización de
      vulnerabilidades, consecuencias de mantener sistemas sin actualizar, MITRE ATT&CK.
- [ ] Al menos una fuente técnica reconocida de ciberseguridad (NIST SP 800-40, MITRE ATT&CK,
      FIRST para CVSS, CISA KEV) citada en APA y usada en el cuerpo.
- [ ] Técnica T1190, Exploit Public-Facing Application: en qué consiste; qué relación tiene con
      los sistemas que permanecen vulnerables; por qué reducir el tiempo de remediación
      disminuye la superficie de ataque; qué relación hay entre `k` y el proceso de remediación.

### Limitaciones del modelo (sección 12; va en Discusión)

- [ ] ¿Es razonable suponer que todos los equipos tienen la misma probabilidad de ser parcheados?
- [ ] ¿Es razonable considerar constante `k`?
- [ ] ¿Todos los equipos tienen la misma importancia?
- [ ] ¿Todas las vulnerabilidades tienen la misma severidad? (conectar con CVSS)
- [ ] ¿El modelo considera ataques reales?
- [ ] ¿El modelo considera que pueden aparecer nuevas vulnerabilidades? (conectar con `λ`)
- [ ] ¿Qué habría que incorporar para un modelo más realista?

### Análisis global (sección 13; va en Discusión y se sintetiza en Conclusiones)

- [ ] Relacionar precisión, tamaño del paso y costo computacional.
- [ ] Precisión de Euler; precisión de Euler mejorado; número de iteraciones; efecto del tamaño
      del paso; estabilidad del método; interpretación física o informática de los resultados.

## 2. Qué pide la guía de informe

Estructura obligatoria, en este orden:

- [ ] **Portada**: título descriptivo del problema, nombres de los autores, fecha, curso,
      docentes, universidad.
- [ ] **Resumen**: objetivo, metodología, resultados más relevantes, conclusión principal.
      Máximo 300 palabras. Autosuficiente.
- [ ] **Índice** (el informe de referencia lo incluye).
- [ ] **Introducción**: planteo del problema, justificación, objetivos generales y
      específicos, estructura del informe. Más larga que el resumen.
- [ ] **Marco teórico**: una subsección por concepto clave, solo los que se usan: de la
      derivada a la ecuación en diferencias (cociente incremental), método de Euler, método de
      Euler mejorado (Heun), error absoluto y orden de un método, estabilidad del método para
      `x' = −kx`, sucesión geométrica y modelo discreto, modelo de remediación con y sin
      aparición de nuevas vulnerabilidades (equilibrio `λ/k`), conceptos de gestión de
      vulnerabilidades (CVE, CVSS, remediación, MITRE ATT&CK y T1190).
- [ ] **Metodología**: herramientas (Python, NumPy, Matplotlib, versiones), diseño de cada
      experimento, criterios de análisis, elección de `h` donde la consigna no lo fija, por qué
      escala logarítmica, uso de Claude, **link al repositorio** (solo acá).
- [ ] **Resultados**: datos, figuras y tablas sin interpretación. Organizado por fenómeno
      (verificación, error y paso, comparación de métodos, remediación y efecto de `k`,
      estabilidad del modelo discreto, nuevas vulnerabilidades), no por actividad de la consigna.
- [ ] **Discusión**: interpretación, comparación con la teoría, respuestas a las preguntas de
      la consigna, relación con T1190 y la remediación, limitaciones del modelo, análisis global.
- [ ] **Conclusiones**: síntesis, respuesta a los objetivos uno por uno, recomendaciones,
      líneas futuras. Sin resultados nuevos.
- [ ] **Bibliografía**: todas las fuentes citadas, formato APA, y todas usadas en el cuerpo.
- [ ] Anexo: opcional; no poner ahí nada esencial.

Figuras:
- [ ] Numeradas correlativamente, pie de figura debajo, ejes identificados con unidades
      (tiempo en unidades de tiempo del modelo, equipos vulnerables), leyenda que no tape las
      curvas, autocontenidas.
- [ ] Citadas en el texto por número ("como se observa en la Figura 2").
- [ ] Tamaño legible; nada de figuras chicas ni capturas de pantalla.

Tablas:
- [ ] Numeradas, título encima con unidades, notas debajo, autocontenidas, citadas por número.
- [ ] Generadas desde el código, nunca capturas de consola.

## 3. Qué mira la rúbrica

Tres dimensiones con nota propia: **fondo** (contenido), **forma** (comunicación) y **código**.
Nota final 1.0 requiere al menos dos dimensiones en Excelente (sin errores, pocas imperfecciones).

Errores graves que hunden todo el trabajo:
- [ ] No estructurado como entrega de ejercicios.
- [ ] Ninguna parte de la consigna sin hacer o sin analizar (incluidas las preguntas sueltas).
- [ ] Sin errores conceptuales ni terminología mal usada de forma persistente.
- [ ] Simbología matemática cuidada (todo en modo matemático de LaTeX).
- [ ] Un solo informe, en PDF.
- [ ] Sin fotos de cuaderno.
- [ ] Portada según lo pedido.
- [ ] El código corre, se reproduce y hace lo que el informe dice.

Errores graves localizados:
- [ ] Toda afirmación fuerte apoyada en datos, figuras o referencias.
- [ ] Nada prometido en la introducción que después no aparezca.
- [ ] Metodología suficiente para reproducir.
- [ ] Todos los datos pedidos presentes; ninguno que el código no genere.
- [ ] Conclusiones que se siguen de los datos.
- [ ] Sin prints voluminosos; imports completos.

Errores leves (en naranja en la rúbrica: comprometen la calidad):
- [ ] Ortografía y sintaxis cuidadas; sin errores de tipeo persistentes.
- [ ] Sin terminología rebuscada fuera del alcance del curso sin explicar.
- [ ] Sin capturas de consola como tablas; figuras legibles y estéticas.
- [ ] Cada sección con todas sus partes (la introducción explica objetivos y estructura).
- [ ] Citas APA correctas.
- [ ] Código comentado y ordenado; ni un archivo por actividad ni todo en uno.

Imperfecciones (no son errores, pero suman o restan):
- [ ] No llamar "ejercicio" ni "actividad" al trabajo en el informe.
- [ ] Citar el propio trabajo cuando ayuda ("como se mostró en la sección 2.3").
- [ ] Justificar las decisiones metodológicas (por qué escala log, por qué ese `h` cuando la
      consigna no lo fija, por qué esos `hk > 1`).
- [ ] Hacer algo más de lo pedido (la figura log-log de orden de los métodos, el equilibrio
      `λ/k` marcado en la figura).
- [ ] Comentarios en el código; sin prints innecesarios.
