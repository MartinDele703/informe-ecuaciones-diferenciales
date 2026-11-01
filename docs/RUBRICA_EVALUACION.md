# Rúbrica de evaluación y testing

Rúbrica de revisión final, armada desde las cuatro fuentes del trabajo:

- La rúbrica de la cátedra (no está en el repo): las tres dimensiones, los tipos de error y la
  tabla de notas. Es la que usa la cátedra para poner la nota.
- `material/Guia_de_informe_academico.pdf`: la estructura obligatoria y las reglas de figuras y
  tablas.
- `material/Simulacion_numerica_de_ecuaciones_diferenciales.pdf`: qué hay que hacer.
- Un informe de otra consigna que sacó la nota máxima (no está en el repo), usado como criterio
  de presentación.

`docs/REQUISITOS.md` sigue siendo la lista de QUÉ hay que hacer. Esta rúbrica es CÓMO se
verifica que esté bien hecho y qué pasa si no lo está. Es la misma que se usó en
`../informe-sumatorias`, con la dimensión CÓDIGO adaptada a esta consigna.

## Cómo se pone la nota

La corrección da una nota por cada una de las tres dimensiones:

| Dimensión | Qué evalúa |
|---|---|
| **FONDO** | Calidad académica: comprensión conceptual, elección de métodos, interpretación de resultados, coherencia de las conclusiones, terminología, argumentación. |
| **FORMA** | Comunicación académica: estructura, normas APA, formato, referencias, claridad visual de tablas e imágenes, ortografía y redacción. |
| **CÓDIGO** | Implementación en Python: funcionamiento, reproducibilidad, claridad, organización, comentarios, visualización. |

Cada dimensión recibe una letra:

| Letra | Nombre | Criterio |
|---|---|---|
| I | Insuficiente | Algún error que compromete el trabajo como un todo. |
| D | Deficiente | Algún error grave localizado, o muchos errores leves. |
| E | Aceptable con errores | Varios errores leves que comprometen la calidad. |
| A | Aceptable | Muy pocos errores leves que comprometen la calidad. |
| MB | Muy bueno | Sólo imperfecciones importantes, o un error leve que no compromete la calidad. |
| X | Excelente | **Ningún error.** Pocas o ninguna imperfección. |

Y la nota final sale de la combinación:

| Nota | Criterio mínimo |
|---|---|
| 1.0 | **Como mínimo 2 dimensiones en Excelente** |
| 0.9 | Como mínimo 1 en Excelente |
| 0.8 | Como mínimo 2 en Muy bueno |
| 0.7 | Como mínimo 1 en Muy bueno |

**Consecuencia operativa: para 1.0 hacen falta dos dimensiones sin un solo error.** Un único
error leve en una dimensión la baja a MB como máximo. Por eso esta rúbrica no distingue entre
"error importante" y "detalle": lo que importa es el conteo de errores por dimensión.

## Escala de gravedad

Tomada de la hoja "criterios de clasificación" del Excel:

| Código | Tipo | Definición |
|---|---|---|
| **G1** | Grave global | Afecta el trabajo como un todo. Hunde la dimensión a Insuficiente. |
| **G2** | Grave local | Afecta algo esencial pero localizado. Baja la dimensión a Deficiente. |
| **L1** | Leve que afecta la calidad | Error no ignorable sobre un requisito no esencial. Impide Excelente. |
| **L2** | Leve que no afecta la calidad | Impacto despreciable. Impide Excelente igual. |
| **P** | Imperfección | No está mal, pero es mejorable. Excelente admite pocas. |

## Cómo se corre

```
python tools/verificar_informe.py          # chequeos automáticos (rápido)
python tools/verificar_informe.py --todo   # agrega la corrida completa de src/main.py
tectonic informe/main.tex                  # tiene que compilar sin warnings
```

El script cubre los ítems marcados como **auto** abajo. Los marcados como **manual** exigen
leer y decidir; se revisan con la sección abierta al lado.

---

# Dimensión FORMA

| ID | Qué se verifica | Modo | Si falla |
|---|---|---|---|
| F1 | Las ocho secciones existen, en el orden de la guía, y `main.tex` las incluye. | auto | G1 |
| F2 | Resumen ≤ 300 palabras y estrictamente más corto que la introducción. | auto | G2 |
| F3 | Portada con título descriptivo, autores, curso, docentes, universidad y fecha. Sin marcadores sin completar. | auto | G2 |
| F4 | Toda figura y tabla tiene label y caption, se cita por número en el texto, y el archivo existe. Pie de figura **debajo**, título de tabla **encima**. | auto | L1 |
| F5 | No hay figuras ni tablas en disco que el informe no use. | auto | P |
| F6 | Ninguna `\ref` o `\eqref` rota, ningún label duplicado. | auto | L1 |
| F7 | Cada entrada de bibliografía se cita en el cuerpo. Sin marcadores sin completar. | auto | L1 |
| F8 | El link del repositorio aparece **sólo** en Metodología. | auto | L1 |
| F9 | Sin simbología matemática fuera de modo matemático (`V_n` en texto plano). | auto | G1 si es persistente, L1 si es aislado |
| F10 | Sin caracteres de control, rayas, comillas curvas, muletillas, coloquialismos, palabras repetidas ni tildes antiguas. | auto | L1 |
| F11 | Compila a **un solo PDF**, sin `Overfull \hbox` ni `??` en el texto. | auto (tectonic) | G1 |
| F12 | Las figuras se ven bien en la página: tamaño legible, ejes con unidades, leyenda que no tapa curvas. | **manual** | L1 |
| F13 | Los pies de figura y títulos de tabla son autocontenidos: se entienden sin leer el cuerpo. | **manual** | L1 |
| F14 | Ninguna tabla es una captura de consola. | **manual** | L1 |
| F15 | Formato APA correcto en cada entrada y en cada cita del cuerpo (autor corporativo con sigla la primera vez). | **manual** | L1 |
| F16 | Redacción: sin oraciones mal armadas, sin lenguaje coloquial, sin llamar "ejercicio" ni "actividad" al trabajo. | **manual** | L1/P |

# Dimensión FONDO

| ID | Qué se verifica | Modo | Si falla |
|---|---|---|---|
| N1 | Cada cifra que el texto afirma sale de una tabla o del código. **Ninguna cifra inventada.** | auto (parcial) | G2 |
| N2 | Los objetivos específicos de la introducción se responden uno por uno en las conclusiones. | auto | G2 |
| N3 | La introducción no promete secciones ni análisis que no existan. | auto | G2 |
| N4 | Ningún análisis ni pregunta de la consigna falta. Se recorre `docs/REQUISITOS.md` §1 ítem por ítem, preguntas sueltas incluidas. | **manual** | G1 |
| N5 | Ninguna afirmación contradice la tabla o figura que la respalda. Se lee cada cifra contra su tabla. | **manual** | G2 |
| N6 | Los verbos están a la altura de la evidencia: "muestra", "sugiere", "es consistente con"; nunca "demuestra" sin prueba. | **manual** | L1 |
| N7 | Resultados no interpreta; Discusión no presenta datos nuevos; Conclusiones no presenta resultados nuevos. | **manual** | L1 |
| N8 | El informe **no** está estructurado como entrega de ejercicios: los resultados van por fenómeno, no por actividad. | **manual** | G1 |
| N9 | Toda afirmación fuerte tiene su referencia, interna o externa, y la referencia sostiene lo que se afirma. La investigación de ciberseguridad tiene al menos una fuente técnica reconocida. | **manual** | G2 |
| N10 | Sin errores conceptuales ni terminología mal usada (estabilidad vs. convergencia, error final vs. máximo). Glosario de `CONTEXT.md` respetado. | **manual** | G1 |
| N11 | Las conclusiones se siguen de los datos y no los exceden. | **manual** | G2 |
| N12 | Las decisiones metodológicas están justificadas (por qué escala log, por qué ese `h` donde la consigna no lo fija, por qué esos `hk > 1`). | **manual** | P |

# Dimensión CÓDIGO

| ID | Qué se verifica | Modo | Si falla |
|---|---|---|---|
| C1 | `euler` y `euler_mejorado` existen en `src/metodos.py` con las firmas exactas de la consigna: `(f, x0, t0, tf, h)`. | auto | G2 |
| C2 | Un módulo por experimento, más métodos, utilidades y punto de entrada. Ni un archivo gigante ni uno por actividad. | auto | L1 |
| C3 | Todo módulo y toda función tienen docstring. | auto | L1 |
| C4 | Ninguna rutina de integración de biblioteca (`solve_ivp`, `odeint`, `scipy.integrate`): los métodos se acumulan con `for`. | auto | G2 |
| C5 | `python src/main.py` corre de punta a punta sin errores y no inunda la consola. | auto (`--todo`) | G1 |
| C6 | Los datos del informe se reproducen al correr el código. | **manual** | G1 |
| C7 | El código es legible y está comentado donde hace falta. | **manual** | L1 |
| C8 | Sin prints innecesarios; los que hay aportan información de control. | **manual** | L2 |
| C9 | Los tiempos se calculan como `t0 + n*h`, no acumulando `t += h`. | **manual** | P |

---

## Pendientes que no son errores

Se completan el día de la entrega y hasta entonces el verificador los reporta:

- Fecha de entrega en la portada (`informe/main.tex`).
- Si alguna tabla llega a medir tiempos de cómputo, es no determinista: sus cifras no van en la
  prosa, y hay que volver a agregar al verificador un chequeo como el N1b del trabajo anterior.
