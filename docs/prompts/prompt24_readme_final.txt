Actúa como redactor técnico.

Contexto: el README del repositorio (lo escribiste tú en la semana 6 con 8 secciones: Qué es, Requisitos, Instalación, Ejecución, Pruebas, Estructura, Uso de IA, Autor y licencia) quedó desactualizado. Estos son los únicos cambios reales desde entonces:
- requirements-dev.txt ahora también tiene pytest-cov==7.1.0.
- Hay 102 pruebas: se agregó tests/test_aceptacion_hu07.py (2 pruebas de aceptación de HU-07, una por escenario, con dado/cuando/entonces).
- Cobertura con: pytest --cov=asistente --cov-branch --cov-report=term-missing. Resultado: 96 % de líneas, 92,86 % de ramas; las líneas 58 y 106 de exclusion.py están explicadas en registro_pruebas.md (sección 5).
- Pipeline .github/workflows/ci.yml en cada push y pull request, con dos trabajos: ci (ruff, pytest con cobertura, pip-audit y el artefacto coverage.xml) y docker (construye la imagen asistente-pruebas:0.1.0 y corre las pruebas dentro; solo corre si pasa ci). Ejecuciones en https://github.com/kenneth0710/asistente-pruebas-pytest/actions
- Dockerfile y .dockerignore: la imagen ejecuta las pruebas con un usuario sin privilegios. Comandos: docker build -t asistente-pruebas:0.1.0 . y docker run --rm asistente-pruebas:0.1.0
- Documentos nuevos: docs/revision_configuracion.md (revisión del pipeline y del Dockerfile), docs/plan_operacion.md (monitoreo y mantenimiento), docs/modulos/ (PDF de la propuesta, el banco de prompts, los requisitos y el diseño, con un README índice).
- Uso de IA nuevo: en el cierre (26 de noviembre) ChatGPT propuso el plan de cierre, el pipeline, el análisis de cobertura, las pruebas de aceptación, el Dockerfile y el plan de operación; bitácora entradas 18 a 23. En los módulos 1 a 3 se usaron Claude (banco de prompts y redacción de la propuesta) y Gemini (requisitos y diseño).
- La bitácora tiene 23 entradas: 10 aceptadas, 9 aceptadas con cambios y 4 rechazadas.

Tarea: entrega solo las secciones que cambian (Requisitos, Pruebas, una sección nueva «Integración continua y Docker» que va después de Pruebas, Estructura y Uso de IA), completas y listas para reemplazar las actuales.

Formato: Markdown. En Estructura, el árbol completo con los archivos nuevos.

Restricciones: usa solo los datos de este mensaje; no inventes comandos, archivos ni resultados; no cambies las demás secciones; mismo estilo y tono del README actual; los comandos en bloques de código.
