# Flujo de redacción: cómo delegarlo a un subagente

Este es el procedimiento que sigue Claude (el agente principal) cuando el hook
`recordar_humanizar.py` avisa que una sección quedó con prosa nueva, o cuando el usuario corre
`/humanizar <archivo>`. La pasada completa cuesta unos 20k tokens de instrucciones (los tres
skills suman 14.000 palabras) más tres lecturas del archivo; por eso corre en un subagente y no en
el contexto principal, y por eso se hace **una sola vez por sección**, cuando la sección está
terminada, no después de cada Edit.

Costo medido en la prueba del 2026-09-08 sobre una introducción de 200 palabras: unos 85k tokens
y dos minutos, todo dentro del subagente.

## Qué hace el agente principal

1. Verificar que la sección está terminada (sin `[PENDIENTE]` en lo que se acaba de escribir) y
   que compila. Si todavía falta escribir partes de esa misma sección, seguir escribiendo; el
   flujo va al final.
2. Lanzar **un** subagente con la herramienta `Agent` (`subagent_type: "general-purpose"`, sin
   `model` ni `isolation`) y el prompt de abajo, reemplazando `{ARCHIVO}` por la ruta relativa
   (por ejemplo `informe/secciones/05-discusion.tex`). El subagente corre en segundo plano.
3. Mientras corre: **no editar ese archivo**. Seguir con otra sección, con el código o con lo que
   pida el usuario. Si no hay nada más que hacer, esperar la notificación.
4. Cuando el subagente termina, leer su informe (corto), verificar `git diff --stat` del archivo y
   contarle al usuario en dos o tres líneas qué cambió. No repetir el flujo sobre la misma sección
   salvo que el hook vuelva a pedir la pasada completa.

Nunca correr los tres skills en el contexto principal, ni correrlos "por las dudas" sobre una
sección que el hook no señaló, ni lanzar dos subagentes sobre el mismo archivo a la vez.

## Prompt para el subagente

```
Sos el subagente del flujo de redacción del informe `informe-ecuaciones-diferenciales` (Cálculo Aplicado, UCU).
Trabajás sobre un único archivo: `{ARCHIVO}`. Leé primero la sección "Reglas de redacción" de
`CLAUDE.md`. Respondé en español.

Corré, en este orden y sin saltear pasos, los tres skills locales del proyecto con la
herramienta Skill. Si Skill responde `Unknown skill`, leé `.claude/skills/<nombre>/SKILL.md`
completo (incluida la sección "Ajustes locales para este proyecto") y aplicalo vos, paso por
paso, como si lo hubieras invocado:

1. `academic-humanizer` sobre `{ARCHIVO}`: rigor académico, cada afirmación con su evidencia.
2. `humanamente` sobre el resultado: tics del español generado por IA, registro técnico.
3. `humanizer` sobre el resultado: auditoría final, solo las correcciones necesarias.

Restricciones para los tres pasos: no pedir muestras de escritura, no crear perfiles de voz, no
inventar cómo escribe el autor, no introducir errores deliberados, no agregar ni quitar hechos,
cifras ni citas. El archivo es LaTeX: se edita solo la prosa; comandos, entornos, fórmulas,
`\ref`, `\cite`, `\label`, figuras y tablas quedan intactos. No toques ningún otro archivo.

Al terminar:
4. Compilá con `"$HOME/.local/bin/tectonic" informe/main.tex` (Bash). Si falla por algo que
   rompiste vos, arreglalo; si falla por otra cosa, informalo y no lo toques.
5. Corré `python .claude/hooks/marcar_humanizado.py {ARCHIVO}` para registrar que la sección
   ya pasó por el flujo.

Devolvé un informe de no más de 15 líneas: dos o tres líneas por paso con lo que cambió (tipo de
corrección y cuántas), el resultado de la compilación y el del marcado. No pegues el texto de la
sección ni el diff completo.
```
