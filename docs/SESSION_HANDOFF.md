# SESSION_HANDOFF

Fecha: 2026-11-01, sesión 1. Leer también `CLAUDE.md`, `CONTEXT.md`, `docs/REQUISITOS.md`,
`docs/RUBRICA_EVALUACION.md` y `docs/adr/0001`.

## 1. Objetivo del proyecto

Informe académico "Simulación numérica de sistemas dinámicos aplicada a ciberseguridad" para
Cálculo Aplicado (UCU, 2026-2), en LaTeX, más el código Python que genera sus figuras y tablas.
Meta: nota máxima según la rúbrica. Es el segundo trabajo del curso; el proceso completo se
hereda de `../informe-sumatorias` (terminado y revisado).

## 2. Estado: scaffolding listo, contenido sin empezar

Lo que hay:
- Todo el proceso copiado y adaptado desde `informe-sumatorias`: hooks del flujo de redacción,
  skills locales (`academic-humanizer`, `humanamente`, `humanizer`, `session-handoff`),
  comandos (`/humanizar`, `/grill-with-docs`), `.claude/settings.json`, `.gitignore`.
- La consigna leída completa y destilada en `docs/REQUISITOS.md` (ítem por ítem, preguntas
  sueltas incluidas) y en el glosario `CONTEXT.md`.
- `docs/RUBRICA_EVALUACION.md` y `tools/verificar_informe.py` adaptados: la dimensión CÓDIGO
  ahora chequea las firmas exactas `euler(f, x0, t0, tf, h)` y `euler_mejorado(...)` (C1), los
  módulos esperados (C2), docstrings (C3), que no se use scipy ni integradores (C4) y la corrida
  (C5). Se agregó F11 parcial: ningún `[PENDIENTE]` fuera de comentarios.
- `src/metodos.py` implementado: `euler`, `euler_mejorado`, `error_absoluto`,
  `cantidad_de_pasos`. Los tres módulos de experimento son stubs con `correr()` que solo
  imprimen "pendiente"; su docstring dice exactamente qué figuras y tablas tienen que producir y
  con qué nombre.
- `informe/main.tex` con la portada (título provisorio) y las ocho secciones como esqueleto
  con comentarios que dicen qué va en cada una y un `[PENDIENTE]`.

Lo que NO hay: ni una línea de prosa del informe, ni figuras, ni tablas, ni bibliografía (solo
candidatas comentadas en `07-bibliografia.tex`). No hay repo remoto todavía.

## 3. Decisiones de esta sesión

- Repo aparte en vez de seguir en `informe-sumatorias` (ver `docs/adr/0001`): ese repo se
  transfirió a Manuel y el link de Metodología tiene que apuntar a un repo con un solo trabajo.
- Módulos de código: `metodos.py` + tres experimentos (verificación; error y métodos;
  vulnerabilidades). Nombres de figuras y tablas previstos en los docstrings de cada módulo.
- Tiempos como `t0 + n*h`, pasos como `round((tf - t0)/h)`.
- El estudio de `hk > 1` se hace numéricamente con `h` elegidos por nosotros.
- Se asume el mismo grupo de autores que el trabajo anterior (Martín, Manuel, Joaquín). Si el
  grupo cambió, corregir `CLAUDE.md`, `README.md`, `informe/main.tex` y `docs/adr/0001`.

## 4. Verificaciones corridas

- `python src/main.py`: corre y imprime tres líneas de "pendiente".
- `tectonic informe/main.tex`: compila el esqueleto.
- `python tools/verificar_informe.py`: reporta los `[PENDIENTE]`, el resumen vacío y la
  bibliografía sin entradas, como corresponde a un esqueleto.

## 5. Próximos pasos recomendados, en orden

1. Crear el repo remoto privado (`gh auth switch --user MartinDele703` y
   `gh repo create MartinDele703/informe-ecuaciones-diferenciales --private --source . --push`)
   e invitar a los demás autores.
2. Implementar los tres experimentos en `src/` siguiendo los docstrings y
   `docs/REQUISITOS.md` §1. Hacer el 1 primero (es el más corto) y verificar a mano con
   `h = 1` sobre `x' = -x` que Euler da 0 en un paso y Euler mejorado da 0.5.
3. Escribir el informe en este orden: Marco teórico, Metodología, Resultados (con las figuras
   ya hechas), Discusión, Conclusiones, Introducción, Resumen. Una sección por vez; al terminar
   cada una, el hook pide el flujo de redacción en subagente.
4. Investigación de ciberseguridad: buscar y verificar las fuentes (NIST SP 800-40, MITRE ATT&CK
   T1190, FIRST CVSS) antes de citarlas.
5. Revisión final con `docs/RUBRICA_EVALUACION.md` y `tools/verificar_informe.py --todo`.

## 6. Preferencias y restricciones

- No usar `/compact`; cerrar con `/session-handoff` y terminal nueva.
- Texto con comandos LaTeX siempre con Edit o Write, nunca con Python ni heredocs.
- Responder en español rioplatense.
