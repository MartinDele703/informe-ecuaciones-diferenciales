# Checklist de entrega

Correr en orden el día que se entrega. Ver `docs/adr/0001-repo-privado-hasta-entregar.md`.

## 1. Verificar el trabajo

- [ ] `python src/main.py` corre de punta a punta sin errores y regenera todas las figuras y tablas.
- [ ] `tectonic informe/main.tex` compila sin warnings de referencias rotas.
- [ ] `python tools/verificar_informe.py --todo` sin hallazgos.
- [ ] Recorrer `docs/REQUISITOS.md` ítem por ítem (pedirle a Claude que lo haga contra el PDF).
- [ ] Fecha en la portada actualizada.
- [ ] Link del repo en Metodología apunta al repo público definitivo.

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

- [ ] Confirmar en GitHub que esos dos archivos no aparecen ni en el historial.
- [ ] Borrar del README y de CLAUDE.md las referencias a esos dos archivos.

## 3. Publicar

```bash
gh repo edit MartinDele703/informe-ecuaciones-diferenciales --visibility public --accept-visibility-change-consequences
```

- [ ] Abrir el link en una ventana de incógnito y verificar que carga.
- [ ] Entregar el PDF (un solo archivo).
