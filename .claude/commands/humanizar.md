---
description: Pasada completa de redacción sobre un archivo .tex del informe, delegada a un subagente en segundo plano (academic-humanizer → humanamente → humanizer → tectonic → marcar)
argument-hint: <ruta a un archivo .tex, por ejemplo informe/secciones/05-discusion.tex>
---

Corré el flujo de redacción sobre `$ARGUMENTS` siguiendo al pie de la letra
`.claude/hooks/flujo_humanizar.md`: un solo subagente en segundo plano con el prompt de ese
archivo, sin correr los skills en este contexto. Mientras el subagente trabaja no edites
`$ARGUMENTS`. Cuando termine, resumime en dos o tres líneas qué cambió cada paso y si compila.
