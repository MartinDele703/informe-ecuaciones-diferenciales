"""Hook PostToolUse (Edit|Write): recuerda el flujo de redacción solo cuando hace falta.

Se dispara después de cada Edit o Write, pero habla únicamente si:
  1. el archivo es una sección del informe (informe/secciones/*.tex, salvo la bibliografía), y
  2. el cambio agregó al menos UMBRAL palabras de prosa nueva (fórmulas, comandos LaTeX,
     comentarios y placeholders no cuentan; un \ref o una tilde tampoco).

Si la sección ya pasó por el flujo (hay snapshot en humanizado/), compara con esa versión:
  - pocos cambios acumulados -> pide una revisión manual de las frases nuevas, sin skills;
  - muchos cambios -> pide la pasada completa otra vez.

Nunca bloquea la edición. Sale con código 0 siempre.
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from prosa import es_seccion, leer_snapshot, palabras, palabras_nuevas  # noqa: E402

UMBRAL = 40            # palabras nuevas en un solo cambio para decir algo
PASADA_COMPLETA = 200  # palabras cambiadas desde el último snapshot para repetir los 3 skills
PROPORCION_COMPLETA = 0.30


def responder(mensaje: str) -> None:
    print(json.dumps({
        "hookSpecificOutput": {"hookEventName": "PostToolUse", "additionalContext": mensaje}
    }, ensure_ascii=False))


def main() -> None:
    # Claude Code habla UTF-8; la consola de Windows no siempre.
    for flujo in (sys.stdin, sys.stdout):
        try:
            flujo.reconfigure(encoding="utf-8")
        except Exception:
            pass
    try:
        datos = json.load(sys.stdin)
    except Exception:
        return
    entrada = datos.get("tool_input") or {}
    ruta = entrada.get("file_path") or ""
    if not es_seccion(ruta):
        return
    try:
        actual = palabras(Path(ruta).read_text(encoding="utf-8", errors="ignore"))
    except Exception:
        return

    # Prosa nueva que aportó este cambio en particular.
    if "edits" in entrada:  # MultiEdit
        antes = [p for e in entrada["edits"] for p in palabras(e.get("old_string", ""))]
        despues = [p for e in entrada["edits"] for p in palabras(e.get("new_string", ""))]
    elif "new_string" in entrada:  # Edit
        antes = palabras(entrada.get("old_string", ""))
        despues = palabras(entrada.get("new_string", ""))
    else:  # Write: se compara con el snapshot si existe, si no todo es nuevo
        antes = leer_snapshot(ruta) or []
        despues = actual
    nuevas = palabras_nuevas(antes, despues)
    if nuevas < UMBRAL:
        return

    nombre = ruta.replace("\\", "/").rsplit("/", 1)[-1]
    snapshot = leer_snapshot(ruta)
    if snapshot is not None:
        cambiadas = palabras_nuevas(snapshot, actual)
        if cambiadas < PASADA_COMPLETA and cambiadas < PROPORCION_COMPLETA * max(len(actual), 1):
            responder(
                f"{nombre} ya pasó por el flujo de redacción; desde entonces cambiaron unas "
                f"{cambiadas} palabras. NO repitas los tres skills. Cuando termines con la sección, "
                "revisá vos las frases nuevas contra las 'Reglas de redacción' de CLAUDE.md, "
                f"compilá, y corré `python .claude/hooks/marcar_humanizado.py {ruta}`."
            )
            return
    responder(
        f"Agregaste unas {nuevas} palabras de prosa a {nombre}. Cuando la sección esté terminada "
        "(una sola vez por sección, no después de cada Edit) y antes de responderle al usuario, "
        "delegá el flujo de redacción a un subagente en segundo plano siguiendo "
        ".claude/hooks/flujo_humanizar.md. Mientras corre, no edites ese archivo; seguí con otra "
        "sección o con el código."
    )


if __name__ == "__main__":
    main()
