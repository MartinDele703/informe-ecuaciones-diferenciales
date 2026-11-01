"""Marca una sección como humanizada: guarda su prosa actual en humanizado/<nombre>.tex.txt.

Uso: python .claude/hooks/marcar_humanizado.py informe/secciones/05-discusion.tex

Lo corre el subagente del flujo de redacción al terminar (después de compilar), o Claude a mano
tras una revisión parcial. El hook recordar_humanizar.py compara contra este snapshot para no
pedir la pasada completa por cambios chicos.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from prosa import es_seccion, guardar_snapshot  # noqa: E402


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    if len(sys.argv) != 2:
        print(__doc__)
        return 2
    ruta = sys.argv[1]
    if not es_seccion(ruta):
        print(f"No es una sección del informe sujeta al flujo: {ruta}")
        return 1
    if not Path(ruta).exists():
        print(f"No existe: {ruta}")
        return 1
    p = guardar_snapshot(ruta)
    print(f"Snapshot guardado en {p.relative_to(Path.cwd()) if p.is_relative_to(Path.cwd()) else p}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
