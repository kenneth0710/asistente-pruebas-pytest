# Plan de operación, monitoreo y mantenimiento

## 1. Registro de eventos y protección de datos

El objetivo del registro de eventos es facilitar la detección de errores, verificar el cumplimiento de los requisitos no funcionales y permitir el seguimiento de incidentes sin comprometer información sensible.

Actualmente, el proyecto dispone de los registros de ejecución de GitHub Actions, los resultados de pytest, los informes de cobertura y los resultados de Ruff y pip-audit. No existe un sistema de registro de eventos de la aplicación porque la CLI todavía no está implementada.

### 1.1. Información que se registra

| Información | Finalidad | Estado |
|---|---|---|
| Fecha y duración del pipeline | Verificar el RNF-03. | Existente |
| Cantidad de pruebas exitosas y fallidas | Detectar regresiones. | Existente |
| Cobertura de líneas y ramas | Identificar código sin ejecutar. | Existente |
| Infracciones detectadas por Ruff | Controlar la calidad del código. | Existente |
| Vulnerabilidades detectadas por pip-audit | Identificar riesgos en dependencias. | Existente |
| Resultado de construcción y ejecución de Docker | Verificar el entorno de pruebas. | Existente |
| Duración de la suite local | Verificar el RNF-02. | Propuesta de seguimiento |
| Identificador anónimo de solicitud | Relacionar eventos de una operación. | Propuesta para la CLI |
| Identificador y versión disponible del modelo de IA | Facilitar la trazabilidad de los resultados. | Propuesta para la CLI |
| Cantidad de solicitudes a Gemini | Controlar el consumo de la API. | Propuesta para la CLI |
| Cantidad de archivos permitidos y bloqueados | Supervisar el filtro de exclusión. | Propuesta para la CLI |
| Código de estado y duración de solicitudes a Gemini | Detectar errores y problemas de rendimiento. | Propuesta para la CLI |

### 1.2. Información que nunca debe registrarse

Teniendo en cuenta los principios de finalidad, acceso restringido, seguridad y confidencialidad de la Ley 1581 de 2012 de Colombia, el proyecto evitará registrar información personal o sensible que no sea necesaria para su operación.

No se debe registrar:

- Claves de API, incluida GEMINI_API_KEY.
- Contenido de archivos .env.
- Nombres, identificaciones, teléfonos, direcciones o correos de clientes reales.
- Contenido de clientes_panaderia.csv y pedidos.db.
- Contenido de archivos incluidos en la lista de exclusión.
- Prompts y respuestas completas de Gemini en los registros operativos.
- Fragmentos de código que puedan contener credenciales o información personal.
- Rutas absolutas que revelen nombres de usuarios del sistema operativo.
- Encabezados de autorización de las solicitudes HTTP.

Los registros de la futura CLI deberán utilizar únicamente metadatos necesarios para diagnosticar su funcionamiento.

Ejemplo sintético de un registro propuesto para la futura CLI:

```json
{
  "nivel": "INFO",
  "evento": "seleccion_archivos",
  "solicitud_id": "sintetica-001",
  "archivos_permitidos": 2,
  "archivos_bloqueados": 3,
  "estado": "completado"
}
```

Este ejemplo es ilustrativo. No corresponde a una ejecución real ni a una funcionalidad implementada.

Como medida inicial, se propone conservar los registros locales de la futura CLI durante un máximo de 30 días. Este plazo es un supuesto operativo revisable por el equipo, no una exigencia específica de la Ley 1581 de 2012.

Referencia normativa: [Ley 1581 de 2012](https://www.funcionpublica.gov.co/eva/gestornormativo/norma.php?i=49981).

## 2. Métricas y alertas

El monitoreo se organiza mediante las cuatro señales doradas de la ingeniería de confiabilidad: latencia, tráfico, errores y saturación.

Debido a que el proyecto no dispone de un servidor, estas señales se aplican al pipeline, la ejecución de pruebas y, cuando exista, al consumo de la API externa de Gemini.

### 2.1. Latencia

Mide el tiempo necesario para completar una operación.

| Métrica | Umbral | Origen del umbral | Cuándo se activa la alerta |
|---|---|---|---|
| Duración de la suite local | Máximo 120 segundos | RNF-02 | Una ejecución supera los 120 segundos. |
| Duración total del pipeline por pull request | Menos de 300 segundos | RNF-03 | Una ejecución alcanza o supera los 300 segundos. |
| Tiempo de respuesta de Gemini | Máximo 60 segundos | Supuesto operativo | Una solicitud supera el tiempo establecido. |

**Estado actual:** la duración del pipeline es observable desde GitHub Actions. La última ejecución reportada tuvo una duración total de 54 segundos, por debajo del límite de 300 segundos.

El 2026-11-26 se midió la duración de la suite local en el equipo de desarrollo (Windows 11, Intel Core i5-12450H, 16 GB de RAM y Python 3.12.10). Se ejecutó el comando python -m pytest tests/ -q tres veces consecutivas, obteniendo en cada ejecución 102 pruebas aprobadas, una duración de 0,12 segundos según pytest y un tiempo total del comando de 0,58 segundos. Las tres ejecuciones cumplen el límite de 120 segundos establecido por RNF-02.

El tiempo de respuesta de Gemini solamente podrá medirse después de implementar la CLI.

### 2.2. Tráfico

Mide la cantidad de operaciones realizadas durante un periodo determinado.

| Métrica | Umbral | Origen del umbral | Cuándo se activa la alerta |
|---|---|---|---|
| Ejecuciones del pipeline por pull request | Al menos una ejecución asociada a su apertura o última actualización de código | Supuesto operativo, política de integración continua | Un pull request no dispone de una ejecución correspondiente a sus cambios. |
| Solicitudes a Gemini | Alcanzar el 80 % de la cuota de solicitudes aplicable | Supuesto operativo | La cantidad de solicitudes alcanza el 80 % de la cuota del modelo utilizado, dentro de su periodo correspondiente. |

**Estado actual:** GitHub Actions permite consultar las ejecuciones asociadas a los cambios del repositorio.

**Propuesta para la CLI:** registrar el número de solicitudes realizadas a Gemini, sin almacenar su contenido. Los límites reales deberán consultarse en la documentación oficial del modelo utilizado, ya que pueden cambiar.

No se establece un número fijo de solicitudes por minuto o por día porque todavía no existe una integración que permita conocer el consumo real ni el modelo definitivo.

### 2.3. Errores

Mide las operaciones fallidas y los incumplimientos de los requisitos de calidad y seguridad.

| Métrica | Umbral | Origen del umbral | Cuándo se activa la alerta |
|---|---|---|---|
| Pruebas automatizadas fallidas | 0 | Política de calidad propuesta | Falla una o más pruebas. |
| Infracciones de Ruff | 0 | Política de calidad existente en CI | Ruff devuelve un código de salida de error. |
| Vulnerabilidades conocidas detectadas | 0 | Política de seguridad existente en CI | pip-audit detecta una vulnerabilidad. |
| Archivos excluidos enviados a Gemini | 0 | RNF-06 | Se detecta un intento efectivo de transmitir un archivo excluido. |
| Pruebas generadas con datos inventados | 100 % | RNF-07 | Se identifica una prueba generada que utiliza datos reales. |
| Errores sembrados detectados | Mínimo 8 de 10 | RNF-08 | Las pruebas detectan menos de 8 de los 10 errores sembrados. |
| Errores de comunicación con Gemini | 3 fallos consecutivos | Supuesto operativo | Tres solicitudes consecutivas fallan. |

**Estado actual:** el pipeline ejecuta 102 pruebas, analiza el código con Ruff y audita las dependencias con pip-audit. Un fallo en cualquiera de estos controles impide que el pipeline termine exitosamente.

Las pruebas de HU-07 verifican la selección de archivos permitidos y el rechazo de archivos excluidos. Sin embargo, todavía no demuestran el cumplimiento de RNF-06 durante una transmisión real porque la integración con Gemini no existe.

El RNF-07 requiere revisión humana de los datos utilizados en las pruebas. El RNF-08 requiere un experimento documentado con diez errores sembrados. No debe considerarse cumplido únicamente por obtener una cobertura elevada o por disponer de pruebas exitosas.

### 2.4. Saturación

Mide qué tan cerca están los recursos disponibles de alcanzar su capacidad máxima.

| Métrica | Umbral | Origen del umbral | Cuándo se activa la alerta |
|---|---|---|---|
| Memoria disponible durante las pruebas locales | Uso superior al 85 % durante 30 segundos consecutivos | Supuesto operativo | El consumo sostenido supera el límite establecido. |
| Cuota de tokens de Gemini | Alcanzar el 80 % de la cuota aplicable | Supuesto operativo | El consumo se aproxima al límite del periodo correspondiente. |
| Cuota gratuita de GitHub Actions, cuando resulte aplicable | Alcanzar el 80 % de la cuota disponible | Supuesto operativo | El consumo se aproxima al límite gratuito de la cuenta. |

**Estado actual:** no existe monitoreo automatizado de saturación.

El equipo puede consultar el consumo de memoria mediante las herramientas del sistema operativo y revisar los límites aplicables en GitHub.

**Propuesta para la CLI:** controlar el consumo de tokens y las cuotas de Gemini. Si se alcanza el límite disponible, la CLI deberá informar al desarrollador y evitar reintentos ilimitados.

### 2.5. Gestión de alertas

No se requiere contratar servicios externos de monitoreo.

| Herramienta | Uso | Estado |
|---|---|---|
| GitHub Actions | Consultar fallos, tiempos y resultados del pipeline. | Existente |
| Notificaciones de GitHub | Informar sobre ejecuciones fallidas según la configuración de cada integrante. | Propuesta de configuración |
| GitHub Issues | Registrar incidentes y tareas correctivas sin información sensible. | Propuesta |
| Administrador de tareas del sistema operativo | Consultar memoria y recursos locales. | Propuesta |
| Módulo logging de Python | Registrar eventos operativos de la futura CLI. | Propuesta |
| Panel de consumo de Gemini | Consultar las cuotas gratuitas disponibles. | Propuesta para la CLI |

Las alertas basadas en tiempos, saturación y consumo de API son políticas propuestas. No se afirma que actualmente existan mecanismos automáticos que las generen.

Los umbrales definidos como supuestos deberán revisarse cuando existan mediciones suficientes.

## 3. Gestión de incidentes

Un incidente es cualquier evento que afecte la seguridad, la disponibilidad del entorno de desarrollo, la calidad de las pruebas o el cumplimiento de los requisitos establecidos.

### 3.1. Clasificación de incidentes

| Prioridad | Ejemplo | Acción inicial |
|---|---|---|
| Crítica | Exposición de una clave de API o transmisión de un archivo excluido. | Detener la operación y contener la exposición. |
| Alta | Pruebas fallidas, vulnerabilidad conocida o regresión del filtro de exclusión. | Bloquear la integración del cambio y revisar la causa. |
| Media | Incumplimiento de los tiempos máximos establecidos en los RNF. | Analizar los registros y corregir el problema de rendimiento. |
| Baja | Error de documentación o mejora operativa pendiente. | Registrar y programar la corrección. |

Esta clasificación es una propuesta organizativa para el equipo de cinco estudiantes.

### 3.2. Procedimiento de atención

1. **Detectar:** identificar el incidente mediante los resultados del pipeline, las pruebas, una revisión humana o, en el futuro, los registros de la CLI.
2. **Registrar:** crear un incidente con su descripción, impacto y evidencia, sin incluir secretos ni datos personales.
3. **Asignar:** seleccionar un integrante responsable de coordinar la solución.
4. **Contener:** detener la operación afectada, evitar integraciones defectuosas o deshabilitar temporalmente la funcionalidad comprometida.
5. **Investigar:** revisar cambios recientes, resultados de pruebas y registros disponibles.
6. **Corregir:** implementar una solución en una rama separada.
7. **Verificar:** ejecutar las pruebas, Ruff, pip-audit y Docker mediante el pipeline.
8. **Recuperar:** integrar la corrección únicamente después de comprobar su funcionamiento.
9. **Documentar:** registrar la causa, las acciones realizadas y las medidas preventivas.
10. **Cerrar:** confirmar que el incidente fue resuelto y que las acciones pendientes tienen responsables asignados.

### 3.3. Incidentes relacionados con información sensible

Si se detecta la exposición de GEMINI_API_KEY, se deberá revocar la clave desde la plataforma de Google, generar una nueva, revisar el alcance de la exposición y evitar que vuelva a incorporarse al repositorio.

Eliminar una clave de un archivo o commit no garantiza que deje de estar comprometida.

Si en el futuro se detecta el envío de archivos excluidos, se deberá detener inmediatamente la comunicación con Gemini, identificar el alcance sin reproducir los datos sensibles y corregir el filtro antes de reactivar la funcionalidad.

Si existe información personal comprometida, el equipo deberá informar al responsable del tratamiento de los datos y evaluar las obligaciones legales aplicables.

Actualmente no existe una integración con Gemini que permita observar incidentes de transmisión desde la CLI.

### 3.4. Plantilla de análisis de incidentes sin culpables

El análisis debe centrarse en las causas técnicas y organizativas, no en señalar a las personas que participaron en el incidente.

```markdown
# Análisis de incidente

- Identificador:
- Fecha de detección:
- Fecha de resolución:
- Prioridad:
- Responsable de seguimiento:
- Estado:

## Resumen

¿Qué ocurrió?

## Impacto

¿Qué funcionalidades, requisitos o procesos fueron afectados?

## Línea de tiempo

- Hora de detección:
- Hora de contención:
- Hora de corrección:
- Hora de verificación:

## Causa raíz

¿Qué condiciones técnicas o del proceso permitieron el incidente?

## Factores contribuyentes

¿Qué controles faltaron o no funcionaron?

## Acciones de contención y recuperación

¿Qué se hizo para reducir el impacto y recuperar la operación?

## Evidencias de verificación

- Enlace al commit:
- Enlace al pipeline:
- Pruebas ejecutadas:
- Resultado obtenido:

## Acciones preventivas

| Acción | Responsable | Fecha límite | Estado |
|--------|-------------|--------------|--------|
|        |             |              |        |

## Lecciones aprendidas

¿Qué cambios deben realizarse para evitar incidentes similares?
```

Los incidentes que contengan información sensible no deberán documentarse íntegramente en el repositorio público.

## 4. Mantenimiento de dependencias y vulnerabilidades

El paquete asistente utiliza exclusivamente la librería estándar de Python. Las herramientas de desarrollo están fijadas en requirements-dev.txt.

Las dependencias declaradas actualmente son:

| Dependencia | Versión | Finalidad |
|---|---|---|
| pytest | 9.2.0 | Ejecución de pruebas. |
| ruff | 0.17.5 | Análisis estático de código. |
| pip-audit | 2.10.1 | Detección de vulnerabilidades conocidas. |
| pytest-cov | 7.1.0 | Medición de cobertura. |

### 4.1. Controles existentes

El pipeline ejecuta la auditoría mediante:

```bash
python -m pip_audit -r requirements-dev.txt
```

Si pip-audit detecta vulnerabilidades conocidas y devuelve un código de error, el pipeline falla.

El Dockerfile utiliza una imagen oficial de Python con una versión específica:

```dockerfile
FROM python:3.12.12-slim-bookworm
```

La auditoría de dependencias de Python no equivale a una auditoría completa de los paquetes del sistema operativo incluidos en la imagen Docker.

### 4.2. Mantenimiento propuesto

| Actividad | Frecuencia propuesta |
|---|---|
| Ejecutar pip-audit | En cada ejecución del trabajo ci que alcance este paso. |
| Revisar nuevas versiones de dependencias | Semanalmente. |
| Revisar actualizaciones de seguridad de Python e imagen base | Semanalmente. |
| Revisar versiones de las acciones de GitHub | Mensualmente. |
| Atender vulnerabilidades críticas conocidas | Inmediatamente después de su detección. |
| Revisar dependencias innecesarias | Mensualmente. |

Las frecuencias son propuestas organizativas, no resultados medidos ni requisitos establecidos por los RNF.

Se propone utilizar Dependabot, disponible gratuitamente en GitHub, para recibir propuestas de actualización de dependencias, acciones e imágenes base. Su activación queda pendiente.

También se podrá utilizar Trivy, una herramienta de código abierto, para revisar vulnerabilidades de la imagen Docker. Este control no está implementado actualmente.

### 4.3. Procedimiento de actualización

1. Identificar la dependencia afectada y consultar sus notas de versión.
2. Revisar cambios incompatibles y vulnerabilidades corregidas.
3. Crear una rama específica para la actualización.
4. Modificar la versión fijada.
5. Ejecutar la suite completa, Ruff y pip-audit.
6. Verificar la construcción y ejecución de Docker.
7. Solicitar la revisión de otro integrante del equipo.
8. Integrar el cambio únicamente si las verificaciones son satisfactorias.
9. Registrar la evidencia y, si intervino una IA, actualizar la bitácora correspondiente.

No se deberán aceptar automáticamente actualizaciones propuestas por herramientas o asistentes de IA.

Actualmente las dependencias directas están fijadas, pero las dependencias transitivas no están completamente bloqueadas y la imagen base se referencia mediante una etiqueta, no mediante un digest inmutable. Estas condiciones limitan la reproducibilidad absoluta.

## 5. Operación y mantenimiento del modelo de IA

Esta sección describe una propuesta para cuando se implemente la CLI definida en ADR-001. Actualmente no existe comunicación con Gemini.

Los modelos de lenguaje pueden cambiar su comportamiento como consecuencia de actualizaciones realizadas por el proveedor, incluso cuando el código del asistente y los prompts permanecen iguales.

### 5.1. Riesgos de una actualización del modelo

| Riesgo | Consecuencia |
|---|---|
| Cambio en la estructura de las respuestas | Las pruebas generadas podrían no tener un formato válido. |
| Interpretación diferente de los requisitos | Se podrían generar pruebas con resultados esperados incorrectos. |
| Menor capacidad para detectar casos límite | Disminución de la efectividad de las pruebas. |
| Generación de funciones inexistentes | Las pruebas podrían fallar por errores de importación o ejecución. |
| Cambios de latencia | Mayor tiempo de generación de pruebas. |
| Cambios en cuotas gratuitas | Interrupciones en la generación o necesidad de limitar solicitudes. |
| Retirada de un modelo | La CLI podría dejar de funcionar con el identificador configurado. |

### 5.2. Control de versiones del modelo

Se propone registrar:

- Identificador del modelo configurado.
- Versión efectiva del modelo, cuando el proveedor la exponga.
- Versión del prompt utilizado.
- Commit del proyecto evaluado.
- Fecha de la evaluación.
- Parámetros de generación relevantes.
- Resultados de las verificaciones.

Siempre que Google lo permita, se utilizará un identificador de modelo versionado en lugar de un alias que cambie automáticamente.

Fijar un identificador no garantiza por sí mismo que las respuestas sean idénticas ni que el proveedor mantenga indefinidamente disponible el modelo.

### 5.3. Evaluación de regresiones del modelo

Se propone construir un banco de evaluación con criterios de aceptación revisados por el equipo, fragmentos de código sintéticos y errores sembrados cuyo comportamiento esperado sea conocido.

El mismo banco deberá utilizarse antes y después de cambiar el modelo o modificar significativamente los prompts.

| Indicador | Criterio de aceptación | Origen |
|---|---|---|
| Archivos excluidos enviados | 0 | RNF-06 |
| Pruebas generadas con datos inventados | 100 % | RNF-07 |
| Errores sembrados detectados | Mínimo 8 de 10 | RNF-08 |
| Pruebas válidas sobre una implementación correcta | Todas las pruebas aceptadas deben pasar | Política de calidad propuesta |
| Resultados esperados derivados de requisitos | Todas las pruebas aceptadas deben tener un oráculo justificable | Política de calidad propuesta |
| Pruebas con funciones inexistentes | 0 entre las pruebas aceptadas | Política de calidad propuesta |

Para atender la variabilidad de los modelos de lenguaje, se propone realizar tres generaciones independientes con el mismo banco de evaluación, siempre que la cuota gratuita lo permita.

Las tres generaciones constituyen un supuesto metodológico y no un experimento ya realizado.

### 5.4. Procedimiento ante un cambio del modelo

1. Identificar el nuevo modelo y revisar la documentación oficial del proveedor.
2. Conservar los resultados de evaluación del modelo anterior como referencia.
3. Ejecutar el mismo banco de evaluación con el nuevo modelo.
4. Revisar manualmente los resultados esperados de las pruebas generadas.
5. Ejecutar las pruebas sobre una implementación correcta.
6. Evaluar su capacidad para detectar los diez errores sembrados.
7. Comprobar que no utilicen datos reales ni archivos excluidos.
8. Comparar los resultados con la evaluación anterior.
9. Rechazar el cambio si incumple algún RNF o presenta una regresión de calidad no justificada.
10. Registrar la decisión, las evidencias y las correcciones en el repositorio.

Si el modelo anterior continúa disponible, se podrá mantener temporalmente mientras se corrigen los problemas del nuevo modelo.

Si ya no está disponible, se deberá suspender la generación automática hasta verificar una alternativa. No se deberá cambiar a otro modelo sin evaluar sus resultados.

### 5.5. Control humano de las pruebas generadas

Las pruebas propuestas por la IA no deberán incorporarse automáticamente a la suite.

Antes de aceptar una prueba, el desarrollador deberá responder:

- ¿El resultado esperado proviene de un criterio de aceptación o requisito escrito?
- ¿La prueba falla cuando se rompe el comportamiento que pretende verificar?
- ¿Aporta una comprobación que no está cubierta innecesariamente por otra prueba?
- ¿Utiliza exclusivamente datos inventados?
- ¿Respeta los archivos y funciones que realmente existen?

La cobertura de código será un indicador complementario, pero no sustituirá la revisión del oráculo ni la evaluación mediante errores sembrados.

Los incumplimientos de estos controles deberán registrarse como resultados rechazados o corregidos en la bitácora de IA.

## 6. Estado actual y propuestas futuras

### 6.1. Capacidades existentes

| Capacidad | Evidencia en el repositorio |
|---|---|
| Filtro de exclusión de archivos HU-07 | asistente/exclusion.py |
| Lista de exclusión | .asistenteignore |
| Suite de 102 pruebas | tests/ |
| Pruebas de aceptación de HU-07 al nivel de la librería | tests/test_aceptacion_hu07.py |
| Configuración de pytest y Ruff | pyproject.toml |
| Dependencias de desarrollo fijadas | requirements-dev.txt |
| Pipeline de integración continua | .github/workflows/ci.yml |
| Medición de cobertura de líneas y ramas | Resultados de GitHub Actions y artefacto coverage.xml |
| Auditoría automatizada de dependencias | Trabajo ci de GitHub Actions |
| Entorno de pruebas contenerizado | Dockerfile y .dockerignore |
| Ejecución automatizada de pruebas dentro del contenedor | Trabajo docker de GitHub Actions |
| Registro de pruebas y mutaciones manuales | registro_pruebas.md |
| Registro del uso y revisión de IA durante el desarrollo | bitacora_ia.md y docs/prompts/ |

La última ejecución del pipeline reportada por el equipo tardó 54 segundos. Los dos trabajos finalizaron correctamente y se ejecutaron 102 pruebas dentro del contenedor.

### 6.2. Propuestas pendientes

| Capacidad | Estado |
|---|---|
| Implementación de la CLI definida en ADR-001 | Pendiente |
| Lectura de .asistenteignore desde la aplicación | Pendiente |
| Integración con la API de Gemini | Pendiente |
| Registro estructurado de eventos de la CLI | Propuesta |
| Alertas automáticas por incumplimiento de tiempos | Propuesta |
| Monitoreo de consumo de solicitudes y tokens | Propuesta |
| Monitoreo de saturación de recursos | Propuesta |
| Actualización de dependencias mediante Dependabot | Propuesta |
| Auditoría de vulnerabilidades de la imagen Docker | Propuesta |
| Banco de evaluación de regresiones del modelo | Propuesta |
| Verificación de HU-07 de extremo a extremo | Pendiente |

### 6.3. Estado de verificación de los requisitos no funcionales

| Requisito | Estado de verificación |
|---|---|
| RNF-02 | Verificado mediante tres ejecuciones locales consecutivas el 2026-11-26, con 102 pruebas aprobadas, 0,12 segundos según pytest y 0,58 segundos de tiempo total del comando en cada ejecución. Cumple el límite de 120 segundos en las condiciones del equipo de desarrollo documentadas en la sección 2.1. |
| RNF-03 | La duración reportada de 54 segundos está por debajo del límite de 300 segundos. Debe comprobarse que las ejecuciones por pull request también cumplen este requisito. |
| RNF-06 | Verificado parcialmente al nivel de selección de archivos mediante las pruebas de HU-07. Pendiente de verificar durante una transmisión real. |
| RNF-07 | Existen datos sintéticos en las pruebas desarrolladas. Pendiente de verificar el 100 % de las pruebas generadas por la futura CLI. |
| RNF-08 | Existen antecedentes de mutaciones manuales. El cumplimiento requiere demostrar la detección de al menos ocho errores de un conjunto documentado de diez errores sembrados. |

### 6.4. Conclusión

La operación actual del proyecto se concentra en garantizar la calidad, seguridad y reproducibilidad del filtro de exclusión de archivos mediante pruebas automatizadas, análisis estático, auditoría de dependencias e integración continua.

No existe un servicio desplegado en producción, una base de datos propia ni usuarios finales. Por tanto, no se justifica implementar infraestructura compleja de monitoreo.

Las medidas futuras deberán incorporarse progresivamente conforme avance la implementación de la CLI y la integración con Gemini, utilizando herramientas gratuitas y priorizando la protección de datos, la revisión humana y la verificación objetiva de los resultados producidos por la IA.
