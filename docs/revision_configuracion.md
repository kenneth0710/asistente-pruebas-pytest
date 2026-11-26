# Revisión del pipeline y del Dockerfile

Proyecto: asistente-pruebas-pytest
Fecha: 2026-11-26

Plantilla de la práctica de la semana 9. El pipeline ya está revisado; el Dockerfile se agrega en el siguiente paso del plan.

## 1. Cómo se generaron

**Herramienta de IA:** ChatGPT (versión web)
**Prompt del pipeline:** [`prompt16_pipeline.txt`](prompts/prompt16_pipeline.txt) (entrada 19 de la [bitácora](../bitacora_ia.md))
**Prompt del Dockerfile:** pendiente

## 2. Hallazgos

El pipeline lo pedí desde el principio con las restricciones de seguridad del curso, así que no trae los errores típicos del ejemplo de clase (`write-all`, clave en `env`, `3.10` sin comillas, acción de terceros, `|| true`). Revisé cada punto de la lista de la semana:

| Archivo y línea | Revisión | Resultado |
|---|---|---|
| ci.yml:3-5 | Eventos | `push` y `pull_request`. Correcto. Al no filtrar ramas, en un pull request desde una rama propia corre dos veces; se acepta porque el repositorio es de una sola persona. |
| ci.yml:7-8 | Permisos | `contents: read`, el mínimo. Correcto. |
| ci.yml | Secretos | No hay `env` ni claves. El asistente todavía no llama a la API de Gemini, así que el pipeline no necesita `GEMINI_API_KEY`. |
| ci.yml:17, 22, 39 | Acciones y versiones | Solo acciones oficiales (`actions/…`), con versión exacta. Comprobé con `gh api` que las tres etiquetas existen. **Riesgo residual:** una etiqueta se puede mover; fijar por SHA sería más estricto. |
| ci.yml:17, 22, 39 | `uses:` sin comillas | Parece un problema por la restricción «entre comillas», pero no lo es: YAML lee `actions/checkout@v4.2.2` como texto. Las comillas sí importan en `python-version: "3.12"`, y ahí están. |
| ci.yml:18-19 | Credenciales | `persist-credentials: false`: el token no queda guardado en el checkout. |
| ci.yml:26-27 | Dependencias | Instala `requirements-dev.txt` con versiones fijadas; se agregó `pytest-cov==7.1.0` (existe en PyPI y funciona con pytest 9.2.0). |
| ci.yml:29-36 | ¿Un fallo detiene el pipeline? | No hay `continue-on-error` ni `|| true`. Ruff, pytest y pip-audit terminan con error si encuentran algo. Comprobado con una prueba rota a propósito (sección 4). |
| ci.yml:38-43 | Artefacto | Sube `coverage.xml` solo si todo pasó; si una prueba falla, el reporte de la consola sigue en el log. |

## 3. Lo que encontraron las herramientas

| Herramienta | Avisos | ¿Coinciden con mis hallazgos? | ¿Qué no encontró? |
|---|---|---|---|
| actionlint | 0 | Sí: no hay errores de sintaxis ni de tipos. | No revisa si las etiquetas existen ni si una versión puede moverse; eso lo revisé con `gh api`. |
| hadolint | pendiente (Dockerfile) | | |

## 4. Verificación

- [x] El pipeline se ejecutó en GitHub y salió en verde: [ejecución 45875920902](https://github.com/kenneth0710/asistente-pruebas-pytest/actions/runs/45875920902). Resultado: 100 aprobadas, cobertura del 95 % (líneas y ramas), «No known vulnerabilities found».
- [x] Hice fallar una prueba a propósito y el pipeline salió en rojo: [ejecución 45876043174](https://github.com/kenneth0710/asistente-pruebas-pytest/actions/runs/45876043174). Resultado: «1 failed, 99 passed», en la rama `demo-pipeline-rojo`, que borré después.
- [ ] La imagen se construye (pendiente: Dockerfile).
- [x] No hay claves en `ci.yml` ni en el historial de Git: el `.env` está en `.gitignore` desde la semana 5.
