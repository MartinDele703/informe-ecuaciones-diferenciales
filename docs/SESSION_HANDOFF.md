# SESSION_HANDOFF

Fecha: 2026-11-01, sesión 6. Leer también `CLAUDE.md`, `CONTEXT.md`, `docs/REQUISITOS.md`,
`docs/RUBRICA_EVALUACION.md`, `docs/ENTREGA.md` y `docs/adr/0001`.

Nota del 2026-11-01 (terminal de `../informe-sumatorias`): los cinco retoques leves de la
revisión externa (k como tasa por unidad de tiempo en Introducción y Marco teórico, "única
deducción analítica" quitada, error relativo ubicado en t = 5, "error máximo ... de la cantidad
inicial" en Conclusiones, y el día declarado como unidad de tiempo en Metodología) **ya están
aplicados** en el commit `77bffdc`, verificados (0 cajas, 0 referencias rotas, verificador sin
hallazgos, 0 CR sueltos) y marcados con `marcar_humanizado.py`. No se repiten. Las cuatro
correcciones de §3 se aplicaron en la sesión 5.

## 1. Objetivo del proyecto

Informe académico "Simulación numérica de sistemas dinámicos aplicada a ciberseguridad" para
Cálculo Aplicado (UCU, 2026-2), en LaTeX, más el código Python que genera sus figuras y tablas.
Meta: nota máxima según la rúbrica. Es el segundo trabajo del curso; el proceso completo se
hereda de `../informe-sumatorias`.

## 2. Estado: informe y versión Word terminados; falta entregar

Lo que hay:
- **Código terminado y reproducible.** `python src/main.py` corre completo, imprime 34 líneas,
  genera 7 figuras y 4 tablas y deja `git status` limpio al volver a correr.
- **Informe cerrado.** 25 páginas, compila con Tectonic sin `Overfull`/`Underfull` ni referencias
  rotas. Portada: autores Manuel Chouhy y Joaquín Riál, docentes Maglis Mujica y Candido De
  Oliveira, fecha "1 de noviembre de 2026".
- **Las siete secciones pasaron por el flujo de redacción** (academic-humanizer, humanamente,
  humanizer). Verificado en esta sesión: cero palabras de prosa cambiadas desde la marca de
  `marcar_humanizado.py` en cada una.
- **Revisión final de esta sesión, todo pasó:** `verificar_informe.py --todo` sin hallazgos;
  compilación con `--keep-logs` con 0 cajas desbordadas y 0 referencias indefinidas; 0 retornos
  de carro sueltos en los nueve `.tex`; texto del PDF sin rayas, sin "??", sin "sin embargo",
  "cabe destacar", "demuestra"; las 25 páginas renderizadas y revisadas a ojo.
- **Repo público** en `https://github.com/MartinDele703/informe-ecuaciones-diferenciales`
  (31 commits, historial limpio). El PDF está en `informe/main.pdf` (ignorado por git) y hay una
  copia con nombre de entrega en el Escritorio de Martín
  (`C:\Users\marti\OneDrive\Escritorio\Informe_Simulacion_numerica_Chouhy_Rial.pdf`): hay que
  regenerar las dos después de las correcciones.

Sesión 5: se aplicaron las cuatro correcciones de §3 (commits `6d3474c` y `c636d2f`, pusheados),
se corrió toda la cadena de verificación (main.py, verificador `--todo`, Tectonic con log: 25
páginas, 0 cajas desbordadas, 0 referencias indefinidas, 0 CR sueltos) y se regeneraron
`informe/main.pdf` y la copia del Escritorio (texto idéntico, 18:25). Además se agregó
`\Urlmuskip=0mu plus 1mu` en `main.tex` porque el cambio de fechas de `216d240` había dejado
una caja desbordada de 5 pt en la entrada de CVE de la bibliografía.

Entregables armados en el Escritorio (`C:\Users\marti\OneDrive\Escritorio\`), fuera del repo:
`Informe_Simulacion_numerica_Chouhy_Rial.pdf` (el informe), `informe-ecuaciones-diferenciales.zip`
(`git archive` del commit `9dd2cae` más `informe/main.pdf`), `RESUMEN_CAMBIOS.md` (cambios y
verificaciones para el compañero) y `Informe_Simulacion_numerica_Chouhy_Rial.docx` (versión Word
rehecha en la sesión 6, ver §3f; pisó la que el usuario había rechazado).

Lo que falta: entregar el PDF y marcar el último ítem de `docs/ENTREGA.md`.

## 3f. Versión Word editable: cómo se hizo (sesión 6) y cómo regenerarla

El usuario pidió "el PDF en versión Word editable" que **se vea como el PDF**. La primera versión
(pandoc con estilos por defecto) fue rechazada por el diseño. En la sesión 6 se probó primero
importar el PDF con Word por COM (opción A): descartada porque las Tablas 2 y 3 quedaban
desarmadas, las 1 y 4 como imágenes, las ecuaciones como texto y una figura separada de su pie.
Se hizo entonces la opción B: **pandoc desde las fuentes LaTeX más un posprocesado con
python-docx y Word por COM**. Resultado: 26 páginas (el PDF tiene 25), cada sección empieza en la
misma página que en el PDF salvo Conclusiones (una después), Latin Modern, portada igual, índice
con puntos de guía, encabezados "2.1." en negrita negra, tablas con reglas booktabs, pies en 10 pt,
926 ecuaciones OMML editables, 7 figuras PNG a 200 dpi, bibliografía con sangría francesa,
número de página al pie, sin "??" ni rayas. El `.docx` queda guardado con el índice ya generado.

Decisiones de diseño que no son obvias:
- **Latin Modern se instaló para el usuario** (sin administrador) desde el OTF de GUST
  (`lm2.004otf.zip`), en `%LOCALAPPDATA%\Microsoft\Windows\Fonts` más registro `HKCU`. Word la ve
  como familia **"LM Roman 10"** (no "Latin Modern Roman"). En otra máquina sin la fuente, Word
  sustituye la tipografía y el documento se reacomoda; el contenido no cambia.
- **Interlineado exacto de 13.6 pt** (el `\baselineskip` de 11 pt) en el texto: con "sencillo",
  LM Roman da 45 líneas por página en vez de 52 y el documento se iba a 29 páginas. Los
  encabezados, la portada, las figuras y los párrafos con ecuaciones en bloque quedan en
  interlineado automático para que no se recorten.
- **Silabeo automático en español** (`es-UY`): sin él, Word no corta palabras y cada párrafo
  ocupa más líneas que en LaTeX.
- Los estilos de las entradas del índice se ajustan **por COM con las constantes
  `wdStyleTOC1/2/3`**, porque el Word en español los llama "TDC 1/2" y los estilos "toc 1" que
  agrega python-docx no se usan.
- El índice de Word descarta el espacio ancho U+2003: el separador entre número y título de los
  encabezados son dos espacios normales.
- La bibliografía va alineada a la izquierda (no justificada) porque Word no corta las URL.

Scripts, en `%LOCALAPPDATA%\Temp\claude-handoff\` con el prefijo
`C--Repos-FACULTAD-6to-Sem--2026-2--Calculo-Aplicado-informe-ecuaciones-diferenciales.`:
- `instalar_lm.ps1 -Zip <lm2.004otf.zip> -Ext <carpeta>`: instala la fuente (ya hecho en esta
  máquina; solo hace falta en otra).
- `convertir_word.py <repo> <scratchpad>`: necesita `<scratchpad>/tex/main.aux` de
  `tectonic --keep-intermediates -o <scratchpad>/tex informe/main.tex`; deja
  `<scratchpad>/informe.docx` (contenido correcto, diseño por defecto).
- `disenar_word.py <scratchpad>/informe.docx <salida.docx> <repo>`: aplica todo el diseño.
- `render_guardar.ps1 -Docx <salida.docx> -Pdf <control.pdf>`: ajusta los estilos del índice,
  actualiza campos e índice, **guarda el `.docx`** y exporta un PDF de control para revisarlo
  con pymupdf (`page.get_pixmap`).
Si cambia el informe, se corren los cuatro pasos en ese orden y se copia la salida al Escritorio
con el nombre de entrega. El `.docx` **no** va al repo ni al ZIP.

## 3. Correcciones acordadas en la sesión 4 (aplicadas en la sesión 5)

Vienen de una revisión que mandó un compañero (hecha con su propio agente). Se analizaron una
por una contra el código y los `.tex`; estas cuatro se aceptaron, las demás no (ver §3b).
Cada cambio de prosa es de una o dos frases: el hook `recordar_humanizar` no va a pedir la pasada
completa; revisar a mano contra las reglas de redacción de `CLAUDE.md` y volver a marcar con
`python .claude/hooks/marcar_humanizado.py <archivo>`.

1. **Precisar "con hk ≥ 2 diverge"** en dos lugares. Con hk = 2 la sucesión alterna entre V0 y
   −V0 con amplitud constante (no converge, pero no crece); con hk > 2 la amplitud crece sin
   cota. El Marco teórico (`02-marco-teorico.tex` líneas 169-178) ya lo dice bien; hay que
   alinear:
   - `informe/secciones/05-discusion.tex` líneas 291-292 ("con hk ≥ 2 diverge").
   - `informe/secciones/06-conclusiones.tex` líneas 43-44 ("con hk ≥ 2 diverge").
   Opcional: media frase en `05-discusion.tex` cerca de la línea 156 diciendo que con
   0 < hk ≤ 1 la sucesión no toma valores negativos (con hk = 1 cae a cero en un paso).

2. **Corregir "Ninguna de esas variantes tiene solución de referencia"** en
   `informe/secciones/06-conclusiones.tex` línea 77. Es falso: el modelo con λ y el de clases con
   k propio tienen solución cerrada. Decir "varias de esas variantes no tienen solución de
   referencia conocida", como ya dice `05-discusion.tex` línea 269.

3. **Tabla 3 (`informe/tablas/exp3-valores.tex`): que los valores chicos de la organización C no
   salgan como "0.0".** Hoy la referencia en t = 15 (0.0275) y las aproximaciones de Euler en
   t = 10 y 15 aparecen como `$0.0$`, mientras la prosa dice "menos de uno" (correcto). Se
   arregla en `src/experimento3_vulnerabilidades.py`, función `actividad_organizaciones`
   (líneas 105-125): hoy usa `comun.formato_decimal(valor, 1)` para V y `(..., 2)` para E.
   Propuesta: una función local que use `formato_decimal(x, 1)` si x ≥ 1 y notación científica
   en modo matemático (por ejemplo `$2.8 \times 10^{-2}$`) si 0 < x < 1; aplicar lo mismo a los
   errores E menores que 0.1 si hiciera falta. Agregar al pie de la tabla
   (`04-resultados.tex` líneas 163-166) que las fracciones de equipo corresponden al modelo
   continuo. Después: `python src/main.py 3`, recompilar y recorrer la prosa que cita la tabla
   (`04-resultados.tex` líneas 135-139 y 151-158, `05-discusion.tex` sección 5.3) para que las
   cifras sigan coincidiendo. El verificador tiene el chequeo N1 (cada cifra de la prosa aparece
   en una tabla o en el código): correrlo.

4. **`src/metodos.py`, `cantidad_de_pasos`: fallar con un `ValueError` claro si (tf − t0)/h no
   es entero** (tolerancia relativa del orden de 1e-9) en vez de redondear en silencio. No
   cambiar a paso variable ni a un último paso más corto: rompe el análisis de orden y la firma
   `(f, x0, t0, tf, h)` la fija la consigna. Todos los h del informe dividen exactamente sus
   intervalos (10/0.01, 30/3, 20/0.1). Actualizar el docstring. Si la Metodología describe el
   redondeo (`03-metodologia.tex`, sección 3.2, cerca de "round"), agregar una frase.

Después de las cuatro: `python src/main.py`, `python tools/verificar_informe.py --todo`,
`tectonic --keep-logs --keep-intermediates -o <scratchpad> informe/main.tex` y grep de
`Overfull|Underfull`, contar CR sueltos en los `.tex` tocados, `tectonic -o informe
informe/main.tex`, copiar `informe/main.pdf` al Escritorio con el nombre de entrega, commit y
push. Recién después entregar y marcar el último ítem de `docs/ENTREGA.md`.

## 3b. Puntos de la revisión del compañero que NO se aplican (ya discutidos con el usuario)

- **Distinguir 0 < hk ≤ 1 de 0 < hk < 1 en Resumen y Conclusiones:** ya está. El Marco teórico
  trata hk = 1 aparte y Resumen/Conclusiones dicen "conserva el signo y la monotonía solo si
  0 < hk < 1", que es correcto.
- **Último paso más corto en `euler`/`euler_mejorado`:** rechazado (ver §3 punto 4). Las fórmulas
  de Euler y de Heun se revisaron y están bien.
- **Sacar la entrada de Anthropic/Claude de la bibliografía:** no se hace. APA 7 pide citar las
  herramientas de IA generativa, el trabajo anterior lo hizo así y es una decisión de
  `CLAUDE.md`. Si el grupo cambiara de idea, la cita "(Anthropic, 2026)" de
  `03-metodologia.tex` línea 147 queda huérfana y hay que convertirla en mención sin cita.
- **ZIP del proyecto y README con comandos:** el repo público ya tiene `README.md` con
  instalación y ejecución; el ZIP sobra.

## 3c. Decisiones de esta sesión

- **Fechas de consulta de la bibliografía:** las cinco entradas con "Recuperado el" dicen
  **18 de octubre de 2026** (commit `216d240`). Decisión del usuario; no volver a actualizarlas.
  Se le advirtió que el historial público de GitHub muestra todos los commits del 1 de
  noviembre, y decidió dejarlo así.
- La revisión del compañero se aplica en este repo, no en una copia aparte: una sola versión
  del informe.

## 3d. Archivos tocados en esta sesión

- `informe/secciones/01-introduccion.tex`, `02-marco-teorico.tex`, `03-metodologia.tex`,
  `05-discusion.tex`, `06-conclusiones.tex` y sus marcas en `.claude/hooks/humanizado/`: los
  cinco retoques de la revisión externa (commit `77bffdc`, pusheado, desde la otra terminal).
- `informe/secciones/07-bibliografia.tex`: fechas de consulta (commit `216d240`, pusheado).
- `docs/SESSION_HANDOFF.md`: este archivo.
- `CLAUDE.md`: fechas de la bibliografía agregadas a las decisiones tomadas.

## 3e. Pendientes menores sin decidir

- `README.md` sigue listando a los tres autores del repo (la portada tiene dos). Martín no
  decidió.
- Objetos sueltos en GitHub (`.../commit/5554608` responde HTTP 200 por SHA): purgarlos requiere
  un formulario a GitHub Support. Sin decidir.

## 4. Verificaciones corridas en esta sesión (todas pasaron)

- `python tools/verificar_informe.py --todo`: sin hallazgos, 34 líneas de consola, árbol limpio.
- `tectonic --keep-logs`: 25 páginas, 0 `Overfull`/`Underfull`, 0 referencias indefinidas.
- CR sueltos en `informe/main.tex` y los ocho `.tex` de `secciones/`: 0.
- Marcas de humanizado contra la prosa actual: 0 palabras nuevas en las siete secciones.
- Patrones prohibidos en el texto del PDF (rayas, "??", comillas curvas literales en las fuentes,
  "cabe destacar", "en este sentido", "sin embargo", "demuestra", "De León"): ninguno.
- Después del cambio de fechas: recompilado, verificador sin hallazgos, PDF regenerado y copiado
  al Escritorio.
- Sesión 5, después de las cuatro correcciones: `main.py` completo con árbol limpio, verificador
  `--todo` sin hallazgos, Tectonic con log 25 páginas / 0 cajas / 0 indefinidas, 0 CR sueltos,
  `cantidad_de_pasos` probada a mano (10/0.1, 10/0.01, 30/3, 20/0.1, 3/0.3 pasan; 10/3 y 1/0.3
  lanzan `ValueError`), patrones prohibidos en el PDF a cero, páginas tocadas revisadas a ojo.
- Word de la sesión 6: 26 páginas, 4 tablas reales, 926 ecuaciones OMML, 7 figuras, pies de
  las 7 figuras y 4 tablas presentes, sin "??" ni rayas, secciones en las mismas páginas que el
  PDF (salvo Conclusiones, una después), 187 líneas silabeadas, recortes a 150 dpi de ecuaciones
  en línea y en bloque sin clipping, páginas de control revisadas a ojo contra el PDF.

## 5. Próximos pasos recomendados, en orden

1. Entregar `C:\Users\marti\OneDrive\Escritorio\Informe_Simulacion_numerica_Chouhy_Rial.pdf` y
   marcar el último ítem de `docs/ENTREGA.md`.
2. Decidir `README.md` y los objetos sueltos (§3e), sin apuro.
3. Si el informe cambia, regenerar el Word con los cuatro pasos de §3f.

## 6. Preferencias y restricciones

- No usar `/compact`; cerrar con `/session-handoff` y terminal nueva.
- Texto con comandos LaTeX siempre con Edit o Write, nunca con Python ni heredocs.
- Responder en español rioplatense.
- Operaciones destructivas o de publicación (reescribir historial, push forzado, cambiar
  visibilidad) solo con el visto bueno explícito del usuario en la sesión.
- Antes de corregir algo que pide un revisor externo, verificarlo contra el código y los `.tex`
  y dar la opinión primero; el usuario decide qué se aplica.
- Cualquier versión Word del informe tiene que verse como el PDF (tipografía, portada, tablas,
  numeración), no solo tener el mismo contenido. Mostrar páginas renderizadas antes de darla por
  buena.
- Archivos de sesión 5 tocados en el repo: `src/experimento3_vulnerabilidades.py`,
  `src/metodos.py`, `informe/main.tex`, `informe/tablas/exp3-valores.tex`,
  `informe/secciones/03-metodologia.tex`, `04-resultados.tex`, `05-discusion.tex`,
  `06-conclusiones.tex`, los snapshots de `.claude/hooks/humanizado/` de esas cuatro secciones y
  este handoff. Todo commiteado y pusheado.
