"""Verificación automática del informe contra la rúbrica de `docs/RUBRICA_EVALUACION.md`.

Cubre los ítems de la rúbrica que se pueden decidir sin criterio humano. Cada chequeo
imprime una línea con su identificador, el resultado y el detalle de lo que encontró.
Los ítems que exigen juicio (calidad del análisis, coherencia de las conclusiones) quedan
en la rúbrica y no acá.

Heredado de `informe-sumatorias/tools/verificar_informe.py`; la dimensión CÓDIGO está
adaptada a esta consigna (firmas de los métodos, sin rutinas de integración de biblioteca).

Uso:
    python tools/verificar_informe.py           # todo salvo la corrida del código
    python tools/verificar_informe.py --todo    # agrega la corrida completa de src/main.py

Devuelve 0 si no hay hallazgos y 1 si hay alguno.
"""

from __future__ import annotations

import ast
import re
import subprocess
import sys
import unicodedata
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
SECCIONES = RAIZ / "informe" / "secciones"
TABLAS = RAIZ / "informe" / "tablas"
FIGURAS = RAIZ / "informe" / "figuras"
MAIN_TEX = RAIZ / "informe" / "main.tex"
SRC = RAIZ / "src"

ORDEN = [
    "00-resumen", "01-introduccion", "02-marco-teorico", "03-metodologia",
    "04-resultados", "05-discusion", "06-conclusiones", "07-bibliografia",
]

MULETILLAS = [
    "cabe destacar", "en este sentido", "es importante mencionar",
    "juega un papel fundamental", "en la era de", "profundizar en",
    "no solo x", "vale la pena", "a modo de cierre", "en definitiva",
]

COLOQUIAL = ["nos gustó", "nos gusto", "este ejercicio", "el ejercicio", "la tarea 1",
             "esta actividad", "la actividad 1", "la actividad 2", "la actividad 3",
             "la actividad 4", "la actividad 5", "la actividad 6"]

# Módulos que tiene que haber en src/ (C2) y firmas exactas que pide la consigna (C1).
MODULOS_ESPERADOS = {"comun.py", "main.py", "metodos.py", "experimento1_verificacion.py",
                     "experimento2_error_metodos.py", "experimento3_vulnerabilidades.py"}
FIRMAS_CONSIGNA = {"euler": ["f", "x0", "t0", "tf", "h"],
                   "euler_mejorado": ["f", "x0", "t0", "tf", "h"]}
INTEGRADORES_PROHIBIDOS = {"solve_ivp", "odeint", "ode", "RK45", "quad"}

hallazgos: list[tuple[str, str]] = []
notas: list[str] = []


def falla(ident: str, detalle: str) -> None:
    hallazgos.append((ident, detalle))


def texto_secciones() -> dict[str, str]:
    return {p.stem: p.read_text(encoding="utf-8") for p in SECCIONES.glob("*.tex")}


def sin_comentarios(t: str) -> str:
    return re.sub(r"(?m)(?<!\\)%.*$", "", t)


def palabras(t: str) -> int:
    t = sin_comentarios(t)
    t = re.sub(r"\$[^$]*\$", "X", t)
    t = re.sub(r"\\begin\{[^}]*\}|\\end\{[^}]*\}", " ", t)
    t = re.sub(r"\\[a-zA-Z]+\*?", " ", t)
    t = re.sub(r"[{}\\]", " ", t)
    return len([w for w in t.split() if any(c.isalnum() for c in w)])


# --------------------------------------------------------------------------- FORMA

def f1_estructura(sec: dict[str, str]) -> None:
    """F1: las ocho secciones existen, en orden, y main.tex las incluye."""
    faltan = [s for s in ORDEN if s not in sec]
    if faltan:
        falla("F1", f"faltan secciones: {faltan}")
        return
    main = MAIN_TEX.read_text(encoding="utf-8")
    incluidas = re.findall(r"\\input\{secciones/([^}]*)\}", main)
    if incluidas != ORDEN:
        falla("F1", f"orden en main.tex: {incluidas}")


def f2_resumen(sec: dict[str, str]) -> None:
    """F2: resumen <= 300 palabras y estrictamente más corto que la introducción."""
    r, i = palabras(sec["00-resumen"]), palabras(sec["01-introduccion"])
    notas.append(f"resumen {r} palabras, introduccion {i}")
    if r > 300:
        falla("F2", f"resumen de {r} palabras (tope 300)")
    if i <= r:
        falla("F2", f"introduccion ({i}) no supera al resumen ({r})")


def f3_portada() -> None:
    """F3: la portada tiene título, autores, curso, docentes, universidad y fecha."""
    main = MAIN_TEX.read_text(encoding="utf-8")
    bloque = main[main.find("titlepage"):main.find("end{titlepage}")]
    requisitos = {
        "universidad": "Universidad",
        "autores": "Chouhy",
        "curso": "Cálculo Aplicado",
        "docentes": "Docentes:",
    }
    for nombre, marca in requisitos.items():
        if marca not in bloque:
            falla("F3", f"la portada no tiene {nombre}")
    if re.search(r"\[.*PENDIENTE.*\]|\[FECHA\]", bloque):
        falla("F3", "la portada tiene un marcador sin completar")


def f4_figuras_tablas(sec: dict[str, str]) -> None:
    """F4: toda figura y tabla existe, se cita por número y tiene pie o título."""
    todo = "".join(sec.values())
    for entorno, carpeta, ext in (("figure", FIGURAS, ".pdf"), ("table", TABLAS, ".tex")):
        for bloque in re.findall(rf"\\begin\{{{entorno}\}}(.*?)\\end\{{{entorno}\}}", todo, re.S):
            lab = re.search(r"\\label\{([^}]*)\}", bloque)
            if not lab:
                falla("F4", f"{entorno} sin \\label")
                continue
            if not re.search(r"\\caption\{", bloque):
                falla("F4", f"{entorno} {lab.group(1)} sin caption")
            if f"\\ref{{{lab.group(1)}}}" not in todo:
                falla("F4", f"{lab.group(1)} no se cita en el texto")
            arch = re.search(r"\\(?:includegraphics|input)(?:\[[^\]]*\])?\{([^}]*)\}", bloque)
            if arch:
                nombre = Path(arch.group(1)).name
                if not (carpeta / nombre).exists() and not (carpeta / (nombre + ext)).exists():
                    falla("F4", f"{lab.group(1)} apunta a un archivo inexistente: {nombre}")
    # el caption de una tabla va antes del \input y el de una figura después del gráfico
    for bloque in re.findall(r"\\begin\{table\}(.*?)\\end\{table\}", todo, re.S):
        if bloque.find("\\caption") > bloque.find("\\input"):
            falla("F4", "tabla con el título debajo (la guía lo pide encima)")
    for bloque in re.findall(r"\\begin\{figure\}(.*?)\\end\{figure\}", todo, re.S):
        if bloque.find("\\caption") < bloque.find("\\includegraphics"):
            falla("F4", "figura con el pie encima (la guía lo pide debajo)")


def f5_huerfanos(sec: dict[str, str]) -> None:
    """F5: no sobran ni faltan figuras y tablas en disco."""
    todo = "".join(sec.values())
    usadas_f = {Path(m).name for m in re.findall(r"\\includegraphics(?:\[[^\]]*\])?\{([^}]*)\}", todo)}
    en_disco_f = {p.name for p in FIGURAS.glob("*.pdf")}
    if en_disco_f - usadas_f:
        falla("F5", f"figuras en disco que el informe no usa: {sorted(en_disco_f - usadas_f)}")
    usadas_t = {Path(m).name + ".tex" for m in re.findall(r"\\input\{tablas/([^}]*)\}", todo)}
    en_disco_t = {p.name for p in TABLAS.glob("*.tex")}
    if en_disco_t - usadas_t:
        falla("F5", f"tablas en disco que el informe no usa: {sorted(en_disco_t - usadas_t)}")


def f6_referencias(sec: dict[str, str]) -> None:
    """F6: \\ref y \\eqref resuelven, no hay labels duplicados."""
    todo = "".join(sec.values()) + MAIN_TEX.read_text(encoding="utf-8")
    labels = re.findall(r"\\label\{([^}]*)\}", todo)
    for l in {l for l in labels if labels.count(l) > 1}:
        falla("F6", f"label duplicado: {l}")
    for r in set(re.findall(r"\\(?:ref|eqref)\{([^}]*)\}", todo)):
        if r not in labels:
            falla("F6", f"referencia rota: {r}")


def f7_apa(sec: dict[str, str]) -> None:
    """F7: cada entrada de bibliografía se cita en el cuerpo y viceversa."""
    bib = sec["07-bibliografia"]
    cuerpo = "".join(v for k, v in sec.items() if k != "07-bibliografia")
    entradas = re.findall(r"\\item\[\]\s*([^.(]+)\((\d{4})\)", bib)
    # autores corporativos: la cita en el cuerpo usa la sigla, no la última palabra del nombre
    siglas = {"Electronics": "IEEE", "Standardization": "ISO", "Technology": "NIST",
              "Corporation": "MITRE", "Teams": "FIRST", "Agency": "CISA"}
    for autor, anio in entradas:
        apellido = autor.strip().split(",")[0].split(" et al")[0].strip()
        clave = apellido.split()[-1] if apellido else ""
        sigla = siglas.get(clave, clave)
        if sigla not in cuerpo and clave not in cuerpo:
            falla("F7", f"entrada de bibliografía no citada en el cuerpo: {clave} ({anio})")
    if re.search(r"\[FECHA\]|\[PENDIENTE\]", bib):
        falla("F7", "la bibliografía tiene un marcador sin completar")


def f8_repo_en_metodologia(sec: dict[str, str]) -> None:
    """F8: el link del repositorio aparece sólo en Metodología."""
    for nombre, t in sec.items():
        if "github.com" in t and nombre != "03-metodologia":
            falla("F8", f"link del repo fuera de Metodología: {nombre}")


def f9_simbologia(sec: dict[str, str]) -> None:
    """F9: sin variables con subíndice fuera de modo matemático."""
    for nombre, t in sec.items():
        limpio = sin_comentarios(t)
        fuera = re.sub(r"\$[^$]*\$|\\begin\{equation\}.*?\\end\{equation\}", "", limpio, flags=re.S)
        fuera = re.sub(r"\\(?:texttt|url|label|ref|eqref|input|includegraphics)\{[^}]*\}", "", fuera)
        for m in re.findall(r"\b[a-zA-Z]_[a-zA-Z0-9]", fuera):
            falla("F9", f"{nombre}: simbología fuera de modo matemático: {m}")


def f10_ortografia(sec: dict[str, str]) -> None:
    """F10: sin caracteres de control, rayas, comillas curvas, muletillas ni coloquialismos."""
    for nombre, t in sec.items():
        for ch in t:
            if unicodedata.category(ch) == "Cc" and ch not in "\n\t":
                falla("F10", f"{nombre}: caracter de control U+{ord(ch):04X}")
                break
        for mala, desc in (("\u2014", "raya"), ("\u201c", "comilla curva"),
                           ("\u201d", "comilla curva"), ("\u2018", "comilla curva")):
            if mala in t:
                falla("F10", f"{nombre}: {desc}")
        limpio = sin_comentarios(t).lower()
        for m in MULETILLAS + COLOQUIAL:
            if m in limpio:
                falla("F10", f"{nombre}: muletilla o coloquialismo '{m}'")
        for m in re.finditer(r"\b(\w{4,})\s+\1\b", limpio):
            falla("F10", f"{nombre}: palabra repetida '{m.group(1)}'")
        for m in re.finditer(r"\bsólo\b|\bfué\b|\bguión\b|\bésta\b|\béste\b", limpio):
            falla("F10", f"{nombre}: tilde antigua '{m.group(0)}'")


def f11_pendientes(sec: dict[str, str]) -> None:
    """F11 (parcial): ninguna sección tiene un marcador [PENDIENTE] fuera de un comentario."""
    for nombre, t in sec.items():
        if "[PENDIENTE]" in sin_comentarios(t):
            falla("F11", f"{nombre}: queda un marcador [PENDIENTE]")


# --------------------------------------------------------------------------- FONDO

def n1_cifras_en_tablas(sec: dict[str, str]) -> None:
    """N1: cada cifra medida que el texto afirma aparece en una tabla o en el código.

    Es el chequeo que impide afirmar en el texto un número que el código no generó.
    En Resultados, Conclusiones y Resumen toda cifra en notación científica es una medición
    y su ausencia es un hallazgo. En el Marco teórico y la Discusión puede haber cotas
    calculadas a mano; esas se listan para revisión manual en vez de marcarse.
    """
    fuente = "".join(p.read_text(encoding="utf-8") for p in TABLAS.glob("*.tex"))
    fuente += "".join(p.read_text(encoding="utf-8") for p in SRC.glob("*.py"))
    patron = re.compile(r"(\d\.\d{2})\s*\\times\s*10\^\{(-?\d+)\}")
    conocidas = {(m.group(1), m.group(2)) for m in patron.finditer(fuente)}
    medidas = {"04-resultados", "06-conclusiones", "00-resumen"}
    for nombre, t in sec.items():
        for m in patron.finditer(sin_comentarios(t)):
            if (m.group(1), m.group(2)) in conocidas:
                continue
            if nombre in medidas:
                falla("N1", f"{nombre}: {m.group(0)} no aparece en ninguna tabla ni en el código")
            else:
                notas.append(f"N1 revisar a mano (cifra derivada): {nombre}: {m.group(0)}")


def n2_objetivos(sec: dict[str, str]) -> None:
    """N2: los objetivos específicos de la introducción se responden en las conclusiones."""
    intro = sec["01-introduccion"]
    bloque = re.search(r"\\begin\{enumerate\}(.*?)\\end\{enumerate\}", intro, re.S)
    if not bloque:
        falla("N2", "la introducción no tiene una lista de objetivos específicos")
        return
    n = len(re.findall(r"\\item", bloque.group(1)))
    notas.append(f"{n} objetivos específicos en la introducción")
    concl = sec["06-conclusiones"].lower()
    ordinales = ["primer", "segundo", "tercer", "cuarto", "quinto", "sexto", "séptimo", "octavo"]
    respondidos = sum(1 for o in ordinales[:n] if o in concl)
    if respondidos < n:
        falla("N2", f"{n} objetivos pero sólo {respondidos} referidos en conclusiones")


def n3_promesas(sec: dict[str, str]) -> None:
    """N3: la introducción no promete secciones que no existan."""
    for r in set(re.findall(r"\\ref\{(sec:[^}]*)\}", sec["01-introduccion"])):
        if f"\\label{{{r}}}" not in "".join(sec.values()):
            falla("N3", f"la introducción referencia una sección inexistente: {r}")


# --------------------------------------------------------------------------- CÓDIGO

def c1_firmas() -> None:
    """C1: euler y euler_mejorado existen en metodos.py con las firmas exactas de la consigna."""
    ruta = SRC / "metodos.py"
    if not ruta.exists():
        falla("C1", "no existe src/metodos.py")
        return
    arbol = ast.parse(ruta.read_text(encoding="utf-8"), filename=ruta.name)
    definidas = {n.name: [a.arg for a in n.args.args]
                 for n in ast.walk(arbol) if isinstance(n, ast.FunctionDef)}
    for nombre, firma in FIRMAS_CONSIGNA.items():
        if nombre not in definidas:
            falla("C1", f"metodos.py no define {nombre}()")
        elif definidas[nombre] != firma:
            falla("C1", f"{nombre}({', '.join(definidas[nombre])}) no tiene la firma de la "
                        f"consigna ({', '.join(firma)})")


def c2_modulos() -> None:
    """C2: un módulo por experimento, más métodos, utilidades y punto de entrada."""
    hay = {p.name for p in SRC.glob("*.py")}
    if MODULOS_ESPERADOS - hay:
        falla("C2", f"faltan módulos: {sorted(MODULOS_ESPERADOS - hay)}")
    if hay - MODULOS_ESPERADOS:
        notas.append(f"módulos extra: {sorted(hay - MODULOS_ESPERADOS)}")


def c3_docstrings() -> None:
    """C3: toda función tiene docstring y todo módulo también."""
    for p in SRC.glob("*.py"):
        arbol = ast.parse(p.read_text(encoding="utf-8"), filename=p.name)
        if not ast.get_docstring(arbol):
            falla("C3", f"{p.name}: el módulo no tiene docstring")
        for nodo in ast.walk(arbol):
            if isinstance(nodo, (ast.FunctionDef, ast.AsyncFunctionDef)):
                if not ast.get_docstring(nodo):
                    falla("C3", f"{p.name}:{nodo.lineno}: {nodo.name}() sin docstring")


def c4_sin_integradores() -> None:
    """C4: ninguna rutina de integración de biblioteca; los métodos se acumulan con for.

    Se recorre el árbol sintáctico y no el texto, para no confundir una llamada real con
    la mención dentro de un docstring que aclara que no se usa.
    """
    for p in SRC.glob("*.py"):
        arbol = ast.parse(p.read_text(encoding="utf-8"), filename=p.name)
        for nodo in ast.walk(arbol):
            if isinstance(nodo, (ast.Import, ast.ImportFrom)):
                modulo = getattr(nodo, "module", None) or ""
                nombres = [a.name for a in nodo.names]
                if "scipy" in modulo or any("scipy" in n for n in nombres):
                    falla("C4", f"{p.name}:{nodo.lineno}: importa scipy")
            if isinstance(nodo, ast.Call):
                f = nodo.func
                nombre = f.id if isinstance(f, ast.Name) else (f.attr if isinstance(f, ast.Attribute) else "")
                if nombre in INTEGRADORES_PROHIBIDOS:
                    falla("C4", f"{p.name}:{nodo.lineno}: llamada a {nombre}()")


def c5_corrida(completa: bool) -> None:
    """C5: el código corre sin errores y no inunda la consola."""
    if not completa:
        notas.append("C5 omitido (correr con --todo)")
        return
    r = subprocess.run([sys.executable, str(SRC / "main.py")],
                       capture_output=True, text=True, cwd=RAIZ, timeout=900)
    if r.returncode != 0:
        falla("C5", f"src/main.py terminó con código {r.returncode}: {r.stderr[-400:]}")
    lineas = [l for l in r.stdout.splitlines() if l.strip()]
    notas.append(f"la corrida imprimió {len(lineas)} líneas")
    if len(lineas) > 40:
        falla("C5", f"consola demasiado voluminosa: {len(lineas)} líneas")


# --------------------------------------------------------------------------- main

def main() -> int:
    completa = "--todo" in sys.argv
    sec = texto_secciones()

    f1_estructura(sec)
    f2_resumen(sec)
    f3_portada()
    f4_figuras_tablas(sec)
    f5_huerfanos(sec)
    f6_referencias(sec)
    f7_apa(sec)
    f8_repo_en_metodologia(sec)
    f9_simbologia(sec)
    f10_ortografia(sec)
    f11_pendientes(sec)
    n1_cifras_en_tablas(sec)
    n2_objetivos(sec)
    n3_promesas(sec)
    c1_firmas()
    c2_modulos()
    c3_docstrings()
    c4_sin_integradores()
    c5_corrida(completa)

    for n in notas:
        print(f"  nota  {n}")
    print()
    if not hallazgos:
        print("sin hallazgos: los chequeos automáticos de la rúbrica pasan")
        return 0
    for ident, detalle in dict.fromkeys(hallazgos):
        print(f"{ident:5s} {detalle}")
    print(f"\n{len(set(hallazgos))} hallazgos")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
