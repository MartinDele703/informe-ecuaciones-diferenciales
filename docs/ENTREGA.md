# Checklist de entrega

Correr en orden el día que se entrega. Ver `docs/adr/0001-repo-privado-hasta-entregar.md`.

## 1. Verificar el trabajo

- [x] `python src/main.py` corre de punta a punta sin errores y regenera todas las figuras y tablas.
- [x] `tectonic informe/main.tex` compila sin warnings de referencias rotas.
- [x] `python tools/verificar_informe.py --todo` sin hallazgos.
- [x] Recorrer `docs/REQUISITOS.md` ítem por ítem (pedirle a Claude que lo haga contra el PDF).
- [x] Fecha en la portada actualizada.
- [x] Link del repo en Metodología apunta al repo público definitivo.

## 2. Limpiar el repo antes de publicarlo

Los archivos ajenos no pueden quedar en un repo público, ni en el historial.

```bash
pip install git-filter-repo
git filter-repo --invert-paths \
  --path "material/Informe Guia_Integracion_Numerica_JuanaYGabriela-4.pdf" \
  --path "material/Rúbricas para informes.xlsx" --force
git remote add origin https://github.com/MartinDele703/informe-ecuaciones-diferenciales.git
git push --force origin main
```

- [x] Confirmar en GitHub que esos dos archivos no aparecen ni en el historial (hecho el
      2026-11-01: los 30 commits de `main` están limpios). Ojo: GitHub conserva un tiempo los
      commits viejos como objetos sueltos, accesibles solo por SHA (`.../commit/5554608`); para
      purgarlos hay que pedirlo a GitHub Support, no alcanza con el push forzado.
- [x] Borrar del README y de CLAUDE.md las referencias a esos dos archivos.

## 3. Publicar

```bash
gh repo edit MartinDele703/informe-ecuaciones-diferenciales --visibility public --accept-visibility-change-consequences
```

- [x] Abrir el link en una ventana de incógnito y verificar que carga (HTTP 200 anónimo, 2026-11-01).
- [ ] Entregar el PDF (un solo archivo).
