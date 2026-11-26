Revisé tus secciones y encontré cinco problemas. Corrígelos:

1. Enlaces rotos: escribiste https://tests/test_aceptacion_hu07.py, https://docs/revision_configuracion.md y https://docs/plan_operacion.md, todos con ?utm_source=chatgpt.com. En un README de GitHub los enlaces a archivos del repositorio son rutas relativas, por ejemplo [tests/test_aceptacion_hu07.py](tests/test_aceptacion_hu07.py). El de GitHub Actions va sin ?utm_source.
2. Uso de IA: borraste lo que ya estaba. ChatGPT también se usó en las semanas 5, 6 y 7. Conserva esos tres párrafos tal como están en el README actual (te los pego abajo) y agrega lo nuevo.
3. Pruebas: quitaste los comandos pytest -v, ruff check . y pip-audit -r requirements-dev.txt, la lista de archivos de prueba y el enlace a registro_pruebas.md. Consérvalos (la sección actual va abajo) y agrega la cobertura y el archivo de aceptación.
4. Estructura: el árbol está incompleto. Estos son todos los archivos del repositorio (sin contar los 24 prompts de docs/prompts/):
.asistenteignore
.dockerignore
.env.example
.github/workflows/ci.yml
.gitignore
Dockerfile
LICENSE
README.md
asistente/__init__.py
asistente/exclusion.py
bitacora_ia.md
docs/modulos/README.md
docs/modulos/modulo1_banco_de_prompts.pdf
docs/modulos/modulo1_propuesta.pdf
docs/modulos/modulo2_requisitos_y_bitacora.pdf
docs/modulos/modulo3_diseno.pdf
docs/plan_operacion.md
docs/revision_configuracion.md
pyproject.toml
registro_pruebas.md
requirements-dev.txt
revision_seguridad.md
tests/test_aceptacion_hu07.py
tests/test_hu07_abuso.py
tests/test_hu07_exclusion.py
tests/test_s7_datos_sinteticos.py
tests/test_s7_esta_excluido.py
tests/test_s7_normalizar_para_comparar.py
tests/test_s7_seleccionar_archivos.py
5. No pongas negrita dentro de los títulos (## **Requisitos**): deja ## Requisitos.

Sección Pruebas actual:
## Pruebas
Para ejecutar las pruebas automatizadas:

```
pytest
```

Para ver cada caso por su nombre (por ejemplo `test_filtrar_rutas[S29]`):

```
pytest -v
```

Actualmente hay 100 pruebas distribuidas en los siguientes archivos:

- `tests/test_hu07_exclusion.py`: pruebas de la HU-07 (semana 5).
- `tests/test_hu07_abuso.py`: pruebas de abuso del filtro (semana 6).
- `tests/test_s7_seleccionar_archivos.py`, `tests/test_s7_normalizar_para_comparar.py` y `tests/test_s7_esta_excluido.py`: casos diseñados con particiones de equivalencia, valores límite y tabla de decisión (semana 7).
- `tests/test_s7_datos_sinteticos.py`: fixture `repo_panaderia` con datos sintéticos (semana 7).

La tabla de casos, las pruebas de la IA descartadas o corregidas, los errores introducidos a propósito y el origen de los datos de prueba están en [`registro_pruebas.md`](registro_pruebas.md).

Para ejecutar el análisis estático con Ruff:

```
ruff check .
```

La configuración de Ruff utiliza las reglas E, F, B y S, definidas en `pyproject.toml`.

Para auditar las dependencias de desarrollo:

```
pip-audit -r requirements-dev.txt
```

Sección Uso de IA actual:
## Uso de IA
La IA se utilizó como apoyo durante las semanas 5, 6 y 7 del desarrollo.

**Semana 5:** ChatGPT propuso las pruebas, la implementación y el refactor de la funcionalidad HU-07.

**Semana 6:** ChatGPT realizó una segunda revisión de seguridad, trabajó como agente en la rama `agente/pruebas-abuso` para desarrollar pruebas de abuso y su corrección, y redactó los docstrings y este README.

**Semana 7:** ChatGPT propuso los casos de prueba con particiones de equivalencia, valores límite y tabla de decisión, escribió las pruebas a partir de la tabla revisada, corrigió el defecto D-01 que esas pruebas encontraron y generó los datos sintéticos. Cada caso y cada prueba se revisaron contra la regla; el detalle está en `registro_pruebas.md`.

Las sugerencias realizadas por la IA se verificaron mediante pruebas antes de integrarse. El detalle del proceso se encuentra en `bitacora_ia.md` y el informe de seguridad en `revision_seguridad.md`.

Tarea: entrega de nuevo las cinco secciones (Requisitos, Pruebas, Integración continua y Docker, Estructura y Uso de IA) corregidas, dentro de un solo bloque de código Markdown para poder copiarlas sin perder el formato. No cambies nada más.
