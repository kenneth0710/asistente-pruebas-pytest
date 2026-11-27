# Informe final del proyecto integrador

**Proyecto:** Asistente de IA que propone pruebas pytest a partir de los criterios de aceptación (app de pedidos de una panadería de barrio).

**Estudiante:** Kenneth Ramírez Burgos

**Repositorio:** https://github.com/kenneth0710/asistente-pruebas-pytest

**Fecha:** 2026-11-26

## 1. Resumen

El proyecto surge de la necesidad de mejorar las pruebas de una aplicación de pedidos desarrollada por cinco estudiantes para una panadería de barrio en Neiva. Propuse un asistente de IA que genere pruebas pytest a partir de criterios de aceptación, sin comprometer los datos sensibles del repositorio. Durante el seminario utilicé Claude, Gemini y ChatGPT como apoyo en las fases de fundamentos, requisitos, diseño, construcción, pruebas y operación. Verifiqué sus resultados mediante la comparación con fuentes originales, cálculos manuales, revisión de código, pruebas automatizadas y errores introducidos a propósito. Implementé la HU-07, correspondiente al filtro de exclusión de archivos, con 102 pruebas aprobadas, una cobertura del 96 % de líneas y del 92,86 % de ramas. El resultado principal fue comprobar que una respuesta de IA aparentemente correcta, incluso acompañada de pruebas exitosas, puede contener errores que solo se identifican mediante una verificación independiente.

## 2. Problema y usuario

El usuario del sistema es un equipo de cinco estudiantes que desarrolla una aplicación de pedidos para una panadería de barrio en Neiva. El equipo está compuesto por tres programadores, una product owner y un líder encargado de aprobar los pull requests.

Antes de plantear el asistente, el equipo probaba manualmente uno o dos de cada cinco criterios de aceptación. Esto permitía que algunos errores pasaran inadvertidos, especialmente los relacionados con casos límite. Un ejemplo identificado durante el levantamiento de requisitos fue la posibilidad de que un pedido con una cantidad de cero unidades llegara a la cocina. Además, no existía un mecanismo que impidiera aprobar un pull request cuando el código presentaba errores.

El problema no consiste únicamente en escribir más pruebas, sino en comprobar que los criterios de aceptación realmente se cumplan. Una prueba que ejecuta correctamente el código, pero utiliza un resultado esperado equivocado, puede generar una falsa sensación de seguridad.

También identifiqué una restricción relacionada con la privacidad. El repositorio contiene archivos que no pueden enviarse a una IA externa:

- `.env`, que contiene claves.
- `clientes_panaderia.csv`, que contiene información de aproximadamente 300 clientes.
- `pedidos.db`, que contiene información de los pedidos.

Por esta razón, propuse un asistente que genere pruebas pytest a partir de los criterios de aceptación y fragmentos de código permitidos. Las pruebas propuestas deben ser revisadas individualmente por los desarrolladores antes de incorporarse al proyecto.

La protección de los archivos sensibles se estableció como una funcionalidad obligatoria. Decidí implementar primero la HU-07, correspondiente a la lista de exclusión, porque cualquier integración posterior con una IA externa dependerá de este mecanismo de protección.

Para obtener los requisitos realicé una entrevista con un compañero que representó al cliente. Su participación fue autorizada por escrito, incluido el uso de la entrevista con herramientas de IA. Omití su nombre y no publiqué la transcripción completa para proteger su privacidad. El documento de requisitos contiene citas textuales que permiten relacionar las necesidades identificadas con las historias de usuario.

Documentos de referencia:

- [Propuesta del proyecto — módulo 1](https://github.com/kenneth0710/asistente-pruebas-pytest/blob/main/docs/modulos/modulo1_propuesta.pdf).
- [Entrevista, requisitos y bitácora — módulo 2](https://github.com/kenneth0710/asistente-pruebas-pytest/blob/main/docs/modulos/modulo2_requisitos_y_bitacora.pdf).

## 3. La IA en el ciclo de vida

Utilicé la inteligencia artificial como herramienta de apoyo durante las diferentes fases del proyecto. En cada fase establecí una forma de verificar sus resultados de acuerdo con el tipo de actividad realizada. No utilicé el mismo mecanismo de verificación para un requisito, una decisión de arquitectura y una prueba automatizada, porque cada uno presenta riesgos diferentes.

| Módulo y fase | Qué hiciste con IA | Herramienta | Evidencia (enlace) | Cómo verificaste |
|---|---|---|---|---|
| 1. Fundamentos | Elaboré un banco de 10 prompts y redacté la propuesta del proyecto con apoyo de IA. También comparé respuestas de dos modelos mediante un laboratorio de validación de correos electrónicos. | Claude, ChatGPT y Gemini. | [Banco de prompts](https://github.com/kenneth0710/asistente-pruebas-pytest/blob/main/docs/modulos/modulo1_banco_de_prompts.pdf) y [propuesta](https://github.com/kenneth0710/asistente-pruebas-pytest/blob/main/docs/modulos/modulo1_propuesta.pdf). | Evalué cada respuesta mediante la ficha de la actividad y ejecuté el código generado. Probé una expresión regular de teléfono con seis casos. En el laboratorio de correos utilicé diez casos adicionales: ChatGPT acertó ocho y Gemini cinco. |
| 2. Requisitos | Extraje actores y necesidades de una entrevista, elaboré las historias HU-01 a HU-10 con criterios Gherkin, revisé defectos, definí los RNF-01 a RNF-10 y trabajé el modelo de dominio y la priorización MoSCoW. | Gemini. | [Requisitos y bitácora del módulo 2](https://github.com/kenneth0710/asistente-pruebas-pytest/blob/main/docs/modulos/modulo2_requisitos_y_bitacora.pdf). | Comparé cada cita con la transcripción y cada escenario con su frase de origen. Encontré 11 requisitos inventados, tres ambigüedades, dos contradicciones y dos omisiones. |
| 3. Diseño | Generé tres alternativas de arquitectura, una matriz ponderada, diagramas C4 de contexto y contenedores, un modelo de datos y una propuesta de interfaz para la CLI. | Gemini 3.8 Flash. | [Documento de diseño y ADR-001](https://github.com/kenneth0710/asistente-pruebas-pytest/blob/main/docs/modulos/modulo3_diseno.pdf). | Recalculé manualmente los resultados de la matriz y comprobé cada relación, campo y decisión contra las historias de usuario. Corregí los elementos que no tenían fundamento en los requisitos. |
| 4. Código | Implementé HU-07 mediante pruebas primero, implementación y refactor. Realicé una revisión de seguridad, desarrollé pruebas de abuso con un agente delimitado y redacté documentación del código. | ChatGPT. | [Implementación de HU-07](https://github.com/kenneth0710/asistente-pruebas-pytest/commit/9b75801), [integración del agente](https://github.com/kenneth0710/asistente-pruebas-pytest/commit/2b9aedd) y [revisión de seguridad](https://github.com/kenneth0710/asistente-pruebas-pytest/blob/main/revision_seguridad.md). | Introduje errores a propósito, revisé el diff del agente antes de integrarlo, comparé el árbol de sintaxis antes y después de añadir docstrings y ejecuté Ruff y pip-audit. |
| 5. Pruebas | Diseñé casos mediante particiones de equivalencia, valores límite y tabla de decisión. Generé pruebas, datos sintéticos y pruebas de aceptación para los dos escenarios de HU-07. También analicé la cobertura. | ChatGPT. | [Registro de pruebas](https://github.com/kenneth0710/asistente-pruebas-pytest/blob/main/registro_pruebas.md) y [pruebas de aceptación](https://github.com/kenneth0710/asistente-pruebas-pytest/blob/main/tests/test_aceptacion_hu07.py). | Revisé cada resultado esperado contra la regla correspondiente, descarté casos redundantes o débiles y realicé nueve mutaciones manuales. Las pruebas diseñadas desde la regla encontraron el defecto D-01. |
| 6. Operación | Configuré el pipeline de integración continua, el entorno de pruebas con Docker y el plan de monitoreo y mantenimiento. | ChatGPT. | [Pipeline](https://github.com/kenneth0710/asistente-pruebas-pytest/blob/main/.github/workflows/ci.yml), [Dockerfile](https://github.com/kenneth0710/asistente-pruebas-pytest/blob/main/Dockerfile), [revisión de configuración](https://github.com/kenneth0710/asistente-pruebas-pytest/blob/main/docs/revision_configuracion.md) y [plan de operación](https://github.com/kenneth0710/asistente-pruebas-pytest/blob/main/docs/plan_operacion.md). | Ejecuté actionlint y hadolint sin avisos, comprobé la existencia de las etiquetas utilizadas, rompí una prueba deliberadamente para verificar que el pipeline fallara y comprobé su duración de 54 segundos frente al RNF-03. |

En el módulo de fundamentos aprendí a evaluar respuestas mediante ejemplos concretos. El laboratorio de la primera semana mostró que dos modelos pueden producir soluciones diferentes para un mismo problema y que ninguna debe aceptarse únicamente por parecer correcta. Las evidencias de ese laboratorio fueron entregadas en Q10, pero no están publicadas en el repositorio porque las capturas contienen información de cuentas personales.

Durante requisitos y diseño, la verificación consistió principalmente en establecer trazabilidad. Cada requisito debía tener una fuente y cada decisión de arquitectura debía responder a una necesidad identificada. Los elementos que la IA añadió sin respaldo no se trataron como requisitos confirmados.

En construcción y pruebas, la verificación fue más allá de ejecutar la suite. Revisé si los resultados esperados representaban correctamente las reglas y si las pruebas eran capaces de detectar comportamientos incorrectos.

De los 100 casos propuestos durante el diseño de pruebas quedaron 77 después de revisar su utilidad y eliminar casos débiles o redundantes. Posteriormente realicé nueve mutaciones manuales, de las cuales siete fueron detectadas y dos resultaron equivalentes. Estas últimas corresponden a M5 y M6. No considero este resultado una demostración del RNF-08, porque no corresponde al experimento de diez errores sembrados exigido por ese requisito.

La cobertura final fue del 96 % de líneas y del 92,86 % de ramas. Las líneas 58 y 106 de `exclusion.py` quedaron sin cubrir. La primera está relacionada con la ambigüedad A7, que todavía debe resolverse. La segunda corresponde a código muerto, cuyo análisis incluyó una comprobación con 200 000 casos aleatorios.

En operación, además de comprobar que el pipeline funcionaba correctamente, verifiqué que pudiera detectar un fallo. La [ejecución fallida intencionalmente](https://github.com/kenneth0710/asistente-pruebas-pytest/actions/runs/45876043174) registró una prueba fallida y 99 aprobadas. Esta evidencia corresponde a una etapa anterior a la incorporación de las dos pruebas de aceptación.

El detalle de las decisiones, correcciones y resultados de estas actividades se encuentra en el [registro de pruebas](https://github.com/kenneth0710/asistente-pruebas-pytest/blob/main/registro_pruebas.md) y en la [bitácora de uso de IA](https://github.com/kenneth0710/asistente-pruebas-pytest/blob/main/bitacora_ia.md).

## 4. Verificación: lo que la IA hizo mal y cómo lo encontraste

### Caso 1: Requisitos inventados a partir de la entrevista

- **Fase:** Requisitos, módulo 2.
- **Qué propuso la IA:** Gemini generó historias de usuario y escenarios de aceptación a partir de la entrevista. Para la HU-03 estableció que la cantidad de productos debía tener un mínimo de uno y un máximo de cien. También añadió mensajes de error, bloqueos de guardado y otros comportamientos.
- **Qué estaba mal:** El cliente únicamente había indicado que «la cantidad de cada producto debe ser mayor a cero». No había establecido un límite superior ni solicitado varios de los comportamientos propuestos. Incorporarlos como requisitos habría cambiado el alcance del proyecto sin autorización.
- **Cómo lo detecté:** Comparé cada escenario con la transcripción de la entrevista y busqué la frase que justificaba cada condición. Cuando no encontraba una fuente, clasificaba el elemento como una propuesta sin confirmar. Esta revisión permitió identificar 11 requisitos inventados, tres ambigüedades, dos contradicciones y dos omisiones.
- **Qué hice:** Reescribí los escenarios utilizando únicamente hechos respaldados por la entrevista. Trasladé las condiciones sin evidencia a preguntas pendientes y corregí la identificación de actores que no utilizaban directamente el sistema. El resultado se encuentra en el [documento de requisitos del módulo 2](https://github.com/kenneth0710/asistente-pruebas-pytest/blob/main/docs/modulos/modulo2_requisitos_y_bitacora.pdf).

Este caso me permitió comprobar que un criterio de aceptación bien redactado no necesariamente representa una necesidad real. La estructura Gherkin puede ser correcta mientras que su contenido es inventado.

### Caso 2: Errores en la evaluación de arquitecturas y los diagramas

- **Fase:** Diseño, módulo 3.
- **Qué propuso la IA:** Gemini presentó tres alternativas de arquitectura, una matriz ponderada para compararlas, un análisis de sensibilidad y diagramas C4. Los resultados que presentó para las tres alternativas fueron 138, 130 y 98.
- **Qué estaba mal:** Los valores no correspondían a la suma de sus propios componentes. Los resultados correctos eran 140, 132 y 103. Además, el análisis de sensibilidad utilizó un peso de nueve, aunque la escala definida era de uno a cinco. En los diagramas apareció una relación según la cual el asistente reportaba el estado de CI, sin que existiera un requisito que respaldara ese comportamiento. También se omitió GitHub Actions como sistema externo.
- **Cómo lo detecté:** Recalculé manualmente cada resultado de la matriz y revisé que los pesos respetaran la escala definida. Después comparé las relaciones de los diagramas con las historias de usuario y revisé que los componentes representaran responsabilidades justificadas.
- **Qué hice:** Corregí los resultados de la matriz, eliminé las relaciones inventadas y ajusté los elementos del diseño que no coincidían con los requisitos. Mantuve la alternativa A, correspondiente a una CLI en Python, un plugin de pytest y GitHub Actions. La decisión quedó registrada en el ADR-001, incluido en el [documento de diseño del módulo 3](https://github.com/kenneth0710/asistente-pruebas-pytest/blob/main/docs/modulos/modulo3_diseno.pdf).

La decisión de arquitectura no dependió únicamente de la recomendación de Gemini. Revisé los datos utilizados para justificarla antes de incorporarla al proyecto.

### Caso 3: Una prueba correcta respecto a un contrato equivocado

- **Fase:** Código y definición del contrato, semana 5.
- **Qué propuso la IA:** ChatGPT escribió una prueba que esperaba que el archivo `.ENV` fuera permitido cuando el patrón de exclusión era `.env`.
- **Qué estaba mal:** En sistemas de archivos que no distinguen mayúsculas y minúsculas, habituales en Windows y macOS, ambas rutas pueden representar el mismo archivo. El comportamiento esperado por la prueba permitía que las claves quedaran expuestas, contradiciendo el RNF-06. Sin embargo, la prueba sí cumplía el contrato que yo había proporcionado. El defecto estaba inicialmente en la definición de la regla.
- **Cómo lo detecté:** Revisé el resultado esperado de la prueba y lo comparé con el requisito de enviar cero archivos excluidos. Después introduje deliberadamente un error eliminando `.lower()` de la implementación corregida. Solo la prueba nueva falló, demostrando que era capaz de detectar esa modificación.
- **Qué hice:** Modifiqué el contrato para que la comparación no distinguiera mayúsculas y minúsculas, corregí la prueba y verifiqué el comportamiento. El cambio quedó registrado en el [commit 4afca43](https://github.com/kenneth0710/asistente-pruebas-pytest/commit/4afca43) y en la entrada 2 de la [bitácora de IA](https://github.com/kenneth0710/asistente-pruebas-pytest/blob/main/bitacora_ia.md).

Este caso fue importante porque el error no se encontraba inicialmente en una implementación defectuosa, sino en una condición que yo había permitido. Una prueba aprobada puede confirmar que el programa cumple una regla y, al mismo tiempo, esa regla puede incumplir un requisito de seguridad.

### Caso 4: Defecto D-01 que las pruebas anteriores no detectaban

- **Fase:** Código y pruebas, semanas 6 y 7.
- **Qué propuso la IA:** Durante la revisión de seguridad, ChatGPT modificó la normalización de rutas para manejar diferentes formas de evasión del filtro, incluidos los componentes `..`. También propuso pruebas para comprobar ese comportamiento.
- **Qué estaba mal:** La operación `rstrip(" .")` se ejecutaba antes de comprobar si el componente era `..`. Como consecuencia, los dos puntos se convertían en una cadena vacía antes de que el programa pudiera resolver correctamente ese componente. Las pruebas anteriores utilizaban rutas como `x/../datos/...`, cuyo archivo podía quedar excluido igualmente por el final de la ruta. Por tanto, esas pruebas podían aprobarse sin demostrar que la normalización funcionaba correctamente.
- **Cómo lo detecté:** En la semana 7 diseñé las pruebas tomando como punto de partida las reglas del contrato, en lugar de copiar el comportamiento de la implementación. Al ejecutarlas aparecieron ocho fallos que permitieron identificar el defecto D-01. Conservé la evidencia de las pruebas en rojo en el [commit 3361726](https://github.com/kenneth0710/asistente-pruebas-pytest/commit/3361726).
- **Qué hice:** ChatGPT corrigió el orden de las operaciones, colocando la comprobación de `..` antes de `rstrip(" .")`, sin modificar las pruebas que habían encontrado el defecto. La corrección quedó registrada en el [commit 3238135](https://github.com/kenneth0710/asistente-pruebas-pytest/commit/3238135). El análisis de los casos y las mutaciones está documentado en el [registro de pruebas](https://github.com/kenneth0710/asistente-pruebas-pytest/blob/main/registro_pruebas.md).

La solución de la semana 6 había permanecido con pruebas exitosas durante una semana. El defecto apareció cuando evalué la regla de manera independiente del código que debía cumplirla.

### Caso 5: Etiqueta de Docker inventada y validación incorrecta de un criterio de aceptación

- **Fase:** Operación y cierre del proyecto.
- **Qué propuso la IA:** ChatGPT configuró la imagen Docker con la etiqueta `asistente-pruebas:1.0.0`. En las pruebas de aceptación también propuso comparar el mensaje de la excepción del segundo escenario de HU-07 con el texto exacto de la implementación.
- **Qué estaba mal:** La versión real del proyecto era `0.1.0`, según `pyproject.toml`. La etiqueta `1.0.0` no tenía una fuente dentro del proyecto. Por otra parte, el criterio de aceptación exigía avisar que el archivo estaba excluido, pero no establecía una redacción exacta del mensaje. La prueba introducía una condición que no pertenecía al requisito.
- **Cómo lo detecté:** Comparé la etiqueta propuesta con la versión declarada en `pyproject.toml`. En la prueba de aceptación comparé la comprobación del mensaje con el escenario original, en lugar de utilizar la implementación como fuente del resultado esperado.
- **Qué hice:** Solicité que la etiqueta coincidiera con la versión del proyecto y que la prueba verificara el significado del aviso sin depender de una redacción exacta. Los cambios están registrados en los [commits d177c2f](https://github.com/kenneth0710/asistente-pruebas-pytest/commit/d177c2f) y [386a3db](https://github.com/kenneth0710/asistente-pruebas-pytest/commit/386a3db). Las verificaciones de configuración se encuentran en [revision_configuracion.md](https://github.com/kenneth0710/asistente-pruebas-pytest/blob/main/docs/revision_configuracion.md).

Estos errores no impedían necesariamente que el pipeline terminara correctamente. Fue necesario comparar las propuestas con los documentos y archivos que establecían las condiciones reales del proyecto.

## 5. Estado final del sistema

- **Arquitectura:** La arquitectura seleccionada mediante el ADR-001 consiste en una CLI desarrollada en Python, un plugin de pytest y GitHub Actions. La decisión está documentada en el [diseño del módulo 3](https://github.com/kenneth0710/asistente-pruebas-pytest/blob/main/docs/modulos/modulo3_diseno.pdf). Actualmente existe la librería que implementa el filtro de exclusión y el pipeline de integración continua del repositorio. La CLI y el plugin todavía no están implementados.

- **Funcionalidades terminadas (historias Must y su estado):** De las seis historias clasificadas como Must, implementé únicamente HU-07 al nivel de la librería.
  - HU-01: pendiente.
  - HU-02: pendiente.
  - HU-03: pendiente.
  - HU-04: pendiente.
  - HU-07: terminada al nivel de la librería, con pruebas de exclusión, normalización de rutas, intentos de evasión y aceptación de sus dos escenarios.
  - HU-10: pendiente.

  La implementación de HU-07 se encuentra en [asistente/exclusion.py](https://github.com/kenneth0710/asistente-pruebas-pytest/blob/main/asistente/exclusion.py). El pipeline actual verifica la calidad del propio asistente y no representa la implementación de HU-10. Tampoco existe todavía una comunicación con Gemini que permita comprobar la protección de datos durante una transmisión real.

- **Pruebas:** El proyecto cuenta con 102 pruebas aprobadas, una cobertura del 96 % de líneas y del 92,86 % de ramas. Incluye dos pruebas de aceptación de HU-07, una por cada escenario. El pipeline realiza el análisis estático con Ruff, ejecuta las pruebas con cobertura, audita las dependencias con pip-audit y posteriormente construye un contenedor Docker donde vuelve a ejecutar las pruebas con un usuario sin privilegios. La duración reportada del pipeline completo es de 54 segundos, inferior al límite de cinco minutos establecido por RNF-03. Todas las ejecuciones de la rama `main` están en verde. Los resultados pueden consultarse en [GitHub Actions](https://github.com/kenneth0710/asistente-pruebas-pytest/actions).

- **Pendientes:**
  - Implementar la CLI, el plugin de pytest y la integración con Gemini.
  - Completar las historias Must restantes: HU-01, HU-02, HU-03, HU-04 y HU-10.
  - Resolver las ambigüedades A6 y A7 con el docente, relacionadas con la normalización de rutas y el caso `.. ` con espacio final, identificado como P-05.
  - Realizar el refactor P-06 para eliminar la lógica duplicada de las líneas 105 y 106 de `exclusion.py`, una vez revisado su comportamiento.
  - Demostrar el RNF-08 mediante el experimento de diez errores sembrados, de los cuales las pruebas deben detectar al menos ocho. Las nueve mutaciones manuales realizadas no sustituyen este experimento.
  - Incorporar Dependabot y el escaneo de vulnerabilidades de la imagen Docker, actualmente definidos como propuestas de mantenimiento.

Los pendientes técnicos están documentados en el [registro de pruebas](https://github.com/kenneth0710/asistente-pruebas-pytest/blob/main/registro_pruebas.md) y en el [plan de operación](https://github.com/kenneth0710/asistente-pruebas-pytest/blob/main/docs/plan_operacion.md).

## 6. Reflexión ética y legal

| Principio | Decisión en mi proyecto | Evidencia |
|---|---|---|
| Datos personales (Ley 1581 de 2012) | Implementé HU-07 como mecanismo de exclusión de archivos sensibles antes de una futura comunicación con una IA externa. Utilicé datos sintéticos en las pruebas, obtuve autorización escrita para utilizar la entrevista con IA y omití el nombre del cliente simulado. No publiqué las capturas del laboratorio que mostraban cuentas personales. El plan de operación establece que los registros no deben contener datos personales ni credenciales. | [Filtro de exclusión](https://github.com/kenneth0710/asistente-pruebas-pytest/blob/main/asistente/exclusion.py), [registro de pruebas, sección 4](https://github.com/kenneth0710/asistente-pruebas-pytest/blob/main/registro_pruebas.md), [requisitos y entrevista](https://github.com/kenneth0710/asistente-pruebas-pytest/blob/main/docs/modulos/modulo2_requisitos_y_bitacora.pdf) y [plan de operación](https://github.com/kenneth0710/asistente-pruebas-pytest/blob/main/docs/plan_operacion.md). |
| Sesgo | El contrato inicial que definí y la prueba propuesta por la IA asumían un comportamiento habitual de Linux respecto a las mayúsculas y minúsculas. Ni yo ni la IA cuestionamos ese supuesto hasta revisar la prueba contra el RNF-06. Corregí el contrato para evitar diferencias en la protección de archivos. Además, utilicé datos sintéticos con nombres que incluyen tildes, ñ y apóstrofos, y referencias a barrios de Neiva, evitando limitar las pruebas a datos en ASCII. | [Corrección del contrato](https://github.com/kenneth0710/asistente-pruebas-pytest/commit/4afca43) y [pruebas con datos sintéticos](https://github.com/kenneth0710/asistente-pruebas-pytest/blob/main/tests/test_s7_datos_sinteticos.py). |
| Transparencia | Documenté el uso de IA en una bitácora de 26 entradas: diez aceptadas, doce aceptadas con cambios y cuatro rechazadas. Conservé los prompts y declaré el uso de IA en los documentos. También utilicé Claude Code como agente para operar el navegador y el repositorio, ejecutar verificaciones y redactar documentación. Las decisiones y la aprobación de cada entrega fueron mías. ChatGPT redactó este informe a partir de los datos que le entregué, y yo lo revisé. | [Bitácora de IA](https://github.com/kenneth0710/asistente-pruebas-pytest/blob/main/bitacora_ia.md), [prompts](https://github.com/kenneth0710/asistente-pruebas-pytest/tree/main/docs/prompts) y [documentos de los módulos](https://github.com/kenneth0710/asistente-pruebas-pytest/tree/main/docs/modulos). |
| Responsabilidad | Conservé la responsabilidad sobre las decisiones, los contratos y la aceptación o rechazo de cada propuesta. El agente de la semana 6 trabajó en una rama separada y solo integré sus cambios después de revisar el diff. Las ambigüedades A6 y A7 quedaron pendientes de una decisión humana, en lugar de permitir que la IA estableciera nuevas reglas sin autorización. | [Integración del agente](https://github.com/kenneth0710/asistente-pruebas-pytest/commit/2b9aedd), [bitácora de IA](https://github.com/kenneth0710/asistente-pruebas-pytest/blob/main/bitacora_ia.md) y [registro de pruebas](https://github.com/kenneth0710/asistente-pruebas-pytest/blob/main/registro_pruebas.md). |
| Propiedad intelectual y política de uso | Utilicé la licencia MIT para el repositorio y herramientas de código abierto: pytest, Ruff y pytest-cov con licencia MIT, y pip-audit con Apache-2.0. Identifiqué el código generado con apoyo de IA mediante la bitácora y los commits. No envié claves ni datos reales a las herramientas de inteligencia artificial. | [Licencia del proyecto](https://github.com/kenneth0710/asistente-pruebas-pytest/blob/main/LICENSE), [dependencias](https://github.com/kenneth0710/asistente-pruebas-pytest/blob/main/requirements-dev.txt) y [bitácora de IA](https://github.com/kenneth0710/asistente-pruebas-pytest/blob/main/bitacora_ia.md). |

El dilema ético más importante fue que utilizar una IA externa para analizar código requiere compartir información del proyecto, mientras que el repositorio contiene claves y datos de aproximadamente 300 clientes. No era suficiente confiar en que los desarrolladores recordarían qué archivos podían compartir. Por esta razón establecí la HU-07 como una historia Must y decidí implementarla antes de desarrollar la comunicación con Gemini. Diseñé pruebas de abuso y adopté el criterio de excluir de más cuando existiera una duda relacionada con la protección de los archivos, dando prioridad al RNF-06. La implementación actual permite verificar el filtro de selección, pero no demuestra todavía la seguridad de una transmisión real. Esa comprobación deberá realizarse cuando exista la integración con la API.

## 7. Aprendizajes

Durante la semana 5 aprendí que una prueba en verde no demuestra necesariamente que la prueba esté bien diseñada. El error que más me enseñó no fue detectado inicialmente por una prueba, sino que estaba dentro de ella. La IA había seguido el contrato que yo le proporcioné, pero ese contrato contradecía un requisito no funcional. Ahora sé que debo revisar las reglas contra los RNF antes de solicitar pruebas y que introducir errores a propósito desde el principio permite comprobar si las pruebas realmente detectan incumplimientos.

En la semana 6 utilicé la inteligencia artificial como segunda revisora de seguridad. Fue útil para revisar la implementación, pero no identificó inicialmente las formas de evasión relacionadas con Windows. También aprendí que el mensaje «10 passed» del agente no era evidencia suficiente para confiar en sus cambios. La confianza surgió después de revisar el diff y comprobar cómo funcionaba cada modificación. Si volviera a realizar esta actividad, escribiría las pruebas de abuso directamente desde el contrato, antes de solicitar las correcciones.

En la semana 7 comprobé la importancia de escribir la regla antes de evaluar el código. Las pruebas diseñadas desde las reglas encontraron en minutos un defecto que había permanecido oculto durante una semana. También aprendí que generar muchos casos no equivale a tener una suite de calidad: la IA propuso 100 casos y fue necesario decidir cuáles eran redundantes o débiles. Esa decisión fue parte de mi trabajo. Las mutaciones manuales me permitieron comprobar aspectos de la efectividad de las pruebas que el porcentaje de cobertura por sí solo no mostraba.

Durante el cierre del proyecto, siete de nueve respuestas necesitaron cambios. Los errores tenían en común que incluían condiciones o valores que no provenían de la fuente correspondiente: una etiqueta de Docker inventada, un mensaje copiado de la implementación y una regla que no estaba explícitamente establecida. Encontré estos problemas comparando las respuestas con los archivos y documentos que definían el comportamiento esperado.

En un proyecto futuro revisaría primero la fuente de cada requisito, establecería el contrato antes de generar las pruebas e introduciría errores deliberados desde las primeras etapas. También mantendría la revisión individual de las propuestas de IA, en lugar de utilizar únicamente los resultados exitosos de las herramientas como criterio de aceptación.

Estos aprendizajes están respaldados por las actividades y decisiones registradas en la [bitácora de uso de IA](https://github.com/kenneth0710/asistente-pruebas-pytest/blob/main/bitacora_ia.md), la [revisión de seguridad](https://github.com/kenneth0710/asistente-pruebas-pytest/blob/main/revision_seguridad.md) y el [registro de pruebas](https://github.com/kenneth0710/asistente-pruebas-pytest/blob/main/registro_pruebas.md).

## 8. Anexos

### Bitácora de uso de IA

La bitácora contiene 26 entradas que documentan las propuestas realizadas por la IA, su verificación y las decisiones de aceptación, modificación o rechazo.

| Resultado de la revisión | Cantidad |
|---|---:|
| Aceptadas | 10 |
| Aceptadas con cambios | 12 |
| Rechazadas | 4 |
| Total | 26 |

- [Bitácora completa de uso de IA](https://github.com/kenneth0710/asistente-pruebas-pytest/blob/main/bitacora_ia.md).
- [Carpeta de prompts utilizados](https://github.com/kenneth0710/asistente-pruebas-pytest/tree/main/docs/prompts).

### Documentos de cada módulo

| Módulo | Documento o evidencia |
|---|---|
| 1. Fundamentos | [Banco de prompts](https://github.com/kenneth0710/asistente-pruebas-pytest/blob/main/docs/modulos/modulo1_banco_de_prompts.pdf). |
| 1. Fundamentos | [Propuesta del proyecto](https://github.com/kenneth0710/asistente-pruebas-pytest/blob/main/docs/modulos/modulo1_propuesta.pdf). |
| 2. Requisitos | [Requisitos y bitácora](https://github.com/kenneth0710/asistente-pruebas-pytest/blob/main/docs/modulos/modulo2_requisitos_y_bitacora.pdf). |
| 3. Diseño | [Documento de diseño y ADR-001](https://github.com/kenneth0710/asistente-pruebas-pytest/blob/main/docs/modulos/modulo3_diseno.pdf). |
| 4. Código | [Implementación de HU-07](https://github.com/kenneth0710/asistente-pruebas-pytest/blob/main/asistente/exclusion.py). |
| 4. Código | [Revisión de seguridad](https://github.com/kenneth0710/asistente-pruebas-pytest/blob/main/revision_seguridad.md). |
| 5. Pruebas | [Registro de pruebas](https://github.com/kenneth0710/asistente-pruebas-pytest/blob/main/registro_pruebas.md). |
| 5. Pruebas | [Pruebas de aceptación de HU-07](https://github.com/kenneth0710/asistente-pruebas-pytest/blob/main/tests/test_aceptacion_hu07.py). |
| 6. Operación | [Pipeline de integración continua](https://github.com/kenneth0710/asistente-pruebas-pytest/blob/main/.github/workflows/ci.yml). |
| 6. Operación | [Dockerfile](https://github.com/kenneth0710/asistente-pruebas-pytest/blob/main/Dockerfile). |
| 6. Operación | [Configuración de exclusión de Docker](https://github.com/kenneth0710/asistente-pruebas-pytest/blob/main/.dockerignore). |
| 6. Operación | [Revisión de configuración](https://github.com/kenneth0710/asistente-pruebas-pytest/blob/main/docs/revision_configuracion.md). |
| 6. Operación | [Plan de operación y mantenimiento](https://github.com/kenneth0710/asistente-pruebas-pytest/blob/main/docs/plan_operacion.md). |

### Evidencias de verificación

| Evidencia | Enlace |
|---|---|
| Implementación inicial de HU-07 | [Commit 9b75801](https://github.com/kenneth0710/asistente-pruebas-pytest/commit/9b75801). |
| Corrección del contrato de mayúsculas y minúsculas | [Commit 4afca43](https://github.com/kenneth0710/asistente-pruebas-pytest/commit/4afca43). |
| Integración revisada del agente de pruebas de abuso | [Commit 2b9aedd](https://github.com/kenneth0710/asistente-pruebas-pytest/commit/2b9aedd). |
| Evidencia de pruebas fallidas por D-01 | [Commit 3361726](https://github.com/kenneth0710/asistente-pruebas-pytest/commit/3361726). |
| Corrección del defecto D-01 | [Commit 3238135](https://github.com/kenneth0710/asistente-pruebas-pytest/commit/3238135). |
| Correcciones relacionadas con las pruebas de aceptación y la etiqueta de Docker | [Commit d177c2f](https://github.com/kenneth0710/asistente-pruebas-pytest/commit/d177c2f) y [commit 386a3db](https://github.com/kenneth0710/asistente-pruebas-pytest/commit/386a3db). |
| Pipeline con una prueba rota intencionalmente | [Ejecución 45876043174](https://github.com/kenneth0710/asistente-pruebas-pytest/actions/runs/45876043174). |
| Historial de ejecuciones y resultados actuales | [GitHub Actions](https://github.com/kenneth0710/asistente-pruebas-pytest/actions). |

### Repositorio y documentación general

- [Repositorio del proyecto](https://github.com/kenneth0710/asistente-pruebas-pytest).
- [README del proyecto](https://github.com/kenneth0710/asistente-pruebas-pytest/blob/main/README.md).
- [Índice de documentos de los módulos](https://github.com/kenneth0710/asistente-pruebas-pytest/blob/main/docs/modulos/README.md).
- [Licencia MIT](https://github.com/kenneth0710/asistente-pruebas-pytest/blob/main/LICENSE).

La transcripción completa de la entrevista y las capturas del laboratorio de la primera semana no se incluyen entre los anexos públicos por motivos de privacidad.
