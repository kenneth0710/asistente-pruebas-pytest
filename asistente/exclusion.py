# asistente/exclusion.py

from fnmatch import fnmatchcase


class ArchivoExcluidoError(Exception):
    """Se lanza cuando se solicita revisar un archivo excluido."""

    pass


def seleccionar_archivos(
    rutas: list[str],
    patrones: list[str],
    archivo_pedido: str | None = None
) -> list[str]:
    """
    Selecciona los archivos permitidos según los patrones de exclusión.

    Las rutas se normalizan usando '/' y las comparaciones
    no distinguen mayúsculas de minúsculas.
    """

    def normalizar(ruta: str) -> str:
        return ruta.replace("\\", "/")

    def esta_excluido(ruta: str) -> bool:
        ruta_normalizada = normalizar(ruta).lower()
        nombre_archivo = ruta_normalizada.rsplit("/", 1)[-1]

        for patron in patrones:
            patron_normalizado = normalizar(patron).lower()

            if (
                fnmatchcase(ruta_normalizada, patron_normalizado)
                or fnmatchcase(nombre_archivo, patron_normalizado)
            ):
                return True

        return False

    # Si el archivo solicitado está excluido, se lanza una excepción.
    if archivo_pedido is not None and esta_excluido(archivo_pedido):
        raise ArchivoExcluidoError(
            f"El archivo '{normalizar(archivo_pedido)}' está excluido."
        )

    # Filtrar las rutas conservando su orden y las repeticiones.
    resultado = [
        normalizar(ruta)
        for ruta in rutas
        if not esta_excluido(ruta)
    ]

    # Agregar el archivo solicitado si está permitido y no existe
    # ya en las rutas después de normalizarlas.
    if archivo_pedido is not None:
        pedido_normalizado = normalizar(archivo_pedido)

        rutas_normalizadas = [normalizar(ruta) for ruta in rutas]

        if pedido_normalizado not in rutas_normalizadas:
            resultado.append(pedido_normalizado)

    return resultado
