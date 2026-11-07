"""Lista de exclusión del asistente (HU-07).

Contrato en el README, sección «Funcionalidad de la semana 5».
Implementación propuesta por ChatGPT y refactorizada (bitácora, entradas 5 y 6).
"""

from fnmatch import fnmatchcase


class ArchivoExcluidoError(Exception):
    """El desarrollador pidió un archivo que está en la lista de exclusión."""


def _normalizar_ruta(ruta: str) -> str:
    """Convierte las barras invertidas de Windows en barras normales."""
    return ruta.replace("\\", "/")


def _esta_excluido(ruta: str, patrones_en_minuscula: list[str]) -> bool:
    """Indica si la ruta coincide con algún patrón, por ruta completa o por nombre.

    La ruta debe venir normalizada con «/» y los patrones normalizados y en
    minúscula; así la comparación no distingue mayúsculas en ningún sistema.
    """
    ruta_minuscula = ruta.lower()
    nombre_archivo = ruta_minuscula.rsplit("/", 1)[-1]

    for patron in patrones_en_minuscula:
        if fnmatchcase(ruta_minuscula, patron) or fnmatchcase(nombre_archivo, patron):
            return True

    return False


def seleccionar_archivos(
    rutas: list[str],
    patrones: list[str],
    archivo_pedido: str | None = None,
) -> list[str]:
    """Devuelve, en una lista nueva y en el mismo orden, las rutas que se pueden enviar a la IA.

    Si archivo_pedido está excluido lanza ArchivoExcluidoError y no se envía nada.
    """
    # Normalizar las rutas, los patrones y el archivo pedido una sola vez.
    rutas_normalizadas = [_normalizar_ruta(ruta) for ruta in rutas]
    patrones_en_minuscula = [_normalizar_ruta(patron).lower() for patron in patrones]
    pedido_normalizado = (
        _normalizar_ruta(archivo_pedido) if archivo_pedido is not None else None
    )

    if pedido_normalizado is not None and _esta_excluido(
        pedido_normalizado, patrones_en_minuscula
    ):
        raise ArchivoExcluidoError(f"El archivo '{pedido_normalizado}' está excluido.")

    # Filtrar las rutas permitidas conservando su orden y sus repeticiones.
    resultado = [
        ruta
        for ruta in rutas_normalizadas
        if not _esta_excluido(ruta, patrones_en_minuscula)
    ]

    # Agregar el archivo pedido si todavía no estaba en las rutas.
    if pedido_normalizado is not None and pedido_normalizado not in rutas_normalizadas:
        resultado.append(pedido_normalizado)

    return resultado
