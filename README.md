# Asistente de pruebas pytest

Asistente de IA que propone pruebas automáticas (pytest) a partir de los criterios de aceptación del módulo de pedidos de una app para una panadería de barrio.

Proyecto final del Seminario de Inteligencia Artificial Aplicada al Ciclo de Vida del Software (FET).
Estudiante: Kenneth Ramírez Burgos.

Este repositorio sigue el diseño de la semana 4 (ADR-001): una CLI en Python, un plugin de pytest para la marca `criterio` y un flujo de GitHub Actions. La lista de exclusión vive en el archivo `.asistenteignore`.

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

Una lista nueva con las rutas que se pueden enviar a la IA, en el mismo orden en que llegaron y escritas con `/`. Si `archivo_pedido` está permitido y no estaba en `rutas`, se agrega al final.

**Error**

Si `archivo_pedido` coincide con algún patrón, lanza `ArchivoExcluidoError` con la ruta en el mensaje y no devuelve ninguna lista: no se envía nada. La CLI lo traduce al código de salida 7 («el archivo pedido está excluido y no se envió», interfaz de la semana 4).

**Regla de coincidencia**

Una ruta queda excluida si un patrón coincide con la ruta completa o con el nombre del archivo (sin carpetas). Así, `.env` excluye también `config/.env`. La comparación distingue mayúsculas y minúsculas y se hace igual en los tres sistemas operativos.

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

**Ejemplos (entrada → salida)**

| # | `rutas` | `patrones` | `archivo_pedido` | Resultado |
|---|---|---|---|---|
| 1 | `["app/pedidos/validaciones.py", ".env", "datos/clientes_panaderia.csv", "pedidos.db"]` | `[".env", "clientes_panaderia.csv", "pedidos.db"]` | `None` | `["app/pedidos/validaciones.py"]` |
| 2 | `["app\\pedidos\\validaciones.py", "config\\.env"]` | `[".env"]` | `None` | `["app/pedidos/validaciones.py"]` |
| 3 | `[]` | `[".env"]` | `None` | `[]` |
| 4 | `["app/pedidos/validaciones.py"]` | `[".env"]` | `"tests/pedidos/test_hu03.py"` | `["app/pedidos/validaciones.py", "tests/pedidos/test_hu03.py"]` |
| 5 | `["app/pedidos/validaciones.py"]` | `[".env"]` | `".env"` | `ArchivoExcluidoError` |

### Cómo ejecutar las pruebas

Requisitos: Python 3.11 o superior y pytest.

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate    macOS/Ubuntu: source .venv/bin/activate
pip install pytest
pytest
```

`pytest` corre todas las pruebas de `tests/` con un solo comando. La configuración está en `pyproject.toml`.

### Bitácora de uso de IA

Las sugerencias del asistente, con la decisión y la verificación de cada una, están en [`bitacora_ia.md`](bitacora_ia.md).
