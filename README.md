# Informe: Simulación numérica de ecuaciones diferenciales

Cálculo Aplicado, UCU, segundo semestre 2026.
Autores: Martín De León, Manuel Chouhy, Joaquín Riál.

Estudio del método de Euler y de Euler mejorado para aproximar la evolución de un sistema
dinámico: verificación contra soluciones de referencia, efecto del tamaño del paso sobre el error
y el costo, estabilidad del modelo discreto, y aplicación a un modelo simplificado de
remediación de vulnerabilidades en una organización.

## Estructura

```
material/           consigna, guía de informe, rúbrica e informe de referencia
docs/               REQUISITOS.md (lista verificable), RUBRICA_EVALUACION.md, ENTREGA.md, adr/
src/                código Python: metodos.py, un módulo por experimento, comun.py y main.py
tools/              verificar_informe.py: chequeos automáticos de la rúbrica
informe/            LaTeX: main.tex, secciones/, figuras/ y tablas/ generadas por el código
CLAUDE.md           contexto para Claude Code
CONTEXT.md          glosario del trabajo
```

## Setup (Windows, macOS o Linux)

1. **Python 3.12** o superior. Verificar con `python --version`.
2. Clonar e instalar dependencias:
   ```
   git clone https://github.com/MartinDele703/informe-ecuaciones-diferenciales.git
   cd informe-ecuaciones-diferenciales
   pip install -r requirements.txt
   ```
3. **Tectonic** para compilar el LaTeX (una sola vez):
   - Windows: descargar `tectonic-*-x86_64-pc-windows-msvc.zip` desde
     https://github.com/tectonic-typesetting/tectonic/releases y descomprimir `tectonic.exe`
     en una carpeta que esté en el PATH (por ejemplo `%USERPROFILE%\.local\bin`).
   - macOS: `brew install tectonic`
   - Linux: ver https://tectonic-typesetting.github.io/
   Alternativa: subir la carpeta `informe/` a Overleaf.
4. **Claude Code**: https://docs.anthropic.com/en/docs/claude-code . Abrirlo parado en la
   carpeta del repo. Lee `CLAUDE.md` solo y queda con el mismo contexto que el resto del grupo.
   - La primera vez pregunta si confiás en la carpeta: aceptá, porque si no, no carga el hook ni
     los skills del repo.
   - `.claude/settings.json` declara los plugins `superpowers` y `claude-md-management`; Claude
     Code ofrece instalarlos al abrir el repo. Si no lo ofrece:
     `/plugin install superpowers@claude-plugins-official` y
     `/plugin install claude-md-management@claude-plugins-official`.
   - Para retomar el trabajo, pegale este prompt a una sesión nueva:
     `Leé docs/SESSION_HANDOFF.md, CLAUDE.md y el git diff actual, y seguí desde el handoff.`

## Uso

```
python src/main.py        # corre los tres experimentos, guarda figuras y tablas
python src/main.py 1      # solo el experimento 1 (verificación)
tectonic informe/main.tex # genera informe/main.pdf
python tools/verificar_informe.py   # chequeos automáticos de la rúbrica
```

Comandos de Claude Code disponibles en el repo:
- `/grill-with-docs`: discutir un cambio de enfoque contra el glosario y las decisiones antes de hacerlo.
- `/session-handoff`: actualiza `docs/SESSION_HANDOFF.md` antes de cerrar una sesión larga (no
  usamos `/compact`). Commitealo y pushealo para que los demás lo vean.
- `/humanizar <archivo.tex>`: pasada completa de redacción sobre una sección, delegada a un
  subagente (`academic-humanizer` → `humanamente` → `humanizer` → compilar → marcar).

El flujo de redacción se dispara solo, pero únicamente cuando hace falta. Un hook de proyecto
(`.claude/settings.json` + `.claude/hooks/recordar_humanizar.py`) corre después de cada Edit o
Write y habla solo si el cambio agregó al menos 40 palabras de prosa a una sección de
`informe/secciones/` (fórmulas, comandos LaTeX, `\ref`, tildes o frases sueltas no cuentan).
Entonces Claude, al terminar la sección, lanza un subagente en segundo plano que corre los tres
skills, compila y guarda un snapshot de la prosa en `.claude/hooks/humanizado/`. Si más adelante
la sección cambia poco respecto de ese snapshot, el hook pide una revisión manual de las frases
nuevas en lugar de repetir la pasada completa. Los detalles están en
`.claude/hooks/flujo_humanizar.md`. El hook necesita `python` en el PATH (en macOS, si solo
existe `python3`, cambiá el comando en `.claude/settings.json`). Podés ver el hook cargado con
`/hooks` dentro de Claude Code.
