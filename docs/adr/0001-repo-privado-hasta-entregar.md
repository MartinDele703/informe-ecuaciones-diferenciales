---
status: accepted
date: 2026-11-01
---

# Repo privado durante el trabajo, público al entregar

La Guía de informe académico exige poner el link del repositorio en Metodología, por lo que al entregar los docentes deben poder abrirlo sin invitación. Pero `material/` contiene material que no corresponde publicar: el informe de referencia de otras estudiantes y la rúbrica de la cátedra. Decidimos crear el repo **privado** en `MartinDele703`, con los demás autores como colaboradores, subir todo `material/` para que todos trabajen con Claude en el mismo contexto, y **antes de entregar** eliminar del historial los archivos ajenos y pasar el repo a público.

Es la misma decisión que se tomó para `informe-sumatorias` (ADR 0001 de ese repo) y que funcionó. La única diferencia es que este trabajo vive en un repo propio desde el inicio: el anterior se transfirió a otro integrante al terminar, y mezclar los dos trabajos en un solo repo dejaría en el link de Metodología un historial y una estructura que no son de este informe.

## Considered Options

- **Continuar en el repo de `informe-sumatorias`**: reutiliza el scaffolding sin copiar nada, pero el repo ya no es de quien arranca este trabajo (se transfirió), el link del informe apuntaría a dos trabajos, y las herramientas (`tools/`, hooks) asumen `informe/` y `src/` en la raíz.
- **Público desde el inicio sin subir docs ajenos**: evita limpiar historial, pero los compañeros no tendrían el mismo contexto en el repo.
- **Privado siempre, invitando a los docentes**: no tenemos sus usuarios de GitHub y el link del informe no abriría para cualquier lector.

## Consequences

- Existe un checklist de entrega (`docs/ENTREGA.md`) que incluye: `git filter-repo` para borrar `material/Informe Guia_Integracion_Numerica_JuanaYGabriela-4.pdf` y `material/Rúbricas para informes.xlsx` del historial, force push, y cambiar visibilidad a público.
- La consigna y la guía de informe sí quedan en el repo público.
- El scaffolding (hooks, skills, verificador, rúbrica, estructura de `informe/` y `src/`) se copió desde `informe-sumatorias` y se adaptó. Si allá se corrige algo del proceso, hay que traerlo a mano.
