# SESSION_HANDOFF

Fecha: 2026-11-01, sesión 2. Leer también `CLAUDE.md`, `CONTEXT.md`, `docs/REQUISITOS.md`,
`docs/RUBRICA_EVALUACION.md`, `docs/ENTREGA.md` y `docs/adr/0001`.

## 1. Objetivo del proyecto

Informe académico "Simulación numérica de sistemas dinámicos aplicada a ciberseguridad" para
Cálculo Aplicado (UCU, 2026-2), en LaTeX, más el código Python que genera sus figuras y tablas.
Meta: nota máxima según la rúbrica. Es el segundo trabajo del curso; el proceso completo se
hereda de `../informe-sumatorias`.

## 2. Estado: borrador completo del informe, listo para revisión humana

Lo que hay:
- **Código terminado.** `src/metodos.py` (Euler, Euler mejorado, error absoluto) y los tres
  experimentos implementados. `python src/main.py` corre completo, imprime 34 líneas y genera
  7 figuras (`informe/figuras/exp1-lineal`, `exp1-exponencial`, `exp2-error-vs-t`, `exp2-orden`,
  `exp3-organizaciones`, `exp3-estabilidad`, `exp3-lambda`) y 4 tablas (`exp2-error-por-h`,
  `exp2-metodos`, `exp3-valores`, `exp3-equilibrio`). Las figuras son reproducibles byte a byte
  (se vacían los metadatos de fecha del PDF en `comun.guardar_figura`): dos corridas seguidas
  dejan `git status` limpio.
- **Informe completo.** Las ocho secciones escritas (Resumen 295 palabras, Introducción con seis
  objetivos específicos, Marco teórico de unas 4,5 páginas con la investigación de
  ciberseguridad, Metodología, Resultados por fenómeno, Discusión con todas las preguntas de la
  consigna respondidas, Conclusiones que responden los seis objetivos con ordinales,
  Bibliografía con 11 entradas APA verificadas). 25 páginas, compila con Tectonic sin
  `Overfull`/`Underfull` ni referencias rotas.
- **Flujo de redacción corrido** (academic-humanizer → humanamente → humanizer) sobre las ocho
  secciones; marcas en `.claude/hooks/humanizado/`.
- `python tools/verificar_informe.py --todo`: un solo hallazgo, F3, la fecha de la portada.

Lo que NO hay: fecha de entrega en la portada (`[FECHA PENDIENTE]` en `informe/main.tex`),
revisión de los autores, y el repo sigue privado.

## 3. Decisiones de esta sesión

- Estudio de $hk > 1$: $k = 0{,}7$, $V_0 = 1000$, $h \in \{1, 2, 3\}$, $0 \le t \le 30$
  ($hk \in \{0{,}7;\ 1{,}4;\ 2{,}1\}$). Modelo con $\lambda$: $h = 0{,}1$, $0 \le t \le 20$,
  comparado contra $\lambda/k$. Ambas en `CLAUDE.md`.
- La figura de orden (`exp2-orden`) grafica el **error máximo** y no el final: con $h = 1$ Euler
  da exactamente 0 y su error final coincide con $e^{-10}$, chico por casualidad, lo que aplana
  la curva. La Discusión explica ese artefacto. Las tablas siguen con error final, como pide la
  consigna.
- Se trabajó con cinco carriles paralelos en worktrees (tres de código, dos de prosa) y después
  secuencialmente en el contexto principal. El patrón quedó documentado en `CLAUDE.md`.
- Fuentes de ciberseguridad citadas: NIST SP 800-40 Rev. 4 (Souppaya y Scarfone, 2022), glosario
  CSRC de NIST, MITRE ATT&CK T1190 (v2.8, 2026), FIRST CVSS v4.0 (rev. 1.2, 2024), CISA KEV, y la
  FAQ archivada del programa CVE (MITRE, 2021; la única con reserva: cve.org no se pudo leer sin
  JavaScript, se puede reemplazar por el Overview actual abriéndolo en el navegador).
- Trampas nuevas registradas en `CLAUDE.md`: `\%` dentro de modo matemático y `\max` dentro de
  `\caption` rompen con babel en español; comentarios con `\begin{enumerate}`/`\item` confunden el
  chequeo N2 del verificador.

## 3b. Archivos tocados en esta sesión

- `src/experimento1_verificacion.py`, `src/experimento2_error_metodos.py`,
  `src/experimento3_vulnerabilidades.py`: implementados desde el stub.
- `src/comun.py`: `guardar_figura` vacía los metadatos de fecha del PDF.
- `informe/figuras/*.pdf` y `informe/tablas/*.tex`: generados.
- `informe/secciones/00` a `07`: todas escritas (el `07` con las 11 entradas APA).
- `CLAUDE.md`: decisiones de $hk$ y $\lambda$, patrón de carriles, trampas nuevas.
- `.gitignore`: ignora `.claude/worktrees/`.
- `.claude/hooks/humanizado/*.txt`: marcas del flujo de redacción, una por sección.
- Sin cambios: `src/metodos.py`, `src/main.py`, `tools/verificar_informe.py`, `docs/REQUISITOS.md`,
  `CONTEXT.md`, `informe/main.tex` (salvo que sigue con `[FECHA PENDIENTE]`).

## 3c. Errores encontrados y corregidos (ninguno abierto)

- Compilación: `$12\,\%$` en modo matemático (`Incompatible glue units`) y `$\max_n$` dentro de
  un `\caption` (`Argument of \es@a has an extra }`), los dos por babel en español. Corregidos y
  registrados en `CLAUDE.md`.
- Verificador N2 contaba 7 objetivos por un `\item` en un comentario de `01-introduccion.tex`.
- Cada corrida de `main.py` cambiaba los bytes de todas las figuras (fecha en el PDF): resuelto en
  `comun.guardar_figura`.
- Un subagente corrigió en Metodología la afirmación "10/0.1 no da exactamente 100", que era
  falsa en Python; ahora dice que no está garantizado y por qué. Verificado.

## 3d. Supuestos

- Mismo grupo de autores y mismos docentes que en `informe/main.tex`; si cambió, corregir ahí,
  en `CLAUDE.md`, `README.md` y `docs/adr/0001`.
- Versiones de herramientas tomadas de esta máquina (Python 3.12.3, NumPy 1.26.4,
  Matplotlib 3.11.1) y escritas en Metodología; si otro compañero compila con otras, no hace
  falta cambiarlas, pero conviene que coincidan con las de quien corra `main.py` por última vez.

## 4. Verificaciones corridas

- `python src/main.py` completo, sin errores; chequeos a mano de cada experimento (Euler con
  $h = 1$ sobre $x' = -x$ da 0, Euler mejorado 0,5; $V_1 = 300$ y $V_2 = 90$ para la
  organización C con $h = 1$; $hk = 1{,}4$ da $-400, 160$; $\lambda = 200$ termina a 0,75 de
  $666{,}67$).
- `tectonic --keep-logs`: 0 cajas desbordadas, 0 referencias indefinidas, 25 páginas.
- `python tools/verificar_informe.py --todo`: solo F3.
- Revisión visual de portada, índice, páginas de Resultados y bibliografía.

## 5. Próximos pasos recomendados, en orden

1. **Lectura completa del PDF por los tres autores** (`tectonic informe/main.tex`), con
   `docs/RUBRICA_EVALUACION.md` al lado. Especial atención a: el título provisorio de la portada,
   la longitud del Marco teórico (4,5 páginas; si hay que acortar, los candidatos son el párrafo
   del desvío $D_n$ y la comparación de razones $1 - hk < e^{-hk}$), y que la Discusión responda
   cada pregunta de `docs/REQUISITOS.md` §1 con el tono esperado.
2. Poner la fecha de entrega en `informe/main.tex` y revisar los nombres de los docentes.
3. Si se cambia prosa de una sección, el hook avisa; revisar a mano las frases nuevas contra las
   reglas de redacción y volver a marcar con `marcar_humanizado.py` (sin correr los skills de
   nuevo salvo cambios grandes).
4. `docs/ENTREGA.md` antes de entregar; después, hacer público el repo (`docs/adr/0001`).

## 6. Preferencias y restricciones

- No usar `/compact`; cerrar con `/session-handoff` y terminal nueva.
- Texto con comandos LaTeX siempre con Edit o Write, nunca con Python ni heredocs.
- Responder en español rioplatense.
