# informe-ecuaciones-diferenciales

Informe académico de **Cálculo Aplicado** (UCU, 2026-2), trabajo "Simulación numérica de sistemas
dinámicos aplicada a ciberseguridad": un informe en LaTeX más el código Python que genera sus
figuras y tablas. Es el segundo trabajo del curso. El primero, `../informe-sumatorias`, está
terminado y revisado, y este repo hereda de él todo el proceso: estructura, hooks, skills,
verificador y rúbrica. Lo que cambia es la consigna.

Autores del repo: Martín De León, Manuel Chouhy, Joaquín Riál. Fecha de entrega: 1 de noviembre
de 2026. En la portada de esta entrega figuran solo Manuel Chouhy y Joaquín Riál, por decisión
de Martín; no volver a agregarlo.

Respondé siempre en español rioplatense, con ortografía y tildes correctas. Los identificadores de
código quedan en inglés o español según estén.

## Leé esto antes de trabajar

1. `material/Simulacion_numerica_de_ecuaciones_diferenciales.pdf`: la consigna. Es la fuente de
   verdad de QUÉ hay que hacer. Leela completa (las fórmulas se pierden con pdftotext; en esta
   máquina el tool Read no abre PDFs, usar `pymupdf` y leer el texto o renderizar las páginas).
2. `docs/REQUISITOS.md`: la consigna, la guía de informe y la rúbrica destiladas en una lista
   verificable. Es lo que se usa para revisar el trabajo antes de entregar.
3. `CONTEXT.md`: glosario. Usá esos términos y no sus alias.
4. `docs/adr/`: decisiones tomadas y por qué. No las reabras sin decirlo.
5. `material/Informe Guia_Integracion_Numerica_JuanaYGabriela-4.pdf`: informe de otra consigna que
   sacó la nota máxima. Ante una duda de criterio ("¿cómo se presenta X?"), mirá primero cómo lo
   resolvieron ahí y recién después preguntá.
6. `../informe-sumatorias/`: el trabajo anterior del mismo grupo, con la misma estructura y nota
   final pendiente pero revisado contra la rúbrica. Ante una duda de cómo se hizo algo acá (una
   tabla, un pie de figura, la Metodología, la cita de Claude en APA, la portada), mirar cómo
   quedó ahí. No copiar prosa: la consigna es otra.

## Decisiones ya tomadas (no volver a preguntar)

- Se hacen **todas** las actividades de la consigna (1 a 6), la investigación sobre gestión de
  vulnerabilidades (CVE, CVSS, MITRE ATT&CK T1190), las limitaciones del modelo y el análisis
  global, integrados al cuerpo del informe. Esta consigna no tiene BONUS.
- Informe en **LaTeX**, un archivo por sección en `informe/secciones/`, compilado con Tectonic
  (`tectonic informe/main.tex`) o importado en Overleaf.
- Código en `src/`: `metodos.py` (las funciones `euler(f, x0, t0, tf, h)` y
  `euler_mejorado(f, x0, t0, tf, h)` con las firmas **exactas** de la consigna),
  `experimento1_verificacion.py`, `experimento2_error_metodos.py`,
  `experimento3_vulnerabilidades.py`, `comun.py` y `main.py`. Ni un solo archivo gigante ni un
  archivo por actividad. Qué produce cada módulo está en `docs/REQUISITOS.md` §1.
- Los métodos se implementan acumulando con un `for`, paso a paso. No se usa `scipy`, `solve_ivp`
  ni ninguna rutina de integración de biblioteca. NumPy y Matplotlib solo para arreglos y figuras.
- La cantidad de pasos es `round((tf - t0) / h)` y los tiempos se calculan como `t0 + n*h`, no
  acumulando `t += h` (eso arrastra error de redondeo en `t` y desplaza la comparación con la
  solución de referencia).
- Las soluciones de referencia ($x = t$, $x = e^{-t}$, $V = V_0 e^{-kt}$) se usan tal como las da
  la consigna: no se resuelven ecuaciones diferenciales analíticamente. La única deducción
  analítica es la de la Actividad 5 (el modelo discreto $V_{n+1} = (1 - hk)V_n$ es una sucesión
  geométrica), que va en el Marco teórico o en Discusión.
- El estudio de $hk > 1$ (Actividad 5) se hace también numéricamente, con valores de $h$ que la
  consigna no fija, y se presenta como un resultado más sobre estabilidad. Valores elegidos:
  $k = 0{,}7$, $V_0 = 1000$, $h \in \{1, 2, 3\}$, $0 \le t \le 30$, es decir
  $hk \in \{0{,}7;\ 1{,}4;\ 2{,}1\}$: cubren los tres regímenes (decrece, oscila amortiguado,
  diverge) con pasos enteros. Metodología y el experimento 3 usan exactamente esos.
- El modelo con $\lambda$ (Actividad 6) se simula con $h = 0{,}1$ en $0 \le t \le 20$ y se compara
  contra el equilibrio $\lambda / k$, porque la consigna no da solución de referencia.
- No hay aleatoriedad en esta consigna, así que no hay semilla. Si apareciera, se sigue la regla
  del trabajo anterior: semilla maestra en `comun.py`, `numpy.random.default_rng`, una semilla
  distinta por repetición.
- Las figuras se guardan en `informe/figuras/` y las tablas en `informe/tablas/` (formato LaTeX).
  Nada se copia de la consola. La consola solo imprime un resumen corto por experimento.
- La investigación de ciberseguridad (sección 11 de la consigna) usa al menos una fuente técnica
  reconocida (NIST, MITRE, FIRST para CVSS, CISA) citada en APA. Sus conceptos van en el Marco
  teórico y su relación con el modelo ($k$ y el tiempo de remediación, T1190 y la superficie de
  ataque) va en Discusión. No existe una sección "Investigación".
- Repo privado hasta entregar, después público (ver `docs/adr/0001`). El checklist de entrega
  está en `docs/ENTREGA.md`.
- Se cita a Claude en la bibliografía en formato APA y se menciona su uso en Metodología, igual
  que en el trabajo anterior.

## Reglas de calidad que salen de la rúbrica

Errores **graves** (bajan una dimensión a Deficiente o Insuficiente):
- Estructurar el informe como una entrega de ejercicios (secciones "Actividad 1", "Caso 2"). Los
  resultados se organizan por fenómeno dentro de Resultados y Discusión.
- Simbología matemática descuidada (`V_n` en texto plano, fórmulas fuera de modo matemático).
- Que falte un análisis o una pregunta pedida en la consigna, o afirmar algo que los datos no
  muestran. La consigna tiene muchas preguntas sueltas (secciones 6, 7, 8.2, 9, 11.1, 12, 13):
  `docs/REQUISITOS.md` las lista una por una y todas tienen que estar respondidas en el cuerpo.
- Datos en el informe que el código no reproduce.
- Código que no corre, o que imprime miles de líneas en consola.

Errores **leves** a evitar:
- Figuras chicas, feas o sin pie autocontenido; capturas de consola como tabla.
- Introducción más corta que el resumen; resumen de más de 300 palabras.
- Link del repo fuera de Metodología.
- Citas APA mal hechas; referencias que no se usan en el cuerpo del texto.
- Lenguaje coloquial ("nos gustó mucho este trabajo").

Para llegar a 1.0 hacen falta dos dimensiones en Excelente, es decir, sin errores.

## Flujo de trabajo

- El estado y los pendientes están en `docs/SESSION_HANDOFF.md`. Al cerrar una sesión larga,
  `/session-handoff` lo actualiza; commitearlo y pushearlo para que los demás lo vean.
- Si trabaja más de una persona a la vez, cada cambio va en una rama con Pull Request a `main`,
  sin aprobación obligatoria, y antes de arrancar se hace `git pull`. Si trabaja una sola, commits
  directos a `main`.
- No usar `/compact`. Cuando el contexto crece, actualizar el handoff y abrir una terminal nueva
  con Claude Code limpio.
- Lo que se aprenda y valga como regla va a este `CLAUDE.md`, no a la memoria automática de
  Claude: esa memoria es local de cada máquina y los compañeros no la ven.
- Antes de commitear, `python src/main.py` tiene que correr sin errores.
- Commits en español, imperativo, cortos.
- `/grill-with-docs` para discutir un cambio de enfoque antes de implementarlo.
- **Carriles paralelos.** Cuando hay trabajo independiente (un módulo de experimento por carril,
  una sección de prosa por carril), se lanza un subagente por carril con `isolation: "worktree"`
  del tool Agent, cada uno con un brief autocontenido que fija los archivos que puede tocar, los
  parámetros ya decididos y los chequeos a mano que tiene que reportar. Nadie toca `comun.py`,
  `main.py` ni `metodos.py` desde un carril. El contexto principal verifica cada rama contra esos
  chequeos, mergea a `main` y recién después corre el flujo de redacción sobre la prosa. Lo que es
  secuencial (Resultados, Discusión, Conclusiones, Introducción, Resumen) se escribe en el
  contexto principal con una sola voz.
- **Flujo de redacción: obligatorio, una vez por sección, en un subagente.** Cuando una sección
  del informe (`informe/secciones/*.tex`) queda terminada con prosa nueva, y antes de darla por
  lista, se la pasa por los tres skills locales `academic-humanizer` → `humanamente` →
  `humanizer`, se compila y se marca con `marcar_humanizado.py`. Cómo y cuándo está en
  `.claude/hooks/flujo_humanizar.md`; el hook `recordar_humanizar.py` avisa cuando corresponde.
  Reglas para no gastar de más:
  - Se corre **al terminar la sección**, no después de cada Edit, y **en un subagente en
    segundo plano** (una pasada cuesta ~20k tokens); el contexto principal sigue con otra cosa y
    no toca ese archivo hasta que el subagente termina.
  - Los skills no se invocan por iniciativa propia ni en el contexto principal. Si el hook no
    habló, no hay nada que humanizar: cambios de fórmulas, figuras, tablas, `\ref`, comandos
    LaTeX, tildes o frases sueltas no lo activan.
  - Si el hook dice que la sección ya pasó por el flujo y cambió poco, se revisan a mano solo
    las frases nuevas contra las reglas de abajo y se vuelve a marcar. Sin skills.
  - `/humanizar <archivo>` hace la pasada completa a mano, para repasar una sección vieja.
  - Estos skills son solo para la redacción; la estructura y el contenido los definen
    `docs/REQUISITOS.md` y la consigna. Nunca pedir muestras de escritura ni crear perfiles de voz.
- Antes de entregar: `docs/ENTREGA.md`.

## Reglas de redacción (para todo texto nuevo del informe)

- Español académico rioplatense neutro: sin voseo ni tuteo en el informe, sin léxico de España.
- Frases de longitud variada, una idea por frase, verbos concretos ("es", "tiene", "mide").
- Sin rayas (—); usar comas, dos puntos, paréntesis o punto. Sin comillas curvas.
- Sin "no solo X, sino también Y", sin tríadas por reflejo, sin "cabe destacar", "en este sentido",
  "es importante mencionar", "juega un papel fundamental", "en la era de", "profundizar en".
- Sin cierres redondos que repiten el párrafo. Sin gerundios de consecuencia ("..., generando...").
- Toda afirmación cuantitativa apunta a una figura, tabla o referencia. Verbos a la altura de la
  evidencia: "muestra", "sugiere", "es consistente con"; no "demuestra" ni "prueba" salvo prueba real.

## Cómo correr

```
pip install -r requirements.txt
python src/main.py            # corre los tres experimentos y regenera figuras y tablas
python src/main.py 2          # solo el experimento 2
tectonic informe/main.tex     # compila el PDF
```

```
python tools/verificar_informe.py          # chequeos automáticos de la rúbrica (rápido)
python tools/verificar_informe.py --todo   # agrega la corrida completa de src/main.py
```

## Trampas conocidas (heredadas del trabajo anterior; no repetirlas)

- **Backslashes de LaTeX desde Python o heredocs de Bash.** En un string de Python que no es raw,
  `\r` es retorno de carro (y `\t`, `\n`, `\b`, `\f`, `\a`, `\v` también se interpretan), así que
  `\ref`, `\right`, `\begin`, `\frac` y `\times` se rompen. Pasó varias veces, incluso dentro de
  heredocs `<<'EOF'` del tool Bash. Para escribir texto con comandos LaTeX, usar **siempre el
  tool Edit o Write**, nunca Python ni heredocs. Verificar con `grep -n -F '\ref' archivo` y
  contando los CR sueltos a nivel de bytes, que tienen que dar 0:
  `python -c "import re,sys;print(len(re.findall(rb'\r(?!\n)',open(sys.argv[1],'rb').read())))" archivo`.
  No usar `grep -c $'\r'` desde Git Bash: con fines de línea CRLF da falsos positivos.
- Después de cualquier reemplazo masivo, buscar tildes perdidas con grep ("simulacion" por
  "simulación").
- **Los subagentes se equivocan.** Verificar cada hallazgo contra el código o las tablas antes de
  aplicarlo.
- Si alguna tabla mide tiempos (costo computacional de la Actividad 2 o 3), es no determinista:
  sus cifras **no van en la prosa**, que describe la tendencia. En el trabajo anterior el
  verificador tenía un chequeo específico para eso (N1b); si acá se agrega una tabla así, hay que
  volver a agregarlo.
- **Babel en español rompe dos cosas.** Un porcentaje dentro de modo matemático (`$12\,\%$`) da
  `Incompatible glue units`: el signo va afuera, `$12$\,\%`. Y `\max`, `\min`, `\lim` dentro de un
  `\caption` dan `Argument of \es@a has an extra }` porque babel los redefine con tilde: usar
  `\protect\max`.
- El verificador cuenta los `\item` entre el primer `\begin{enumerate}` y el primer
  `\end{enumerate}` de la Introducción, comentarios incluidos: no escribir esos comandos en los
  comentarios de `01-introduccion.tex`.
- Tectonic no escribe el log por omisión. Para ver `Overfull`/`Underfull`:
  `tectonic --keep-logs --keep-intermediates -o <dir> informe/main.tex` y grep sobre `<dir>/main.log`.
- En Windows, el tool Read puede no abrir PDFs: extraer el texto con `pymupdf` o renderizar la
  página (`page.get_pixmap(dpi=110).save(...)`) y leer el PNG. Exportar `PYTHONIOENCODING=utf-8`
  antes de imprimir texto extraído, o la consola tira `UnicodeEncodeError`.
