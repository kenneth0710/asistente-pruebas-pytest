# Registro de pruebas: tabla de casos y pruebas de la IA

Proyecto: Asistente de IA que propone pruebas pytest a partir de los criterios de aceptación del módulo de pedidos (app de panadería de barrio)
Estudiante: Kenneth Ramírez Burgos
Fecha: 2026-11-21
Commit de partida: `7a2f207` (entrega de la semana 6)

Probé las tres funciones de `asistente/exclusion.py` que tienen reglas de negocio de la HU-07:
- `seleccionar_archivos`: es la que combina varias condiciones, así que lleva tabla de decisión.
- `_normalizar_para_comparar`
- `_esta_excluido`

Las reglas salen del contrato de la semana 5 (README) y de las correcciones H-01 y H-02 de la semana 6 (`revision_seguridad.md`). Esas reglas son el oráculo: los esperados salen de ellas, nunca de ejecutar el código.

Resultado final: **102 pruebas en verde** con `pytest -v` y `ruff check .` sin avisos.
- 24 pruebas de las semanas 5 y 6.
- 74 casos nuevos de las tres funciones.
- 2 pruebas con datos sintéticos.
- 2 pruebas de aceptación de HU-07 (sección 6, agregadas el 2026-11-26).

La cobertura la mide el pipeline en cada push (sección 5): 96 % de líneas y 92,86 % de ramas.

Las pruebas nuevas encontraron un **defecto real (D-01)**, que se corrigió en el código sin tocar ninguna prueba.

Los prompts exactos están en [`docs/prompts/`](docs/prompts/), del 8 al 14, y en la bitácora, entradas 12 a 17. La cobertura y las pruebas de aceptación usan los prompts 17 a 19 (entradas 20 y 21).

## 1. Tabla de casos

### Regla: `seleccionar_archivos(rutas, patrones, archivo_pedido=None)`: devuelve las rutas permitidas y gestiona el archivo pedido

**Regla completa (el oráculo, HU-07-E1 y HU-07-E2, contrato de la semana 5):**
- Devuelve una lista nueva con las rutas que no están excluidas, en el mismo orden en que llegaron y escritas con «/» en lugar de «\». Las rutas repetidas se conservan.
- Si `archivo_pedido` es `None`, solo filtra.
- Si `archivo_pedido` está excluido, lanza `ArchivoExcluidoError` con la ruta en el mensaje y no devuelve nada.
- Si `archivo_pedido` está permitido y no estaba en `rutas` (comparando después de cambiar «\» por «/»), se agrega al final. Si ya estaba, no se repite.
- La exclusión sigue la regla de `_esta_excluido`, y la comparación no distingue mayúsculas.

| Técnica | Partición o límite | Entrada | Esperado | Prueba que lo cubre |
|---|---|---|---|---|
| Límite | Lista de rutas vacía | R=`[]`, P=`[".env"]` | `[]` | `test_HU07_E1_lista_de_rutas_vacia_devuelve_lista_vacia` (S02, ya existía) |
| Límite | Una ruta permitida | R=`["main.py"]`, P=`[".env"]` | `["main.py"]` | `test_filtrar_rutas[S03]` |
| Límite | Una ruta excluida | R=`[".env"]`, P=`[".env"]` | `[]` | `test_filtrar_rutas[S04]` |
| Partición | Varias permitidas: conserva el orden | R=`["b.py","a.py","c.py"]` | igual | `test_HU07_E1_conserva_el_orden_de_archivos_permitidos` (S05, ya existía) |
| Partición | Permitidas y excluidas mezcladas | R=`["main.py",".env","test.py","pedidos.db"]`, P=`[".env","pedidos.db"]` | `["main.py","test.py"]` | `test_filtrar_rutas[S07]` |
| Límite | Lista de patrones vacía | R=`["main.py",".env"]`, P=`[]` | `["main.py",".env"]` | `test_filtrar_rutas[S08]` |
| Partición | Permitidas repetidas se conservan | R=`["a.py","a.py"]` | `["a.py","a.py"]` | `test_filtrar_rutas[S09]` |
| Partición | Excluidas repetidas se quitan todas | R=`[".env",".env"]` | `[]` | `test_filtrar_rutas[S10]` |
| Partición | Separadores de Windows en la salida | R=`["src\\main.py"]`, P=`[]` | `["src/main.py"]` | `test_filtrar_rutas[S12]` |
| Partición | Ruta excluida en mayúsculas | R=`[".ENV"]`, P=`[".env"]` | `[]` | `test_filtrar_rutas[S13]` |
| Partición | La salida conserva las mayúsculas | R=`["Main.PY"]` | `["Main.PY"]` | `test_filtrar_rutas[S14]` |
| Partición | La salida solo cambia «\» | R=`["./src//main.py"]` | `["./src//main.py"]` | `test_filtrar_rutas[S15]` |
| Partición inválida (abuso) | `..` dentro de la carpeta del patrón | R=`["datos/x/../clientes_panaderia.csv","main.py"]`, P=`["datos/clientes_panaderia.csv"]` | `["main.py"]` | `test_filtrar_rutas[S29]` |
| Partición | Patrón en mayúsculas | R=`[".env","main.py"]`, P=`[".ENV"]` | `["main.py"]` | `test_filtrar_rutas[S30]` |
| Decisión R1 | Sin archivo pedido | A=`None` | `["a.py"]` | `test_gestionar_archivo_pedido[S17]` |
| Decisión R2 | Pedido excluido y presente | A=`".env"` | `ArchivoExcluidoError` | `test_rechazar_archivo_pedido_excluido[S18]` |
| Decisión R2 | Pedido excluido y ausente | A=`"pedidos.db"` | `ArchivoExcluidoError` | `test_rechazar_archivo_pedido_excluido[S19]` |
| Decisión R2 | Pedido excluido por flujo NTFS | A=`".env::$DATA"` | `ArchivoExcluidoError` | `test_rechazar_archivo_pedido_excluido[S27]` |
| Decisión R3 | Pedido permitido y presente | R=`["a.py","b.py"]`, A=`"a.py"` | `["a.py","b.py"]` | `test_gestionar_archivo_pedido[S21]` |
| Decisión R3 | Presente con otro separador | R=`["app/pedidos/validaciones.py"]`, A=`"app\\pedidos\\validaciones.py"` | sin repetir | `test_HU07_E1_archivo_pedido_que_ya_venia_no_se_repite` (S23, ya existía) |
| Decisión R4 | Pedido permitido y ausente | A=`"c.py"` | se agrega al final | `test_HU07_E1_agrega_archivo_pedido_permitido_al_final` (S20, ya existía) |
| Decisión R4 + límite | Pedido con rutas vacías | R=`[]`, A=`"a.py"` | `["a.py"]` | `test_gestionar_archivo_pedido[S22]` |
| Decisión R4 | Pedido nuevo con «\» | A=`"src\\b.py"` | `["a.py","src/b.py"]` | `test_gestionar_archivo_pedido[S26]` |
| Partición | Devuelve una lista nueva | R=`["a.py"]`, P=`[]` | igual y `is not R` | `test_HU07_E1_sin_patrones_se_envian_todas_en_una_lista_nueva` (S28, ya existía) |
| Partición (datos sintéticos) | Repositorio ficticio completo | fixture `repo_panaderia` | lista fija de 6 archivos permitidos | `test_filtrar_repositorio_panaderia` |

**Tabla de decisión.** Condiciones:
- C1: ¿hay `archivo_pedido`?
- C2: ¿el archivo pedido está excluido?
- C3: ¿ya estaba en `rutas`?

Son 2 × 2 × 2 = 8 combinaciones. Se simplifican a 4, porque si no hay archivo pedido, C2 y C3 no importan, y si está excluido, C3 no importa.

| Regla | C1 | C2 | C3 | Acción | Pruebas |
|---|---|---|---|---|---|
| R1 | No | — | — | Solo filtra | S17 |
| R2 | Sí | Sí | — | `ArchivoExcluidoError`, no devuelve nada | S18, S19, S27 |
| R3 | Sí | No | Sí | Filtra sin repetir el pedido | S21, S23 |
| R4 | Sí | No | No | Filtra y agrega el pedido al final | S20, S22, S26 |

### Regla: `_normalizar_para_comparar(ruta)`: forma única de una ruta, solo para comparar (RNF-04, H-01, H-02)

**Regla completa (el oráculo):**
- a) «\» se cambia por «/».
- b) Se quitan los componentes vacíos (`//`) y los `.`.
- c) `..` elimina el componente anterior. Si no hay componente anterior, en una ruta relativa el `..` se conserva y en una absoluta se descarta.
- d) A cada componente se le quitan los espacios y los puntos del final.
- e) Si un componente tiene «:», se corta desde el «:» (flujo de NTFS), excepto una letra de unidad de dos caracteres como `C:`.
- f) El resultado queda en minúsculas.
- g) Una ruta absoluta conserva el «/» inicial.

| Técnica | Partición o límite | Entrada | Esperado | Prueba que lo cubre |
|---|---|---|---|---|
| Límite | Cadena vacía | `""` | `""` | `test_normalizar_ruta_para_comparar[N01]` |
| Partición | Ya normalizada | `"datos/pedidos.db"` | igual | `[N03]` |
| Partición | Separadores de Windows | `"datos\\pedidos.db"` | `"datos/pedidos.db"` | `[N04]` |
| Límite | Barra doble | `"datos//pedidos.db"` | `"datos/pedidos.db"` | `[N06]` |
| Límite | Barra al final | `"datos/"` | `"datos"` | `[N08]` |
| Límite | Ruta absoluta | `"/datos/pedidos.db"` | igual | `[N09]` |
| Límite | Solo la raíz | `"/"` | `"/"` | `[N10]` |
| Partición | `.` al inicio | `"./.env"` | `".env"` | `[N12]` |
| Partición | `.` intermedio | `"datos/./pedidos.db"` | `"datos/pedidos.db"` | `[N13]` |
| Límite | Solo `.` | `"."` | `""` | `[N15]` |
| Partición | `..` con anterior | `"x/../.env"` | `".env"` | `[N16]` |
| Partición | Varios `..` | `"a/b/../../.env"` | `".env"` | `[N17]` |
| Partición | `..` sin anterior, relativa | `"../datos/pedidos.db"` | igual | `[N18]` |
| Partición | `..` sin anterior, absoluta | `"/../.env"` | `"/.env"` | `[N19]` |
| Límite | `..` deja la ruta vacía | `"a/.."` | `""` | `[N20]` |
| Límite | `..` vuelve a la raíz | `"/a/.."` | `"/"` | `[N21]` |
| Límite | Espacio final | `".env "` | `".env"` | `[N22]` |
| Límite | Punto final | `".env."` | `".env"` | `[N24]` |
| Partición | Puntos y espacios finales | `".env. . "` | `".env"` | `[N26]` |
| Partición | Limpieza en componente intermedio | `"datos. /pedidos.db"` | `"datos/pedidos.db"` | `[N27]` |
| Partición | Espacio inicial no se quita | `" .env"` | `" .env"` | `[N28]` |
| Partición | Puntos internos se conservan | `"archivo.test.py"` | igual | `[N29]` |
| Partición | Flujo NTFS | `".env::$DATA"` | `".env"` | `[N30]` |
| Partición | «:» en componente intermedio | `"datos:flujo/pedidos.db"` | `"datos/pedidos.db"` | `[N31]` |
| Límite | Letra de unidad sola | `"C:"` | `"c:"` | `[N32]` |
| Partición | Ruta con unidad | `"C:\\Datos\\PEDIDOS.DB"` | `"c:/datos/pedidos.db"` | `[N33]` |
| Partición | Mayúsculas | `"DATOS/CLIENTES_PANADERIA.CSV"` | en minúsculas | `[N34]` |
| Partición | Varias reglas juntas | `"/DATOS//./x/../.ENV. "` | `"/datos/.env"` | `[N36]` |
| Límite (agregado tras M7) | Nombre de una letra con flujo: no es una unidad | `"a:$DATA"` | `"a"` | `[N38]` |

### Regla: `_esta_excluido(ruta, patrones_normalizados)`: decide si una ruta no puede salir hacia la IA (HU-07, RNF-06)

**Regla completa (el oráculo):**
- La ruta se normaliza con la regla anterior.
- Queda excluida (`True`) si algún patrón glob, ya normalizado, coincide con la ruta completa, con cualquier final de la ruta formado por componentes completos, o con el nombre del archivo.
- Sin coincidencias, o sin patrones, devuelve `False`.

| Técnica | Partición o límite | Entrada (ruta, patrones) | Esperado | Prueba que lo cubre |
|---|---|---|---|---|
| Límite | Sin patrones | `".env"`, `[]` | `False` | `test_determinar_si_ruta_esta_excluida[E01]` |
| Límite | Un patrón que coincide | `".env"`, `[".env"]` | `True` | `[E03]` |
| Límite | Un patrón que no coincide | `"main.py"`, `[".env"]` | `False` | `[E04]` |
| Partición | Coincide la ruta completa | `"datos/pedidos.db"`, `["datos/pedidos.db"]` | `True` | `[E05]` |
| Partición | Coincide un final de la ruta | `"c:/repo/datos/clientes_panaderia.csv"`, `["datos/clientes_panaderia.csv"]` | `True` | `[E06]` |
| Partición | Coincide el nombre | `"src/config/.env"`, `[".env"]` | `True` | `[E07]` |
| Partición inválida | Componente parecido | `"misdatos/pedidos.db"`, `["datos/pedidos.db"]` | `False` | `[E08]` |
| Partición inválida | Nombre parecido | `"archivo.env"`, `[".env"]` | `False` | `[E09]` |
| Partición inválida | Patrón al comienzo, no al final | `"datos/pedidos.db/copia.py"`, `["datos/pedidos.db"]` | `False` | `[E10]` |
| Partición | Comodín que coincide | `"datos/pedidos.db"`, `["*.db"]` | `True` | `[E11]` |
| Partición inválida | Comodín que no coincide | `"datos/pedidos.csv"`, `["*.db"]` | `False` | `[E12]` |
| Partición | Varios patrones, ninguno coincide | `"main.py"`, `[".env","*.db","*.csv"]` | `False` | `[E17]` |
| Límite | Varios patrones, coincide el último | `"clientes_panaderia.csv"`, igual | `True` | `[E20]` |
| Partición | Ruta en mayúsculas | `"DATOS/PEDIDOS.DB"`, `["datos/pedidos.db"]` | `True` | `[E23]` |
| Partición | Separadores de Windows | `"datos\\pedidos.db"` | `True` | `[E24]` |
| Partición | `.` y barras dobles | `"./datos//./pedidos.db"` | `True` | `[E25]` |
| Partición (abuso) | `..` dentro de la carpeta del patrón | `"datos/x/../pedidos.db"`, `["datos/pedidos.db"]` | `True` | `[E36]` |
| Partición | `..` sobre la raíz | `"/../.env"`, `[".env"]` | `True` | `[E27]` |
| Límite | Espacio final | `".env "`, `[".env"]` | `True` | `[E28]` |
| Límite | Punto final | `".env."`, `[".env"]` | `True` | `[E29]` |
| Partición | Flujo NTFS | `".env::$DATA"`, `[".env"]` | `True` | `[E30]` |
| Partición | «:» con número | `"datos/clientes_panaderia.csv:1"`, `["clientes_panaderia.csv"]` | `True` | `[E31]` |
| Límite | Barra final | `"datos/pedidos.db/"`, `["pedidos.db"]` | `True` | `[E32]` |
| Partición | Ruta y patrón absolutos | `"/datos/pedidos.db"`, `["/datos/pedidos.db"]` | `True` | `[E33]` |
| Partición inválida | Ruta relativa, patrón absoluto | `"datos/pedidos.db"`, `["/datos/pedidos.db"]` | `False` | `[E34]` |
| Límite (agregado tras M7) | Archivo de una letra con flujo NTFS | `"a:$DATA"`, `["a"]` | `True` | `[E37]` |

**Ambigüedades encontradas.** ChatGPT señaló 20 y yo comprobé las principales. Las que no tienen respuesta en la regla no se convirtieron en prueba: quedan para decidir con el docente o con el cliente.

| # | Ambigüedad | Qué hace hoy el código | Decisión |
|---|---|---|---|
| A1 | `archivo_pedido=""` (cadena vacía) | Agrega `""` al resultado | Pendiente con el cliente. Propuesta: tratarlo como error. |
| A2 | Rutas vacías dentro de `rutas` (`["", "a.py"]`) | Las conserva | Pendiente. La CLI no debería generarlas. |
| A3 | Patrón vacío `""` | No excluye nada | Pendiente. Propuesta: ignorarlo al leer `.asistenteignore`. |
| A4 | ¿Quién normaliza los patrones en `seleccionar_archivos`? | La propia función | **Resuelta:** el contrato de la semana 5 dice que no distingue mayúsculas. Se agregó S30. |
| A5 | Prioridad entre la regla c (`..`) y la d (quitar puntos finales) | Antes de D-01, la d se comía el `..` | **Resuelta:** manda la c. Era el defecto D-01 y se corrigió. |
| A6 | `.. ` (con espacio final): ¿es `..`? | No lo trata como `..`, y `datos/x/.. /clientes_panaderia.csv` no se excluye con un patrón de carpeta | **Pendiente (riesgo):** Windows lo abre como `..`. Ver la sección 3, P-05. |
| A7 | Componente `...` | Queda vacío y se descarta | Pendiente con el docente. |
| A8 | `C:/../.env`, rutas UNC (`\\servidor\recurso`) y prefijos `\\?\` | `C:` se trata como un componente más | Fuera del alcance de la HU-07. Pendiente para la CLI. |
| A9 | Significado de `*`, `?`, `**` y patrones mal formados | Se usa `fnmatch` de la librería estándar (`*` también cruza «/») | **Resuelta** por el ADR-001: solo librería estándar. No se prueba la librería (se descartaron E13–E16). |
| A10 | Tipos incorrectos (`None`, números) y longitudes máximas | No definidos | Fuera del contrato. |
| A11 | Enlaces simbólicos | La función no lee el disco | Ya era el pendiente P-03 de la semana 6. |

## 2. Pruebas de la IA descartadas o corregidas

**Prompts usados:** las plantillas del profesor de la clase del 21/11 («Actúa como analista de pruebas…» y «Actúa como desarrollador que escribe pruebas con pytest…»), en una conversación de ChatGPT. Están en `docs/prompts/prompt8_diseno_casos.txt` y `prompt9_generar_pruebas.txt`, y en las entradas 12 y 13 de la bitácora.
- **Diseño de casos:** ChatGPT propuso 100 casos, la tabla de decisión y 20 ambigüedades.
- **Mi revisión:** con las 5 preguntas de la clase (particiones, límites, origen del esperado, ambigüedades y reglas inventadas) dejé 77 casos, más 2 que agregué después por la mutación M7.
- **Generación:** ChatGPT escribió las pruebas a partir de la tabla revisada.
- **Revisión de cada prueba:** con las 3 preguntas de la guía.

| Prueba o caso generado | Decisión | Por qué | En su lugar |
|---|---|---|---|
| Casos de diseño S01, S06, S11, S25, N02, N05, N07, N11, N14, N23, N25, N35, E02, E18, E19, E21, E22, E35 | Descartados | Redundantes: otro caso de la misma partición ya cubre el valor | Se dejó un caso por partición |
| Casos E13–E16 (`?` y `*` con cero caracteres) | Descartados | Prueban la librería `fnmatch`, no una regla del proyecto | Se dejaron E11 y E12, que prueban la regla «patrones glob» con un ejemplo del proyecto |
| Caso N37 (componentes repetidos) | Descartado | No sale de ninguna regla escrita; no fallaría si rompo el código | Nada |
| Caso S24 (pedido `main.py` con ruta `Main.py` devuelve los dos) | Descartado | Su esperado sí sale de la regla, pero fija un comportamiento dudoso (pendiente P-04 de la semana 6) | Queda como ambigüedad |
| Caso S16 `x/../datos/pedidos.db` con patrón `pedidos.db` | Corregido | Débil: se excluye por el nombre, así que no prueba que `..` funcione | S29: `datos/x/../clientes_panaderia.csv` con patrón de carpeta |
| Caso E26 `x/../datos/pedidos.db` con patrón `datos/pedidos.db` | Corregido | Débil: se excluye por un final de la ruta aunque `..` no funcione | E36: `datos/x/../pedidos.db` |
| — | Agregado | La IA no tenía un caso de patrón en mayúsculas (contrato de la semana 5) | S30 |
| Pruebas S02, S05, S20, S23, S28 (`tests/test_s7_seleccionar_archivos.py`) | Descartadas | Redundantes: repiten exactamente pruebas de la semana 5 (ver la tabla 1) | Se las pedí quitar a ChatGPT (commit `6cc45e7`); la tabla apunta a la prueba original |
| `test_no_devolver_archivos_excluidos` (datos sintéticos) | Descartada | Débil y redundante: con una función que devuelve siempre `[]` seguía en verde | La cubre `test_filtrar_repositorio_panaderia`, con lista exacta (commit `680a9da`) |
| N16, N17, N18, N20, N21, N36, E36, S29 (fallaron al primer intento) | Conservadas sin cambios | El esperado sale de la regla 2c: era un **defecto real del código** | Se corrigió el código (D-01, commit `3238135`), no las pruebas |
| N38 y E37 | Agregadas | La mutación M7 sobrevivía a toda la suite | Se las pedí a ChatGPT (commit `0d132c1`) |

**Defecto D-01 encontrado por las pruebas.** Línea 55 de `_normalizar_para_comparar` en el commit `7a2f207`: `componente.rstrip(" .")` convertía `..` en una cadena vacía **antes** de revisar si era `..`. Por eso la regla c nunca se aplicaba y `datos/x/../clientes_panaderia.csv` salía hacia la IA con el patrón `datos/clientes_panaderia.csv`.
- La corrección de la semana 6 había dicho que resolvía el `..`, pero sus pruebas no lo detectaron: usaban `x/../datos/…`, que se excluye igual por el final de la ruta.
- Corrección: ChatGPT movió la revisión de `..` antes del `rstrip`. Las 8 pruebas pasaron sin tocarlas.

## 3. Romper el código a propósito

Cada cambio se hizo de uno en uno en `asistente/exclusion.py`, se corrió `pytest` y se deshizo con `git restore`. Los números de línea son los del commit `680a9da`.

| Cambio introducido | Archivo y línea | ¿Alguna prueba falló? | Qué hice |
|---|---|---|---|
| M1: `elif not ruta.startswith("/")` → `elif ruta.startswith("/")` (borde relativa/absoluta del `..`) | exclusion.py:46 | Sí, 2: N18 y N19 | Nada: la suite protege ese borde |
| M2: `rstrip(" .")` → `rstrip(" ")` (deja de quitar los puntos finales) | exclusion.py:55 | Sí, 6: N24, N26, N27, N36, E29 y la prueba de abuso `.env.` | Nada |
| M3: `_esta_excluido` devuelve siempre `False` (respuesta tonta) | exclusion.py:99 | Sí, 47 | Nada |
| M4: siempre agrega el archivo pedido (quita `not in rutas_normalizadas`) | exclusion.py:164 | Sí, 2: S21 y `test_HU07_E1_archivo_pedido_que_ya_venia_no_se_repite` | Nada |
| M5: quita la comparación por nombre de archivo | exclusion.py:105 | **No** | Es un **mutante equivalente**: el último «final de la ruta» ya es el nombre, así que ninguna prueba lo puede detectar. Muestra lógica duplicada. Ver P-06. |
| M6: los finales de la ruta empiezan en 1 (sin la ruta completa) | exclusion.py:83 | **No** | **Mutante equivalente**: la línea anterior ya compara la ruta completa. Ver P-06. |
| M7: la letra de unidad se reconoce sin revisar la longitud (`componente[1:2] == ":"`) | exclusion.py:50 | **No** en la primera corrida | **Se agregaron N38 y E37** (`"a:$DATA"`). Con ellos, M7 hace fallar 2 pruebas. |
| M8: `seleccionar_archivos` devuelve siempre `[]` | exclusion.py:167 | Sí, 34 | Nada. Este cambio mostró que `test_no_devolver_archivos_excluidos` era débil, y se descartó. |
| M9: quita el `.lower()` final de la normalización | exclusion.py:63 | Sí, 7: N33, N34, N36, E23, S13, S30 y `test_HU07_E1_env_en_mayusculas_tampoco_se_envia` | Nada |

**Pendientes que dejó esta semana.**
- **P-05.** El componente `.. ` (con espacio final) no se trata como `..` (ambigüedad A6). En Windows sí sube una carpeta, así que con un patrón de carpeta es una evasión residual. La regla 2 no fija el orden entre c) y d), y prefiero decidirlo con el docente antes de cambiar el contrato.
- **P-06.** La comparación por nombre y la de la ruta completa están duplicadas dentro de la de «finales de la ruta» (mutantes M5 y M6). No cambia el comportamiento, pero es una oportunidad de refactor para la próxima semana.

## 4. Datos de prueba

**Origen:** sintéticos, generados con ChatGPT (prompt 13, entrada 16 de la bitácora) y revisados por mí. Confirmo que no hay datos de personas reales. Los nombres son inventados, los teléfonos usan el patrón ficticio `300 000 xxxx` y la clave del `.env` es `clave-falsa-solo-para-pruebas`.

El fixture `repo_panaderia(tmp_path)` de `tests/test_s7_datos_sinteticos.py` crea en una carpeta temporal:
- un repositorio ficticio de la panadería con `.asistenteignore` (`.env`, `clientes_panaderia.csv`, `pedidos.db`, `*.bak`);
- un `.env` falso;
- `datos/clientes_panaderia.csv` con 8 clientes;
- `datos/pedidos.db` y `datos/respaldo_pedidos.bak`;
- 5 archivos de código.

**Casos difíciles incluidos:**
- **Nombres de clientes con tildes, ñ y apóstrofo:** «Ámbar Castañuelo», «Érika D'Avellana», «Nicolás Piñaluz».
- **Un nombre vacío y dos saldos en cero.**
- **Barrios de Neiva:** Cándido Leguízamo, Las Granjas, Santa Inés, Los Mártires, La Gaitana, Las Palmas, El Altico y El Jardín.
- **Nombres de archivo difíciles:** `app/pedidos/validación_año.py`, `app/Pedidos de Doña Ana's.py` (ñ, apóstrofo y espacios), `app/Inventario.PY` (mayúsculas) y `app/cálculo de precios.py`.
- **Un patrón con comodín:** `*.bak`.

`test_filtrar_repositorio_panaderia` comprueba que salen exactamente los 6 archivos permitidos, comparando contra una lista fija. `test_verificar_datos_sinteticos_del_csv` comprueba que los casos difíciles existen de verdad en el CSV.

## 5. Cobertura (semana 8, medida por el pipeline)

Comando del pipeline: `pytest tests/ --cov=asistente --cov-branch --cov-report=term-missing --cov-report=xml`. El reporte `coverage.xml` queda como artefacto de cada ejecución en GitHub Actions.

| Medida | Resultado |
|---|---|
| Líneas | 96 % (48 de 50) |
| Ramas | 92,86 % (26 de 28) |
| Combinada (la que imprime pytest-cov) | 95 % |
| Líneas sin ejecutar | `exclusion.py`: 58 y 106 |

Le pedí a ChatGPT que analizara las dos líneas con el prompt 17 ([`prompt17_cobertura.txt`](docs/prompts/prompt17_cobertura.txt), entrada 20 de la bitácora). La condición era que no propusiera pruebas solo para subir el porcentaje. Después comprobé cada afirmación ejecutando código:

| Línea | ¿Se puede alcanzar? | Comprobación | Decisión |
|---|---|---|---|
| 58 (`continue` cuando un componente queda vacío después de la regla d) | **Sí.** Con `" "` o con `datos/.../clientes_panaderia.csv`. | Ejecuté las dos entradas midiendo la cobertura: la línea 58 se ejecuta. Hoy `...` desaparece y la ruta queda `datos/clientes_panaderia.csv`. | **No escribo la prueba todavía.** Su esperado depende de la ambigüedad **A7**: la regla no dice si un componente que queda vacío después de la regla d se descarta. Escribirla ahora sería copiar lo que hace el código, no la regla. Queda pendiente con el docente, junto con A6 (`.. `). |
| 106 (`return True` por el nombre del archivo) | **No.** Es código muerto. | El nombre del archivo es el último «final de la ruta», y `_coincide_con_patron` ya lo compara en la línea 82. Si coincide, la función sale en la línea 104. Lo confirmé con 200 000 rutas y patrones aleatorios: ningún caso hace verdadera la línea 105 sin que antes lo sea la 103. | **No se puede probar.** Confirma que M5 es un mutante equivalente (sección 3). Se resuelve quitando la comparación duplicada en el refactor pendiente **P-06**, no con una prueba. |

**Qué dice este 95 %.** Las dos líneas que faltan no son descuidos de la suite: una espera una decisión de requisitos y la otra no se puede ejecutar. Pero la cobertura sola no prueba la calidad. En la semana 7, `test_no_devolver_archivos_excluidos` ejecutaba casi todo el código y aun así seguía en verde con una función que devolvía siempre `[]` (mutación M8). Lo que muestra la calidad de la suite son las mutaciones de la sección 3: 7 de 9 detectadas y las otras 2 equivalentes.

## 6. Pruebas de aceptación de HU-07 (semana 8)

Archivo: [`tests/test_aceptacion_hu07.py`](tests/test_aceptacion_hu07.py). Las generó ChatGPT con el prompt 18 a partir del **texto exacto** de los criterios del documento de requisitos de la semana 3. Las corrigió con el prompt 19, después de mi revisión (entrada 21 de la bitácora).

**Clasificación de los escenarios.** Los dos se pueden automatizar hoy en la librería: `seleccionar_archivos` devuelve justo «lo que se envía al servicio de IA», y `ArchivoExcluidoError` es el aviso. Lo que **todavía no se puede observar** es el envío real a la IA y el aviso que vería el usuario en pantalla, porque la CLI no existe. Las pruebas simulan esa parte, y la simulación está declarada en el propio archivo:
- `repositorio_panaderia` crea un repositorio ficticio en `tmp_path`;
- `leer_patrones` lee el `.asistenteignore`;
- `listar_archivos` reúne los archivos.

| Criterio (texto del requisito) | Prueba | Dado | Cuando | Entonces (qué se comprueba) |
|---|---|---|---|---|
| HU-07-E1: archivos excluidos | `test_archivos_excluidos_no_se_incluyen` | `.asistenteignore` con `.env`, `clientes_panaderia.csv` y `pedidos.db`, y los 3 archivos con contenido falso | `seleccionar_archivos` con todos los archivos del repositorio | Ninguno de los 3 está en el resultado, y el resultado es **exactamente** `.asistenteignore` más los 3 archivos del módulo `pedidos/` |
| HU-07-E2: pedido explícito de un archivo excluido | `test_pedido_explicito_de_archivo_excluido` | `.env` está en la lista de exclusión | `archivo_pedido=".env"` | Se lanza `ArchivoExcluidoError`, así que no se devuelve nada para enviar, y el aviso nombra `.env` y dice «excluido» |

**Lo que corregí de la primera versión de la IA** (prompt 19):

| Problema | Por qué era un problema | Corrección |
|---|---|---|
| E2 comparaba el mensaje completo: `== "El archivo '.env' está excluido."` | El esperado salía del código, no del criterio. El criterio solo pide que avise que está excluido, y con otra redacción la prueba fallaba aunque el criterio se cumpliera. | Comprueba que el aviso nombra `.env` y dice «excluido». |
| Comentarios `# Dado`, `# Cuando` y `# Entonces` vacíos | No dejaban ver qué parte del criterio cubría cada línea. | Cada comentario lleva el texto del criterio con sus datos. |
| `listar_archivos` quitaba `.asistenteignore` a escondidas | Era una regla inventada. El criterio solo excluye 3 archivos, y esa regla cambiaba la lista exacta esperada en E1. | `.asistenteignore` entra en las rutas y en la lista esperada. |

**Verificación.**
- Las 2 pruebas pasan y ruff no da avisos; la suite completa queda en 102 aprobadas.
- Con mutaciones, una a la vez y deshechas después:
  - `_esta_excluido` devuelve siempre `False`: fallan las 2;
  - `seleccionar_archivos` devuelve siempre `[]`: falla E1, gracias a la lista exacta;
  - se quita el `raise`: falla E2.
- Cambié la redacción del mensaje del error y las 2 pruebas siguieron en verde: ya no dependen del texto exacto.

**Lo que no cubren.** No prueban que la CLI lea el `.asistenteignore` real ni que el aviso llegue a la pantalla. Eso queda pendiente hasta que exista la CLI (ADR-001).
