# Informe de revisión de código y seguridad

Proyecto: Asistente de IA que propone pruebas pytest a partir de los criterios de aceptación del módulo de pedidos (app de panadería de barrio)
Estudiante: Kenneth Ramírez Burgos
Fecha: 2026-11-14
Commit revisado: `61a2af1` (entrega de la semana 5, antes de las correcciones)

## 1. Herramientas y criterios

- **Linter:** ruff 0.17.5 con las reglas E, F, B y S. La configuración está en `pyproject.toml`. Antes de corregir había 16 avisos: 1 E501 y 15 S101 en las pruebas. Ahora queda 0.
- **Auditoría de dependencias:** pip-audit 2.10.1 sobre `requirements-dev.txt`. Resultado: «No known vulnerabilities found».
- **Lista de revisión:** la de la semana 6, que revisa tres cosas:
  - Corrección y pruebas: si cumple la historia y sus límites, si las pruebas cubren casos de error y de límite, y si el linter queda sin avisos o con avisos justificados.
  - Diseño y legibilidad: si respeta el ADR, si los nombres son claros sin valores mágicos, y si las funciones son cortas y sin duplicación.
  - Seguridad: si las consultas usan parámetros, si hay claves en el código o en Git, y si se verifican los permisos.
- **Revisión con IA:** ChatGPT (versión web) en un chat nuevo, para que no revisara con indulgencia el código que generó en la semana 5. Usé el prompt de revisión de la clase (sección 3).

### Puntos de seguridad revisados

| Punto | ¿Aplica? | Resultado |
|---|---|---|
| Inyección (consultas con parámetros) | No, porque el asistente no tiene base de datos ni ejecuta comandos (`subprocess`, `eval`). | Sin hallazgos. Las reglas S de ruff no dan avisos. |
| Secretos (código, historial, .gitignore, .env.example) | Sí. | Revisé `git log -p` en todas las ramas y no hay claves. Nunca se subió un `.env`, `.db` ni `.csv`. `.env` está en `.gitignore`. Faltaba `.env.example`; ver H-04. |
| Contraseñas (scrypt, bcrypt o argon2 con sal) | No, porque el asistente no tiene usuarios ni guarda contraseñas. | No aplica. |
| Control de acceso (rol verificado y prueba de abuso) | Sí. En este proyecto el control de acceso es el filtro de exclusión: decide qué archivos pueden salir hacia la IA (RNF-06). | Había dos evasiones reales (H-01 y H-02). Se corrigieron con 10 pruebas de abuso en `tests/test_hu07_abuso.py`. |
| Dependencias (existen, necesarias, versión fijada, pip-audit) | Sí. | El código solo usa la librería estándar. Las herramientas (pytest, ruff, pip-audit) existen en PyPI, son necesarias y ahora tienen versión fijada (H-05). pip-audit no reporta vulnerabilidades. |

## 2. Tabla de hallazgos

| Id | Archivo y línea | Problema | Categoría (OWASP o tipo) | Severidad | Corrección | Commit |
|---|---|---|---|---|---|---|
| H-01 | asistente/exclusion.py:16 y :26 (versión `61a2af1`) | Con un patrón que lleva carpeta (`datos/clientes_panaderia.csv`), las rutas equivalentes no coincidían, y los datos de unos 300 clientes podían salir hacia la IA. Las rutas eran `./datos/…`, `x/../datos/…`, `datos//…`, `C:/repo/datos/…` y `/home/ana/repo/datos/…`. | A01:2021 Pérdida de control de acceso | Alta | Se normaliza la ruta solo para comparar (quita `.`, resuelve `..` y `//`) y el patrón se compara contra cada sufijo de la ruta. Hay 5 pruebas de abuso. | `9780a9c` (pruebas), `daeb3bb` (corrección) |
| H-02 | asistente/exclusion.py:25–26 (versión `61a2af1`) | Windows abre `.env ` (espacio final), `.env.` (punto final) y `.env::$DATA` (flujo NTFS) como el mismo `.env`, pero el filtro no los reconocía. Así, la clave de Gemini podía salir. | A01:2021 Pérdida de control de acceso (equivalencia de nombres, CWE-41) | Alta | Al comparar se quitan los espacios y puntos finales y el sufijo de flujo `:…`. Hay 3 pruebas de abuso y 1 de error (`archivo_pedido=".env "` lanza `ArchivoExcluidoError`). | `9780a9c`, `daeb3bb` |
| H-03 | asistente/exclusion.py:40 | Línea de 96 caracteres (aviso E501). | Estilo | Baja | Se dividió la línea en la corrección del agente. | `daeb3bb` |
| H-04 | raíz del repositorio | No existía `.env.example`, así que no quedaba claro qué variable de entorno usa el asistente. | A05:2021 Configuración de seguridad incorrecta (secretos) | Baja | Se agregó `.env.example` con `GEMINI_API_KEY=` vacía. | `3072702` |
| H-05 | raíz del repositorio | Las herramientas no tenían versión fijada: pytest se instalaba sin versión. | A06:2021 Componentes vulnerables y desactualizados | Baja | Se creó `requirements-dev.txt` con versiones fijadas y se revisó con pip-audit. | `3072702` |
| H-06 | asistente/exclusion.py (todas las funciones) | Las docstrings no decían qué reciben, qué devuelven ni qué errores lanzan. | Mantenibilidad | Baja | Se agregaron docstrings con Args, Returns y Raises, verificadas contra el código. | `4206999` |

**Severidad:**
- Alta: permite acceder a datos o cambiarlos sin permiso, o expone secretos.
- Media: error probable, o riesgo que depende de ciertas condiciones.
- Baja: estilo o mantenibilidad.

### Avisos del linter no corregidos

| Regla | Archivo y línea | Por qué se mantiene |
|---|---|---|
| S101 | `tests/*` (todas las líneas con `assert`) | `assert` es la forma normal de comprobar en pytest. Está desactivado solo para `tests/` en `pyproject.toml`; en el código del asistente sigue activo. |

## 3. Revisión con IA

**Prompt usado:** el prompt de la clase, adaptado a mi proyecto. Lo pegué completo en [`docs/prompts/prompt4_revision_seguridad.txt`](docs/prompts/prompt4_revision_seguridad.txt) y está registrado en la entrada 7 de la bitácora.
- **Rol:** revisor de Python con experiencia en seguridad.
- **Contexto:** HU-07, RNF-04, RNF-06, ADR-001 y el contrato, más el código con números de línea.
- **Tarea:** revisar corrección, legibilidad, inyección, secretos, contraseñas, control de acceso y dependencias.
- **Formato:** tabla de línea, problema, severidad y corrección.
- **Restricciones:** no reescribir todo, y separar los problemas seguros de las sospechas.

| Hallazgo de la IA | ¿Real o falso positivo? | Cómo lo verifiqué |
|---|---|---|
| Líneas 16 y 26: no resuelve `..` (ejemplo `config/../.env`) | **Real en parte.** Su ejemplo es un falso positivo, pero el problema existe con patrones que llevan carpeta (H-01), y eso la IA no lo mostró. | Ejecuté `seleccionar_archivos(["config/../.env"], [".env"])` y devolvió `[]`: ya se excluía por el nombre del archivo. Con `x/../datos/clientes_panaderia.csv` y el patrón `datos/clientes_panaderia.csv`, el archivo sí pasaba. |
| Línea 58: los patrones no se normalizan igual que las rutas | **Real en parte.** Quedó cubierto en H-01: ahora los patrones también pasan por `_normalizar_para_comparar`. | Lo comparé contra el código: los patrones solo pasaban por `replace` y `lower`. |
| Línea 41: `fnmatchcase` no garantiza proteger rutas equivalentes | **Falso positivo, o no accionable.** No señala ninguna entrada concreta que falle. | Lo revisé contra el código. `fnmatchcase` es correcto y evita las reglas de mayúsculas de Windows. |
| Líneas 60–61: el filtrado depende de la normalización | **No es un hallazgo distinto:** repite el primero. | — |
| Líneas 64–65: el archivo pedido podría saltarse las reglas | **Falso positivo.** | El archivo pedido pasa por el mismo `_esta_excluido` antes de agregarse, y hay pruebas HU-07-E2 que lo comprueban. |
| Sospechas: otro módulo que envíe a Gemini sin filtro; la clave en registros; enlaces simbólicos | **No aplican hoy**, porque el módulo que lee el disco y llama a la API todavía no existe. Quedan como pendientes P-02 y P-03. | Revisé el repositorio: solo existen `asistente/exclusion.py` y las pruebas. |
| 7 pruebas recomendadas (`config/../.env`, `C:\proyecto\.env`, `/home/…/.env`, `.ENV`, `respaldo.db`, etc.) | **No aportan detección nueva:** las 7 ya pasaban con el código revisado. | Las ejecuté una por una contra la versión `61a2af1`. |

**Lo que la IA no encontró:**
- **H-02 completo:** las variantes de Windows (`.env `, `.env.` y `.env::$DATA`), que son la evasión más grave porque exponen la clave.
- **Los casos concretos de H-01:** `./datos/…` y las rutas absolutas con patrón de carpeta.
- **El aviso E501 del linter.**

También noté que la IA marcó como «seguros» problemas cuyos ejemplos ya funcionaban. Ese es el límite de «falsos positivos» que se vio en clase.

## 4. Pendientes

| Pendiente | Por qué no se corrigió todavía | Plan |
|---|---|---|
| P-01. Patrones de carpeta estilo `.gitignore` (`datos/` para excluir todo lo que hay dentro) | El contrato de la semana 5 no los incluye, y cambiarlos cambia el comportamiento. | Agregar el soporte con su contrato y sus pruebas al construir la CLI. Mientras tanto, se escribe el patrón completo (`datos/*`). |
| P-02. Garantizar que todo envío a Gemini pase por `seleccionar_archivos` y que la clave no aparezca en registros ni errores | El módulo de envío (CLI) todavía no existe. | Agregar una prueba de integración que falle si se llama a la API con una ruta excluida. |
| P-03. Enlaces simbólicos que apunten a archivos excluidos | La función no lee el disco; el riesgo aparece cuando la CLI lea archivos. | Resolver el destino real con `Path.resolve()` en la CLI antes de filtrar. |
| P-04. Comprobar si el archivo pedido ya está en la lista sin distinguir mayúsculas | Hallazgo menor de la semana 5. No deja salir archivos excluidos: solo podría repetir una ruta permitida. | Revisarlo junto con P-01. |

Una decisión tomada en la corrección: ahora el patrón `datos/clientes_panaderia.csv` también excluye `otra/datos/clientes_panaderia.csv`, porque compara contra cada sufijo de la ruta. Es más estricto que antes, y en este filtro es preferible excluir de más (RNF-06).

**Claves expuestas:** ninguna. El historial de Git se revisó en todas las ramas y nunca se subió un `.env` ni una clave.
