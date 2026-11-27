# Asistente de pruebas pytest

## Qué es

Asistente de IA que ayuda a un equipo de cinco estudiantes a proponer pruebas pytest a partir de los criterios de aceptación del módulo de pedidos de una aplicación para una panadería de barrio, evitando que archivos con información sensible se envíen al servicio de IA.

En esta versión está implementada la funcionalidad HU-07: el filtro de la lista de exclusión (`.asistenteignore`), que impide enviar los archivos `.env`, `clientes_panaderia.csv` y `pedidos.db`.

La funcionalidad se encuentra en `asistente/exclusion.py` y cuenta con la función `seleccionar_archivos(rutas, patrones, archivo_pedido=None)` y la excepción `ArchivoExcluidoError`.

La CLI completa definida en el ADR-001 (CLI en Python, plugin de pytest y GitHub Actions) todavía no está construida.

## Requisitos

- Python 3.11 o superior.
- Dependencias de desarrollo definidas en `requirements-dev.txt`:

| Herramienta | Versión | Propósito |
|---|---|---|
| pytest | 9.2.0 | Ejecución de pruebas automatizadas. |
| ruff | 0.17.5 | Análisis estático de código. |
| pip-audit | 2.10.1 | Auditoría de vulnerabilidades en dependencias. |
| pytest-cov | 7.1.0 | Medición de cobertura de código. |

El código del asistente utiliza únicamente la librería estándar de Python. Docker es opcional y permite ejecutar las pruebas en un entorno contenerizado.

## Instalación

Clona el repositorio:

```bash
git clone https://github.com/kenneth0710/asistente-pruebas-pytest.git
cd asistente-pruebas-pytest
```

Crea un entorno virtual:

```
python -m venv .venv
```

Activa el entorno virtual según tu sistema operativo.

**Windows:**

```
.venv\Scripts\activate
```

**macOS y Ubuntu:**

```
source .venv/bin/activate
```

Instala las herramientas de desarrollo:

```
pip install -r requirements-dev.txt
```

Copia `.env.example` como `.env`. La variable `GEMINI_API_KEY` se utilizará cuando exista la CLI. El archivo `.env` nunca debe subirse al repositorio.

## Ejecución
Como la CLI todavía no existe, la función se utiliza directamente desde Python.

Ejemplo:

```
python -c "from asistente.exclusion import seleccionar_archivos; print(seleccionar_archivos(['app/pedidos/validaciones.py', '.env'], ['.env']))"
```

Resultado esperado:

```
['app/pedidos/validaciones.py']
```

En este ejemplo, el filtro excluye `.env` y devuelve únicamente la ruta permitida.

## Pruebas

Para ejecutar las pruebas automatizadas:

```
pytest
```

Para ver cada caso por su nombre (por ejemplo `test_filtrar_rutas[S29]`):

```
pytest -v
```

Actualmente hay 102 pruebas distribuidas en los siguientes archivos:

- `tests/test_hu07_exclusion.py`: pruebas de la HU-07 (semana 5).
- `tests/test_hu07_abuso.py`: pruebas de abuso del filtro (semana 6).
- `tests/test_s7_seleccionar_archivos.py`, `tests/test_s7_normalizar_para_comparar.py` y `tests/test_s7_esta_excluido.py`: casos diseñados con particiones de equivalencia, valores límite y tabla de decisión (semana 7).
- `tests/test_s7_datos_sinteticos.py`: fixture `repo_panaderia` con datos sintéticos (semana 7).
- [`tests/test_aceptacion_hu07.py`](tests/test_aceptacion_hu07.py): dos pruebas de aceptación de HU-07, una por cada escenario del documento de requisitos, organizadas mediante la estructura Dado, Cuando y Entonces (cierre del proyecto).

La tabla de casos, las pruebas de la IA descartadas o corregidas, los errores introducidos a propósito y el origen de los datos de prueba están en [`registro_pruebas.md`](registro_pruebas.md).

Para ejecutar las pruebas y medir la cobertura de líneas y ramas:

```
pytest --cov=asistente --cov-branch --cov-report=term-missing
```

Resultados obtenidos:

| Indicador | Resultado |
|---|---:|
| Pruebas aprobadas | 102 |
| Cobertura de líneas | 96 % |
| Cobertura de ramas | 92,86 % |

Las líneas 58 y 106 de `asistente/exclusion.py` no están cubiertas. El análisis y la justificación de estos casos se encuentran en la sección 5 de [`registro_pruebas.md`](registro_pruebas.md).

Para ejecutar el análisis estático con Ruff:

```
ruff check .
```

La configuración de Ruff utiliza las reglas E, F, B y S, definidas en `pyproject.toml`.

Para auditar las dependencias de desarrollo:

```
pip-audit -r requirements-dev.txt
```

## Integración continua y Docker

El proyecto cuenta con un pipeline de integración continua mediante GitHub Actions, configurado en [`.github/workflows/ci.yml`](.github/workflows/ci.yml), que se ejecuta en cada push y pull request.

El pipeline se divide en dos trabajos:

| Trabajo | Descripción |
|---|---|
| `ci` | Ejecuta Ruff, pytest con cobertura y pip-audit. Almacena el informe `coverage.xml` como artefacto. |
| `docker` | Construye la imagen Docker y ejecuta las pruebas dentro del contenedor. Solo se ejecuta si el trabajo `ci` finaliza correctamente. |

Las ejecuciones del pipeline pueden consultarse en [GitHub Actions](https://github.com/kenneth0710/asistente-pruebas-pytest/actions).

El [`Dockerfile`](Dockerfile) y el [`.dockerignore`](.dockerignore) permiten construir un entorno reproducible de pruebas. El contenedor ejecuta las pruebas con un usuario sin privilegios.

Para construir la imagen:

```
docker build -t asistente-pruebas:0.1.0 .
```

Para ejecutar las pruebas dentro del contenedor:

```
docker run --rm asistente-pruebas:0.1.0
```

La imagen está destinada a la ejecución de pruebas, no al despliegue de un servicio.

Documentación relacionada:

- [Revisión de la configuración del pipeline y Dockerfile](docs/revision_configuracion.md).
- [Plan de operación, monitoreo y mantenimiento](docs/plan_operacion.md).

## Estructura

```
asistente-pruebas-pytest/
├── .github/
│   └── workflows/
│       └── ci.yml
├── asistente/
│   ├── __init__.py
│   └── exclusion.py
├── docs/
│   ├── modulos/
│   │   ├── README.md
│   │   ├── modulo1_banco_de_prompts.pdf
│   │   ├── modulo1_propuesta.pdf
│   │   ├── modulo2_requisitos_y_bitacora.pdf
│   │   └── modulo3_diseno.pdf
│   ├── prompts/
│   ├── informe_final.pdf
│   ├── plan_operacion.md
│   ├── revision_configuracion.md
│   └── sustentacion.pdf
├── tests/
│   ├── test_aceptacion_hu07.py
│   ├── test_hu07_abuso.py
│   ├── test_hu07_exclusion.py
│   ├── test_s7_datos_sinteticos.py
│   ├── test_s7_esta_excluido.py
│   ├── test_s7_normalizar_para_comparar.py
│   └── test_s7_seleccionar_archivos.py
├── .asistenteignore
├── .dockerignore
├── .env.example
├── .gitignore
├── bitacora_ia.md
├── Dockerfile
├── informe_final.md
├── LICENSE
├── pyproject.toml
├── README.md
├── registro_pruebas.md
├── requirements-dev.txt
└── revision_seguridad.md
```

La carpeta [`docs/modulos/`](docs/modulos/) contiene los documentos PDF de la propuesta del proyecto, el banco de prompts, los requisitos y el diseño. Su archivo [`README.md`](docs/modulos/README.md) funciona como índice de estos documentos.

La carpeta `docs/prompts/` contiene los prompts utilizados durante el proyecto, cuyos archivos individuales se omiten del árbol para facilitar su lectura.

## Uso de IA

La IA se utilizó como apoyo durante los diferentes módulos del proyecto, las semanas 5, 6 y 7 del desarrollo y el cierre del proyecto.

**Módulo 1:** Claude se utilizó como apoyo para elaborar el banco de prompts y redactar la propuesta del proyecto.

**Módulos 2 y 3:** Gemini se utilizó como apoyo para la definición de requisitos y el diseño del software.

**Semana 5:** ChatGPT propuso las pruebas, la implementación y el refactor de la funcionalidad HU-07.

**Semana 6:** ChatGPT realizó una segunda revisión de seguridad, trabajó como agente en la rama `agente/pruebas-abuso` para desarrollar pruebas de abuso y su corrección, y redactó los docstrings y este README.

**Semana 7:** ChatGPT propuso los casos de prueba con particiones de equivalencia, valores límite y tabla de decisión, escribió las pruebas a partir de la tabla revisada, corrigió el defecto D-01 que esas pruebas encontraron y generó los datos sintéticos. Cada caso y cada prueba se revisaron contra la regla; el detalle está en `registro_pruebas.md`.

**Cierre del proyecto (26 de noviembre):** ChatGPT propuso el plan de cierre, el pipeline de integración continua, el análisis de cobertura, las pruebas de aceptación, el Dockerfile y el plan de operación. Las propuestas fueron sometidas a revisión humana antes de su aceptación. El proceso está documentado en las entradas 18 a 26 de `bitacora_ia.md`.

Las sugerencias realizadas por la IA se verificaron mediante pruebas antes de integrarse. El detalle del proceso se encuentra en `bitacora_ia.md` y el informe de seguridad en `revision_seguridad.md`.

La [`bitácora de IA`](bitacora_ia.md) contiene 28 entradas, clasificadas de la siguiente manera:

| Resultado de la revisión | Cantidad |
|---|---:|
| Aceptadas | 11 |
| Aceptadas con cambios | 13 |
| Rechazadas | 4 |
| **Total** | **28** |

Los prompts utilizados se encuentran en [`docs/prompts/`](docs/prompts/). La bitácora permite consultar las decisiones tomadas durante la revisión de los resultados generados por la inteligencia artificial.

## Entrega final

- [Informe final](informe_final.md) (también en [PDF](docs/informe_final.pdf)).
- [Diapositivas de la sustentación](docs/sustentacion.pdf).

## Autor y licencia
**Autor:** Kenneth Ramírez Burgos.

**Institución:** Fundación Escuela Tecnológica de Neiva «Jesús Oviedo Pérez».

**Asignatura:** Seminario de IA aplicada al ciclo de vida del software.

**Año:** 2026.

**Licencia:** MIT. Consulta el archivo `LICENSE` para conocer sus términos.

---

## Funcionalidad de la semana 5

### Historia de usuario

**HU-07** (prioridad Must). Como líder del equipo, quiero que el asistente ignore los archivos de una lista de exclusión, para que las claves y los datos reales de clientes no salgan a una IA externa. Necesidad de origen: N-07.

Criterios de aceptación (documento de requisitos, semana 3):

- **HU-07-E1. Archivos excluidos.** Dado que la lista de exclusión contiene `.env`, `clientes_panaderia.csv` y `pedidos.db`, cuando el desarrollador pide pruebas para el módulo de pedidos, entonces ninguno de esos 3 archivos se incluye en lo que se envía al servicio de IA.
- **HU-07-E2 (error). Pedido explícito de un archivo excluido.** Dado que `.env` está en la lista de exclusión, cuando el desarrollador pide al asistente revisar `.env`, entonces el asistente no envía el archivo y avisa que está excluido.

Requisitos no funcionales relacionados: RNF-04 (funcionar sin cambios en Windows 11, macOS y Ubuntu, incluidas las rutas de archivos) y RNF-06 (0 archivos de la lista de exclusión enviados a la IA).

### Contrato

```python
def seleccionar_archivos(
    rutas: list[str],
    patrones: list[str],
    archivo_pedido: str | None = None,
) -> list[str]: ...

class ArchivoExcluidoError(Exception): ...
```

Ubicación: `asistente/exclusion.py`.

**Qué recibe**

- `rutas`: rutas relativas a la raíz del repositorio de los archivos que el asistente reunió como contexto para la historia. Pueden venir con `/` o con `\` (Windows).
- `patrones`: los patrones de `.asistenteignore`, ya sin comentarios ni líneas vacías. Son patrones tipo glob, por ejemplo `.env`, `*.db` o `datos/clientes_panaderia.csv`.
- `archivo_pedido`: la ruta que el desarrollador pidió revisar con `--archivo`, o `None` si no pidió ninguna.

**Qué devuelve**

Una lista nueva con las rutas que se pueden enviar a la IA, en el mismo orden en que llegaron y escritas con `/`. Si `archivo_pedido` está permitido y no estaba en `rutas`, se agrega al final. Para saber si «ya estaba», se compara después de pasar las dos rutas a `/` (`app\pedidos\validaciones.py` y `app/pedidos/validaciones.py` son la misma ruta y no se repite).

**Error**

Si `archivo_pedido` coincide con algún patrón, lanza `ArchivoExcluidoError` con la ruta en el mensaje y no devuelve ninguna lista: no se envía nada. La CLI lo traduce al código de salida 7 («el archivo pedido está excluido y no se envió», interfaz de la semana 4).

**Regla de coincidencia**

Una ruta queda excluida si un patrón coincide con la ruta completa o con el nombre del archivo (sin carpetas). Así, `.env` excluye también `config/.env`, y `*.db` excluye `datos/pedidos.db`. La comparación **no** distingue mayúsculas y minúsculas: `.ENV` también queda excluido, porque en Windows y macOS es el mismo archivo que `.env`. Se hace igual en los tres sistemas operativos (RNF-04), y ante la duda se excluye (RNF-06).

> Cambio del contrato (7/11/2026): la primera versión decía que la comparación distinguía mayúsculas. Al revisar las pruebas que propuso el asistente vi que eso dejaba salir `.ENV`, que en Windows es el mismo `.env`. Ver la entrada 2 de la bitácora.

**Supuestos**

- La función no lee el disco ni la red: solo trabaja con las listas que recibe.
- No modifica las listas que recibe.
- Los patrones de negación de `.gitignore` (`!patron`) no se soportan en esta versión.
- Las rutas repetidas se devuelven tal como llegaron; quitar duplicados no es parte de esta historia.

**Casos límite**

- `rutas` vacía: devuelve `[]`.
- `patrones` vacía: devuelve todas las rutas, en el mismo orden.
- Archivo excluido dentro de una subcarpeta (`config/.env`).
- Ruta con `\` de Windows (`datos\clientes_panaderia.csv`).
- Nombre parecido a uno excluido: `.env.ejemplo` no coincide con `.env` y sí se envía.
- Mismo nombre con otras mayúsculas: `.ENV` se excluye igual que `.env`.
- `archivo_pedido` que ya venía en `rutas` (con otra barra): no se agrega dos veces.

**Ejemplos (entrada → salida)**

| # | `rutas` | `patrones` | `archivo_pedido` | Resultado |
|---|---|---|---|---|
| 1 | `["app/pedidos/validaciones.py", ".env", "datos/clientes_panaderia.csv", "pedidos.db"]` | `[".env", "clientes_panaderia.csv", "pedidos.db"]` | `None` | `["app/pedidos/validaciones.py"]` |
| 2 | `["app\\pedidos\\validaciones.py", "config\\.env"]` | `[".env"]` | `None` | `["app/pedidos/validaciones.py"]` |
| 3 | `[]` | `[".env"]` | `None` | `[]` |
| 4 | `["app/pedidos/validaciones.py"]` | `[".env"]` | `"tests/pedidos/test_hu03.py"` | `["app/pedidos/validaciones.py", "tests/pedidos/test_hu03.py"]` |
| 5 | `["app/pedidos/validaciones.py"]` | `[".env"]` | `".env"` | `ArchivoExcluidoError` |
| 6 | `["app/pedidos/validaciones.py", "datos/pedidos.db"]` | `["*.db"]` | `None` | `["app/pedidos/validaciones.py"]` |
| 7 | `[".ENV", "app/pedidos/validaciones.py"]` | `[".env"]` | `None` | `["app/pedidos/validaciones.py"]` |

### Cómo ejecutar las pruebas

Requisitos: Python 3.11 o superior y pytest.

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate    macOS/Ubuntu: source .venv/bin/activate
pip install pytest
pytest
```

`pytest` corre todas las pruebas de `tests/` con un solo comando. La configuración está en `pyproject.toml`.
