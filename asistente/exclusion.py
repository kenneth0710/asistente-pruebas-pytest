"""Lista de exclusión del asistente (HU-07).

Contrato en el README, sección «Funcionalidad de la semana 5».
"""


class ArchivoExcluidoError(Exception):
    """El desarrollador pidió un archivo que está en la lista de exclusión."""


def seleccionar_archivos(
    rutas: list[str],
    patrones: list[str],
    archivo_pedido: str | None = None,
) -> list[str]:
    raise NotImplementedError("Pendiente: se implementa después de las pruebas")
