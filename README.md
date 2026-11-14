# Asistente de pruebas pytest

## Qué es

Asistente de IA que ayuda a un equipo de cinco estudiantes a proponer pruebas pytest a partir de los criterios de aceptación del módulo de pedidos de una aplicación para una panadería de barrio, evitando que archivos con información sensible se envíen al servicio de IA.

En esta versión está implementada la funcionalidad HU-07: el filtro de la lista de exclusión (`.asistenteignore`), que impide enviar los archivos `.env`, `clientes_panaderia.csv` y `pedidos.db`.

La funcionalidad se encuentra en `asistente/exclusion.py` y cuenta con la función `seleccionar_archivos(rutas, patrones, archivo_pedido=None)` y la excepción `ArchivoExcluidoError`.

La CLI completa definida en el ADR-001 (CLI en Python, plugin de pytest y GitHub Actions) todavía no está construida.

## Requisitos

- Python 3.11 o superior.
- El código utiliza únicamente la librería estándar de Python.
- Las herramientas de desarrollo tienen sus versiones fijadas en `requirements-dev.txt`:
  - `pytest==9.2.0`
  - `ruff==0.17.5`
  - `pip-audit==2.10.1`

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

Actualmente hay 24 pruebas distribuidas en los siguientes archivos:

- `tests/test_hu07_exclusion.py`
- `tests/test_hu07_abuso.py`

Para ejecutar el análisis estático con Ruff:

```
ruff check .
```

La configuración de Ruff utiliza las reglas E, F, B y S, definidas en `pyproject.toml`.

Para auditar las dependencias de desarrollo:

```
pip-audit -r requirements-dev.txt
```

## Estructura
```
asistente-pruebas-pytest/
├── asistente/
│   ├── __init__.py
│   └── exclusion.py
├── tests/
│   ├── test_hu07_exclusion.py
│   └── test_hu07_abuso.py
├── docs/
│   └── prompts/
├── .asistenteignore
├── .env.example
├── pyproject.toml
├── requirements-dev.txt
├── bitacora_ia.md
├── revision_seguridad.md
├── LICENSE
└── README.md
```

Descripción de los elementos principales:

- `asistente/`: contiene el código del proyecto.
- `tests/`: contiene las pruebas automatizadas con pytest.
- `docs/prompts/`: almacena los prompts exactos enviados a la IA.
- `.asistenteignore`: contiene una lista de exclusión de ejemplo.
- `.env.example`: sirve como plantilla para configurar las variables de entorno.
- `pyproject.toml`: contiene la configuración de pytest y Ruff.
- `requirements-dev.txt`: fija las versiones de las herramientas de desarrollo.
- `bitacora_ia.md`: registra el uso de IA durante el desarrollo.
- `revision_seguridad.md`: contiene el informe de revisión de seguridad.
- `LICENSE`: contiene los términos de la licencia MIT.

## Uso de IA
La IA se utilizó como apoyo durante las semanas 5 y 6 del desarrollo.

**Semana 5:** ChatGPT propuso las pruebas, la implementación y el refactor de la funcionalidad HU-07.

**Semana 6:** ChatGPT realizó una segunda revisión de seguridad, trabajó como agente en la rama `agente/pruebas-abuso` para desarrollar pruebas de abuso y su corrección, y redactó los docstrings y este README.

Las sugerencias realizadas por la IA se verificaron mediante pruebas antes de integrarse. El detalle del proceso se encuentra en `bitacora_ia.md` y el informe de seguridad en `revision_seguridad.md`.

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
