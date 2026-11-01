"""Utilidades compartidas por los hooks del flujo de redacción.

Extraen la prosa de un archivo LaTeX (sin comentarios, comandos, fórmulas ni placeholders) y
miden cuántas palabras cambiaron entre dos versiones.
"""
import difflib
import re
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
DIR_SNAPSHOTS = Path(__file__).resolve().parent / "humanizado"

_RE_MATE = re.compile(r"\$\$.*?\$\$|\$.*?\$|\\[.*?\\]|\\(.*?\\)", re.DOTALL)
_RE_COMANDO = re.compile(r"\[A-Za-z@]+\*?(\[[^\]]*\])?")
_RE_PALABRA = re.compile(r"[^\W\d_]+", re.UNICODE)


def es_seccion(ruta: str) -> bool:
    """True si la ruta es una sección del informe sujeta al flujo (no la bibliografía)."""
    r = ruta.replace("\\", "/")
    return ("/informe/secciones/" in r or r.startswith("informe/secciones/")) \
        and r.endswith(".tex") and not r.endswith("07-bibliografia.tex")


def lineas_de_prosa(texto: str) -> list[str]:
    """Líneas con prosa: ni comentarios, ni comandos solos, ni placeholders, ni vacías."""
    out = []
    for ln in texto.splitlines():
        s = ln.strip()
        if not s or s.startswith("%") or s.startswith("\\") or "[PENDIENTE]" in s:
            continue
        out.append(s)
    return out


def palabras(texto: str) -> list[str]:
    """Palabras de la prosa, sin fórmulas ni comandos LaTeX."""
    limpio = _RE_MATE.sub(" ", "\n".join(lineas_de_prosa(texto)))
    limpio = _RE_COMANDO.sub(" ", limpio)
    return [p.lower() for p in _RE_PALABRA.findall(limpio)]


def palabras_nuevas(antes: list[str], despues: list[str]) -> int:
    """Cuántas palabras de `despues` no estaban (en ese lugar) en `antes`."""
    sm = difflib.SequenceMatcher(a=antes, b=despues, autojunk=False)
    return sum(j2 - j1 for op, _, _, j1, j2 in sm.get_opcodes() if op in ("insert", "replace"))


def ruta_snapshot(ruta: str) -> Path:
    nombre = ruta.replace("\\", "/").rsplit("/", 1)[-1]
    return DIR_SNAPSHOTS / (nombre + ".txt")


def leer_snapshot(ruta: str) -> list[str] | None:
    p = ruta_snapshot(ruta)
    if not p.exists():
        return None
    return palabras(p.read_text(encoding="utf-8"))


def guardar_snapshot(ruta: str) -> Path:
    texto = Path(ruta).read_text(encoding="utf-8")
    p = ruta_snapshot(ruta)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text("\n".join(lineas_de_prosa(texto)) + "\n", encoding="utf-8")
    return p
