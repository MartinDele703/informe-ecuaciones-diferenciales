---
name: session-handoff
description: Save a clean session handoff before leaving a large Claude Code context and continuing in a new terminal. Use when context usage gets high, when the user explicitly asks to hand off / wrap up the session, or before handing the repo to another teammate. Do NOT use /compact.
---

# Session Handoff

Create a clean handoff document so the user (or another teammate) can continue in a fresh Claude
Code terminal without relying on the current conversation context.

Do not compact the session.

Instead, inspect the current project state and write a handoff file to disk.

## Output File

In this repo the handoff lives in `docs/SESSION_HANDOFF.md` (not in the repo root).

If something learned in the session is a durable rule (not just state), also update `CLAUDE.md`.
Never rely on Claude's local auto-memory for that: it does not travel with `git clone`, so the
other teammates would not see it.

Preserve existing useful information. Do not delete prior decisions unless clearly obsolete.

## What to Include

1. Current project goal.
2. Current task or feature being worked on.
3. Current implementation status.
4. Files changed in this session.
5. Important decisions made.
6. Bugs found / fixed / still open.
7. Commands run, and verifications with their results.
8. Pending TODOs and next recommended steps.
9. Assumptions made.
10. User preferences or constraints discovered in this session.
11. Anything the next Claude Code session must know before editing.

## Style

Be concise but complete. Write for a fresh Claude Code session that has not seen the current
conversation. Prefer concrete file paths, commands, decisions, and next actions. Avoid vague
phrases like "we discussed" or "as mentioned earlier". Write in Spanish.

## Final Response

After writing the handoff, respond with:

1. The path of the handoff file.
2. A short summary of what was saved.
3. A reminder to commit and push the handoff, so the rest of the group sees it.
4. The exact prompt to paste into the new terminal:

```text
Leé `docs/SESSION_HANDOFF.md`, `CLAUDE.md` y el git diff actual.

Seguí desde el handoff como si fuera una sesión nueva.

Respondé con exactamente dos cosas:

1. Una tabla de estado, una fila por pendiente del handoff. Columnas: ítem, estado
   (✅ hecho / 🔴 reabierto o roto / ⬜ pendiente / ⏸️ diferido), con pocas palabras sólo si
   cambian lo que yo decidiría.
2. Los próximos 3 pasos, con una recomendación concreta de por cuál empezar.

Si algo del handoff contradice el código, decilo en una línea debajo de la tabla.

No edites archivos hasta después de la tabla y los 3 pasos.
```
