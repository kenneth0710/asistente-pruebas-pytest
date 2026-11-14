# Bitácora de uso de IA

Proyecto: Asistente de IA que propone pruebas pytest a partir de los criterios de aceptación del módulo de pedidos de una app para panadería de barrio
Estudiante: Kenneth Ramírez Burgos
Funcionalidad: HU-07 Lista de exclusión de archivos (`seleccionar_archivos`)
Asistente usado:
- Semana 5: ChatGPT (OpenAI), versión web, modo chat, en una sola conversación el 7 de noviembre de 2026. Le di como contexto el contrato y las pruebas. El código lo pegué y lo ejecuté en VS Code con pytest.
- Semana 6: ChatGPT, versión web, en un chat nuevo el 14 de noviembre de 2026. Lo usé en modo chat para la revisión, las docstrings y el README, y como agente delimitado en la rama `agente/pruebas-abuso`. Sus entradas empiezan en la sección «Semana 6».

Los prompts exactos están en [`docs/prompts/`](docs/prompts/): uno para las pruebas, otro para la implementación y otro para el refactor. Siguen la estructura del curso (rol, contexto, tarea, formato y restricciones) y el prompt del OVA «Contrato y pruebas primero».

## Entradas

### Entrada 1

- **Fecha:** 2026-11-07
- **Prompt o sugerencia:** Prompt 1 ([`prompt1_pruebas.txt`](docs/prompts/prompt1_pruebas.txt)). Le pedí solo las pruebas pytest para el contrato de la HU-07, con la marca `criterio` y nombres en español, sin la implementación. ChatGPT propuso 12 pruebas, una tabla que clasifica cada una como normal, límite o error, y dos preguntas sobre el contrato.
- **Decisión:** Aceptada con cambios
- **Por qué:** Las pruebas cubrían los dos escenarios y los cinco ejemplos del contrato. Hice tres cambios:
  - Rechacé una prueba (entrada 2).
  - Agregué `assert resultado is not rutas`, porque el contrato pide una lista nueva y `resultado == rutas` pasaría aunque la función devolviera la misma lista.
  - Renombré algunas pruebas para que el nombre diga el resultado esperado (RNF-10), por ejemplo `test_HU07_E1_archivo_con_nombre_parecido_si_se_envia`.

  La clasificación también tenía un error: puso como caso «normal» el `.env` dentro de una subcarpeta, que en mi contrato es un caso límite.
- **Verificación:** Corrí `pytest` contra un esqueleto que lanza `NotImplementedError`. Las 14 pruebas fallaron por esa razón y no por errores de importación o de sintaxis.
- **Commit relacionado:** `0b72ae2` «Pruebas de la HU-07 lista de exclusión (en rojo)»

### Entrada 2

- **Fecha:** 2026-11-07
- **Prompt o sugerencia:** Dentro de la respuesta al prompt 1 venía la prueba `test_HU07_E1_distingue_mayusculas_y_minusculas`, que esperaba que `.ENV` sí se enviara a la IA cuando el patrón es `.env`.
- **Decisión:** Rechazada
- **Por qué:** La prueba cumplía lo que yo había escrito en el contrato («distingue mayúsculas»). Al leerla vi que el error era del contrato: en Windows y macOS `.ENV` y `.env` son el mismo archivo, así que esa prueba aprobaba que las claves salieran hacia la IA, contra RNF-06. Cambié el contrato para que la comparación no distinga mayúsculas y reemplacé la prueba por `test_HU07_E1_env_en_mayusculas_tampoco_se_envia`. El cambio está en un commit aparte y explicado en el README.
- **Verificación:** Con la implementación ya en verde, sembré el error de quitar el `.lower()`. Solo falló la prueba nueva. La prueba de ChatGPT habría pasado con ese error, que deja salir el `.env`.
- **Commit relacionado:** `4afca43` «Ajusta el contrato de la HU-07: la comparación no distingue mayúsculas y admite comodines»

### Entrada 3

- **Fecha:** 2026-11-07
- **Prompt o sugerencia:** Al final de la respuesta al prompt 1, ChatGPT hizo dos preguntas sobre el contrato:
  - Si `archivo_pedido` ya está en `rutas`, ¿se compara antes o después de normalizar las barras?
  - ¿Los patrones admiten comodines como `*.csv`?
- **Decisión:** Aceptada
- **Por qué:** Las dos preguntas señalaban huecos reales del contrato. Las respondí en el README: se compara después de normalizar, y los patrones son glob, así que `*.db` excluye `datos/pedidos.db`. Agregué los ejemplos 6 y 7 y dos pruebas: `test_HU07_E1_archivo_pedido_que_ya_venia_no_se_repite` y `test_HU07_E1_patron_con_comodin_excluye_por_extension`.
- **Verificación:** Sembré el error de no normalizar las barras de Windows. Fallaron la prueba de rutas de Windows y la nueva prueba del archivo pedido repetido.
- **Commit relacionado:** `4afca43` (contrato) y `0b72ae2` (pruebas)

### Entrada 4

- **Fecha:** 2026-11-07
- **Prompt o sugerencia:** ChatGPT recomendó correr las pruebas con `pytest -v -m "criterio('HU-07-E1') or criterio('HU-07-E2')"` y registrar la marca `criterio` en la configuración de pytest.
- **Decisión:** Rechazada (el comando). Lo de registrar la marca ya estaba hecho en `pyproject.toml`.
- **Por qué:** La opción `-m` de pytest selecciona por el nombre de la marca, no por su argumento posicional, así que el comando no filtra por criterio. La guía pide que todas las pruebas corran con un solo comando, y ese comando es `pytest`.
- **Verificación:** Corrí el comando sugerido y respondió `no tests ran`: no ejecutó ninguna de las 14 pruebas. Con `pytest` corren las 14.
- **Commit relacionado:** README, sección «Cómo ejecutar las pruebas» (`61b74ab`)

### Entrada 5

- **Fecha:** 2026-11-07
- **Prompt o sugerencia:** Prompt 2 ([`prompt2_implementacion.txt`](docs/prompts/prompt2_implementacion.txt)). Le pasé el contrato final y las 14 pruebas, y le pedí la implementación más simple de `asistente/exclusion.py`, solo con la librería estándar, sin cambiar la firma y sin tocar las pruebas.
- **Decisión:** Aceptada
- **Por qué:** Leí el código línea por línea:
  - `replace("\\", "/")` normaliza las rutas de Windows.
  - `.lower()` en la ruta y en el patrón hace que no distinga mayúsculas.
  - `rsplit("/", 1)[-1]` saca el nombre del archivo.
  - `fnmatchcase` compara el glob igual en todos los sistemas. `fnmatch` en Windows cambia las reglas de mayúsculas, así que no conviene.
  - La excepción se lanza antes de armar la lista, así que si el archivo pedido está excluido no se devuelve nada.

  Cumple el contrato y no modifica las listas recibidas. ChatGPT anotó como supuesto que la revisión de «ya estaba en `rutas`» sí distingue mayúsculas. Eso no está en el contrato y no deja salir archivos excluidos, así que lo dejo como pregunta para la próxima versión.
- **Verificación:** `pytest`: 14 passed en el primer intento. Para comprobar que las pruebas no pasaban por casualidad, sembré 3 errores y en todos fallaron pruebas:
  - Sin `.lower()`: 1 prueba en rojo.
  - Sin comparar el nombre del archivo: 5 pruebas en rojo, entre ellas la de error HU-07-E2.
  - Sin normalizar las barras: 2 pruebas en rojo.

  Después restauré el código.
- **Commit relacionado:** `9b75801` «Implementa seleccionar_archivos con ChatGPT: las 14 pruebas de la HU-07 pasan (en verde)»

### Entrada 6

- **Fecha:** 2026-11-07
- **Prompt o sugerencia:** Prompt 3 ([`prompt3_refactor.txt`](docs/prompts/prompt3_refactor.txt)). Le pedí refactors sin cambiar el comportamiento, cada uno por separado y con su riesgo. Propuso seis:
  1. Sacar `normalizar` a `_normalizar_ruta`.
  2. Normalizar los patrones una sola vez.
  3. Sacar `esta_excluido` a `_esta_excluido`.
  4. No normalizar varias veces las mismas rutas.
  5. Usar nombres más claros.
  6. Mantener `fnmatchcase`.
- **Decisión:** Aceptada con cambios
- **Por qué:** Los seis cambios eliminan duplicación y funciones anidadas, y facilitan explicar el código. Les hice dos ajustes:
  - En su versión, `_esta_excluido(ruta, patrones)` solo funciona bien si los patrones ya vienen en minúscula, y ni el nombre ni la docstring lo decían. Si alguien la llama después con los patrones crudos, vuelve a distinguir mayúsculas sin que nadie lo note. Renombré el parámetro a `patrones_en_minuscula` y lo documenté.
  - La variable `pedido_normalizado` se creaba dentro de un `if` y se usaba en otro. Funcionaba, pero era frágil, así que la calculo una sola vez al principio.

  También devolví la docstring del módulo, que el refactor había quitado.
- **Verificación:** `pytest`: 14 passed sin modificar ninguna prueba. `git diff` no muestra cambios en `tests/`.
- **Commit relacionado:** `d70fea0` «Refactor de exclusion.py sin cambiar comportamiento…»

## Resumen

| Decisión | Cantidad |
|---|---|
| Aceptadas | 2 (entradas 3 y 5) |
| Aceptadas con cambios | 2 (entradas 1 y 6) |
| Rechazadas | 2 (entradas 2 y 4) |

## Errores que atraparon las pruebas

El error más importante lo encontré al revisar las pruebas, antes de escribir código. La prueba de mayúsculas que propuso ChatGPT aprobaba enviar `.ENV`, y eso venía de un defecto de mi propio contrato (entrada 2). Lo corregí y escribí una prueba que exige excluirlo.

La implementación de ChatGPT pasó las 14 pruebas a la primera, así que ninguna prueba falló con su código. Para comprobar que las pruebas detectan errores reales, sembré 3 errores a propósito y en los tres fallaron pruebas (entrada 5). El error de quitar `.lower()` solo lo detecta la prueba que escribí para reemplazar la de ChatGPT. Con la prueba original, ese error habría pasado en verde y el `.env` en mayúsculas habría salido hacia la IA.

## Reflexión final

Lo que más me ayudó de ChatGPT fue proponer pruebas a partir del contrato: en un minuto tenía 12 pruebas bien nombradas y dos preguntas que mostraron huecos que yo no había visto (comodines y rutas repetidas). La implementación también salió correcta a la primera. Aun así tuve que leer cada línea, porque una prueba en verde no dice si la prueba está bien. El error que más me enseñó no lo atrapó una prueba: estaba en una prueba. ChatGPT siguió al pie de la letra mi contrato y escribió una prueba que aprobaba enviar `.ENV`, que en Windows es el mismo `.env`. Solo los errores sembrados mostraron que esa prueba no protegía nada. En la próxima funcionalidad revisaría el contrato contra los requisitos no funcionales (en este caso RNF-04 y RNF-06) antes de pedir pruebas. También sembraría errores desde el principio para medir si las pruebas sirven, que es la meta de 8 de 10 errores detectados del proyecto.

---

# Semana 6: revisión de seguridad, agente y documentación

Commit revisado: `61a2af1`. El informe completo está en [`revision_seguridad.md`](revision_seguridad.md). Los prompts siguen las plantillas de la clase del 14/11: «Prompt para revisar código con IA» y «Cómo delimitar la tarea de un agente».

### Entrada 7

- **Fecha:** 2026-11-14
- **Prompt o sugerencia:** Prompt 4 ([`prompt4_revision_seguridad.txt`](docs/prompts/prompt4_revision_seguridad.txt)). Usé el prompt de revisión de la clase en un chat nuevo de ChatGPT, con el código con números de línea, las pruebas, la HU-07, los RNF y el ADR. ChatGPT entregó:
  - 6 problemas «seguros».
  - 4 sospechas.
  - La revisión de los 5 puntos de seguridad.
  - 7 pruebas recomendadas.
- **Decisión:** Aceptada con cambios
- **Por qué:** Verifiqué cada hallazgo antes de usarlo:
  - Dos son reales en parte (rutas con `..` y patrones sin normalizar), pero su ejemplo `config/../.env` ya se excluía. El problema real aparece con patrones que llevan carpeta, y la IA no lo mostró.
  - Tres son falsos positivos o repeticiones (líneas 41, 60–61 y 64–65).
  - Las sospechas no aplican todavía, porque no existe el módulo que envía a Gemini. Quedaron como pendientes.
  - La IA no encontró las variantes de Windows (`.env `, `.env.`, `.env::$DATA`) ni el aviso E501.
- **Verificación:** Ejecuté cada ejemplo de la IA y cada evasión contra la versión `61a2af1` con `python -I -c "…seleccionar_archivos(…)"`. La clasificación completa está en la sección 3 de `revision_seguridad.md`.
- **Commit relacionado:** `3072702` (ruff, `.env.example`, versiones fijadas) y el informe.

### Entrada 8

- **Fecha:** 2026-11-14
- **Prompt o sugerencia:** En la misma respuesta, ChatGPT recomendó 7 pruebas nuevas: `config/../.env`, `C:\proyecto\.env`, `/home/usuario/proyecto/.env`, `config\..\clientes_panaderia.csv`, archivo pedido `config/../.env`, `.ENV` y `respaldo.db`.
- **Decisión:** Rechazada
- **Por qué:** Las 7 ya pasaban con el código revisado, así que no detectan nada nuevo. Agregarlas solo inflaría el conteo de pruebas. En su lugar le pedí al agente las 8 evasiones que sí fallaban, más 1 prueba de error.
- **Verificación:** Corrí los 7 casos contra `61a2af1` y todos se excluían o lanzaban `ArchivoExcluidoError`.
- **Commit relacionado:** no aplica (no se agregaron).

### Entrada 9

- **Fecha:** 2026-11-14
- **Prompt o sugerencia:** Prompt 5 ([`prompt5_agente_pruebas_abuso.txt`](docs/prompts/prompt5_agente_pruebas_abuso.txt)). Usé la plantilla del agente de la clase:
  - **Rol:** agente en la rama `agente/pruebas-abuso`.
  - **Tarea:** agregar pruebas de abuso para las 8 evasiones y hacerlas pasar.
  - **Formato:** resumen de archivos cambiados, pruebas y resultado de pytest.
  - **Restricciones:** solo `asistente/exclusion.py` y `tests/`, sin instalar paquetes, y detenerse si había que cambiar una prueba existente.

  ChatGPT devolvió `tests/test_hu07_abuso.py` (10 casos parametrizados) y `exclusion.py` corregido.
- **Decisión:** Aceptada, después de revisar el diff.
- **Por qué:**
  - Seguí los permisos de la clase: el agente trabajó en su propia rama y `main` solo recibió el cambio revisado (`git merge --no-ff`).
  - En el diff confirmé que no tocó `tests/test_hu07_exclusion.py` (0 líneas cambiadas), que no agregó dependencias y que mantuvo la firma.
  - Su corrección normaliza la ruta solo para comparar, y la ruta permitida se devuelve igual que antes.
  - Un efecto que acepté a propósito: ahora `otra/datos/clientes_panaderia.csv` también se excluye, porque compara contra cada sufijo de la ruta. Ante la duda se excluye (RNF-06).
- **Verificación:**
  - Con sus pruebas y el código anterior: 9 pruebas fallidas y 15 aprobadas (commit en rojo).
  - Con su corrección: 24 aprobadas.
  - `ruff check .` sin avisos.
  - El agente afirmó «10 passed», pero solo corrió sus pruebas nuevas en su entorno, y dijo que no pudo verificar ruff. La suite completa y el linter los corrí yo en el proyecto.
- **Commit relacionado:** `9780a9c` (pruebas en rojo), `daeb3bb` (corrección) y `2b9aedd` (integración a `main`).

### Entrada 10

- **Fecha:** 2026-11-14
- **Prompt o sugerencia:** Prompt 6 ([`prompt6_docstrings.txt`](docs/prompts/prompt6_docstrings.txt)). Le pedí docstrings con el formato de la clase (Args, Returns, Raises) sin cambiar ni una línea de código.
- **Decisión:** Aceptada
- **Por qué:** Cada docstring dice lo que hace el código. La de `seleccionar_archivos` documenta el error `ArchivoExcluidoError` y que el archivo pedido se agrega al final. Solo le falta mencionar que la comparación no distingue mayúsculas; es una omisión, no algo falso, y está explicado en el contrato del README.
- **Verificación:**
  - Comparé el árbol de sintaxis (`ast`) del archivo, sin docstrings, antes y después: la lógica quedó idéntica.
  - `ruff check .` sin avisos.
  - 24 pruebas aprobadas.
- **Commit relacionado:** `4206999`

### Entrada 11

- **Fecha:** 2026-11-14
- **Prompt o sugerencia:** Prompt 7 ([`prompt7_readme.txt`](docs/prompts/prompt7_readme.txt)). Le pedí el README con las 8 secciones de la clase, dándole solo datos reales del repositorio.
- **Decisión:** Aceptada
- **Por qué:**
  - Usó solo los datos que le di: no inventó comandos ni archivos.
  - Al copiar la respuesta, los bloques de código llegaron con marcadores de más (```` y títulos en negrita). Solo corregí esos marcadores, sin cambiar el texto.
  - Debajo dejé, sin cambios, la sección «Funcionalidad de la semana 5» con el contrato.
- **Verificación:** Probé los comandos del README en una carpeta limpia, clonando el repositorio:
  - Instalación: `python -m venv .venv` y `pip install -r requirements-dev.txt`.
  - Activación en PowerShell con `.venv\Scripts\activate`.
  - `pytest`: 24 aprobadas.
  - `ruff check .`: limpio.
  - `pip-audit -r requirements-dev.txt`: sin vulnerabilidades.
  - El ejemplo de «Ejecución» imprime `['app/pedidos/validaciones.py']`.
- **Commit relacionado:** `d5977ab`

## Resumen de la semana 6

| Decisión | Cantidad |
|---|---|
| Aceptadas | 3 (entradas 9, 10 y 11) |
| Aceptadas con cambios | 1 (entrada 7) |
| Rechazadas | 1 (entrada 8) |

## Reflexión de la semana 6

- La revisión con IA sirvió como segunda revisora, pero no reemplazó la mía. Apuntó a la zona correcta (la normalización de rutas), aunque con ejemplos que ya funcionaban.
- Las evasiones más graves no las vio: los nombres que Windows abre como el mismo `.env`. Las encontré al pensar en cómo se puede abrir el mismo archivo con otro nombre en los tres sistemas operativos del equipo.
- Usar ChatGPT como agente en una rama, con una instrucción delimitada, funcionó bien. Revisar el diff fue lo que me dio confianza para integrarlo, no su «10 passed», porque ese resultado no incluía las pruebas que ya existían.
- Para la próxima vez: escribir las pruebas de abuso desde el contrato, antes de pedir el código, y no esperar a la revisión de seguridad.
