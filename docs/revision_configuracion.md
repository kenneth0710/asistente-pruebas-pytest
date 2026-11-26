# Revisión del pipeline y del Dockerfile

Proyecto: asistente-pruebas-pytest
Fecha: 2026-11-26

Plantilla de la práctica de la semana 9. Los dos archivos los generó ChatGPT con las restricciones de seguridad del curso, y yo los revisé línea por línea antes de aceptarlos.

## 1. Cómo se generaron

**Herramienta de IA:** ChatGPT (versión web)
**Prompt del pipeline:** [`prompt16_pipeline.txt`](prompts/prompt16_pipeline.txt) (entrada 19 de la [bitácora](../bitacora_ia.md))
**Prompt del Dockerfile:** [`prompt20_docker.txt`](prompts/prompt20_docker.txt), corregido con [`prompt21_etiqueta_imagen.txt`](prompts/prompt21_etiqueta_imagen.txt) (entrada 22 de la [bitácora](../bitacora_ia.md))

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
| ci.yml:29-36 | ¿Un fallo detiene el pipeline? | No hay `continue-on-error` ni `\|\| true`. Ruff, pytest y pip-audit terminan con error si encuentran algo. Comprobado con una prueba rota a propósito (sección 4). |
| ci.yml:38-43 | Artefacto | Sube `coverage.xml` solo si todo pasó; si una prueba falla, el reporte de la consola sigue en el log. |

### Dockerfile, .dockerignore y trabajo `docker`

Revisé los tres archivos con las seis preguntas de la semana: imagen base, secretos, usuario, `.dockerignore`, versiones y modo desarrollo.

| Archivo y línea | Revisión | Resultado |
|---|---|---|
| Dockerfile:1 | Imagen base | `python:3.12.12-slim-bookworm`: liviana y con versión exacta. La API de Docker Hub confirma que la etiqueta existe y está activa. **Riesgo residual:** una etiqueta fija de parche no recibe los arreglos de seguridad nuevos, y fijarla por digest sería más estricto. Queda en el plan de operación (sección 4). |
| Dockerfile:3-4 | Variables de entorno | Solo `PYTHONDONTWRITEBYTECODE` y `PYTHONUNBUFFERED`. No hay ninguna clave. |
| Dockerfile:8-10 | Dependencias | Instala `requirements-dev.txt`, con versiones fijadas, y `--no-cache-dir`. La imagen trae ruff y pip-audit, que no hacen falta para correr las pruebas. Se acepta porque es el mismo entorno del pipeline; solo hace la imagen más pesada. |
| Dockerfile:12-13, 21 | Usuario | Crea `appuser` (uid 10001) y termina con `USER 10001:10001`: el contenedor no corre como root. |
| Dockerfile:15-17 | Qué se copia | Solo `pyproject.toml`, `asistente/` y `tests/`. Aunque el `.dockerignore` fallara, el `.env` no entraría en la imagen. Comprobé que ninguna prueba lee archivos fuera de esas carpetas: todas usan `tmp_path`. |
| Dockerfile:23 | Modo desarrollo | No hay `--reload` ni puertos abiertos. `CMD` ejecuta pytest con cobertura y, si una prueba falla, devuelve un código de error. |
| .dockerignore | Archivos fuera | `.env` (también en subcarpetas), `.git`, `.venv`, cachés, `__pycache__` y reportes de cobertura. |
| ci.yml:45-60 | Trabajo `docker` | `needs: ci`, el mismo checkout sin credenciales y solo comandos `docker`, sin acciones de terceros ni secretos. `docker run` devuelve el código de salida de pytest, así que una prueba fallida pone el trabajo en rojo. |
| ci.yml:57, 60 | **Problema encontrado:** etiqueta `asistente-pruebas:1.0.0` | La etiqueta no salía de ningún dato del proyecto: `pyproject.toml` dice `0.1.0`. Se la señalé a ChatGPT (prompt 21) y la cambió a `0.1.0`. |
| ci.yml | Cambio no pedido | En el trabajo `ci`, ChatGPT puso comillas en `uses:` y `runs-on:`. No cambia el comportamiento (ver la fila «`uses:` sin comillas») y se acepta. |

## 3. Lo que encontraron las herramientas

| Herramienta | Avisos | ¿Coinciden con mis hallazgos? | ¿Qué no encontró? |
|---|---|---|---|
| actionlint | 0 | Sí: no hay errores de sintaxis ni de tipos. | No revisa si las etiquetas existen ni si una versión puede moverse; eso lo revisé con `gh api`. |
| hadolint | 0 | Sí: la imagen base está fijada, `pip` usa `--no-cache-dir` y la última instrucción `USER` no es root. | No sabe si la etiqueta existe en Docker Hub (lo revisé con su API), ni si la etiqueta de la imagen coincide con la versión del proyecto (`1.0.0` contra `0.1.0`), ni si las pruebas necesitan archivos que no se copian. |

## 4. Verificación

- [x] El pipeline se ejecutó en GitHub y salió en verde: [ejecución 45875920902](https://github.com/kenneth0710/asistente-pruebas-pytest/actions/runs/45875920902). Resultado: 100 aprobadas, cobertura del 95 % (líneas y ramas), «No known vulnerabilities found».
- [x] Hice fallar una prueba a propósito y el pipeline salió en rojo: [ejecución 45876043174](https://github.com/kenneth0710/asistente-pruebas-pytest/actions/runs/45876043174). Resultado: «1 failed, 99 passed», en la rama `demo-pipeline-rojo`, que borré después.
- [x] La imagen se construye y las pruebas pasan dentro del contenedor. No tengo Docker en mi equipo, así que se comprueba en el trabajo `docker` del pipeline: [ejecución 45879288064](https://github.com/kenneth0710/asistente-pruebas-pytest/actions/runs/45879288064), que nombra la imagen `asistente-pruebas:0.1.0` y da «102 passed». Ese trabajo solo corre si pasa el trabajo `ci` (`needs: ci`).
- [x] No hay claves en `ci.yml`, en el `Dockerfile` ni en el historial de Git: el `.env` está en `.gitignore` desde la semana 5, el `.dockerignore` lo deja fuera y el `Dockerfile` copia solo `pyproject.toml`, `asistente/` y `tests/`.
