# Bitácora de uso de IA

Proyecto: Asistente de IA que propone pruebas pytest a partir de los criterios de aceptación del módulo de pedidos de una app para panadería de barrio
Estudiante: Kenneth Ramírez Burgos
Funcionalidad: HU-07 Lista de exclusión de archivos (`seleccionar_archivos`)
Asistente usado: ChatGPT (OpenAI), versión web, modo chat, en una sola conversación el 7 de noviembre de 2026. Le di como contexto el contrato y las pruebas. El código lo pegué y lo ejecuté en VS Code con pytest.

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
