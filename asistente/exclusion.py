"""Documentación del módulo de exclusión correspondiente a la HU-07.

El contrato de las funciones de este módulo está definido en el README.
"""

from fnmatch import fnmatchcase


class ArchivoExcluidoError(Exception):
    """Indica que el desarrollador solicitó un archivo excluido."""


def _normalizar_ruta(ruta: str) -> str:
    """Convierte las barras invertidas de una ruta en barras normales.

    Args:
        ruta (str): Ruta que se desea normalizar.

    Returns:
        str: Ruta con las barras invertidas reemplazadas por barras normales.
    """
    return ruta.replace("\\", "/")


def _normalizar_para_comparar(ruta: str) -> str:
    """Normaliza una ruta para comparar sus equivalencias con los patrones.

    Args:
        ruta (str): Ruta que se desea normalizar para la comparación.

    Returns:
        str: Ruta con separadores normalizados, componentes vacíos y puntos
            simples eliminados, componentes especiales procesados y en
            minúsculas.
    """
    ruta = _normalizar_ruta(ruta)
    componentes = []

    for componente in ruta.split("/"):
        if componente in ("", "."):
            continue

        if componente == "..":
            if componentes and componentes[-1] != "..":
                componentes.pop()
            elif not ruta.startswith("/"):
                componentes.append(componente)
            continue

        if len(componente) == 2 and componente[1] == ":":
            componente = componente.lower()
        elif ":" in componente:
            componente = componente.split(":", 1)[0]

        componente = componente.rstrip(" .")

        if componente in ("", "."):
            continue

        componentes.append(componente)

    prefijo = "/" if ruta.startswith("/") else ""
    return (prefijo + "/".join(componentes)).lower()


def _coincide_con_patron(ruta: str, patron: str) -> bool:
    """Comprueba si un patrón coincide con una ruta completa o alguno de sus sufijos.

    Args:
        ruta (str): Ruta normalizada que se desea comprobar.
        patron (str): Patrón glob con el que se compara la ruta.

    Returns:
        bool: True si el patrón coincide con la ruta completa o algún sufijo;
            False en caso contrario.
    """
    componentes = ruta.split("/")
    if fnmatchcase(ruta, patron):
        return True

    return any(
        fnmatchcase("/".join(componentes[indice:]), patron)
        for indice in range(len(componentes))
    )


def _esta_excluido(ruta: str, patrones_normalizados: list[str]) -> bool:
    """Determina si una ruta coincide con alguno de los patrones de exclusión.

    Args:
        ruta (str): Ruta que se desea comprobar.
        patrones_normalizados (list[str]): Patrones normalizados que se utilizan
            para comprobar la exclusión.

    Returns:
        bool: True si la ruta o su nombre coincide con algún patrón;
            False en caso contrario.
    """
    ruta_normalizada = _normalizar_para_comparar(ruta)
    nombre_archivo = ruta_normalizada.rsplit("/", 1)[-1]

    for patron in patrones_normalizados:
        if _coincide_con_patron(ruta_normalizada, patron):
            return True
        if fnmatchcase(nombre_archivo, patron):
            return True

    return False


def seleccionar_archivos(
    rutas: list[str],
    patrones: list[str],
    archivo_pedido: str | None = None,
) -> list[str]:
    """Selecciona las rutas que no coinciden con los patrones de exclusión.

    Normaliza los separadores de las rutas, comprueba la exclusión mediante
    patrones glob y conserva el orden de las rutas permitidas. Si se proporciona
    un archivo solicitado que está excluido, lanza una excepción. Si el archivo
    solicitado no está excluido y no aparece en las rutas originales, lo agrega
    al final del resultado.

    Args:
        rutas (list[str]): Lista de rutas que se desean filtrar.
        patrones (list[str]): Lista de patrones glob utilizados para determinar
            qué rutas están excluidas.
        archivo_pedido (str | None): Ruta del archivo solicitado explícitamente.
            Si está excluido, se lanza una excepción. Si no está excluido y no
            aparece en las rutas originales, se agrega al resultado.
            Por defecto es None.

    Returns:
        list[str]: Nueva lista con las rutas permitidas, en el mismo orden
            en que aparecen en la entrada, conservando las repeticiones.
            Las barras invertidas se reemplazan por barras normales.
            Si corresponde, incluye el archivo solicitado al final.

    Raises:
        ArchivoExcluidoError: Si el archivo_pedido coincide con alguno de los
            patrones de exclusión.
    """
    rutas_normalizadas = [_normalizar_ruta(ruta) for ruta in rutas]
    patrones_normalizados = [
        _normalizar_para_comparar(patron) for patron in patrones
    ]
    pedido_normalizado = (
        _normalizar_ruta(archivo_pedido) if archivo_pedido is not None else None
    )

    if pedido_normalizado is not None and _esta_excluido(
        pedido_normalizado, patrones_normalizados
    ):
        raise ArchivoExcluidoError(
            f"El archivo '{pedido_normalizado}' está excluido."
        )

    resultado = [
        ruta
        for ruta in rutas_normalizadas
        if not _esta_excluido(ruta, patrones_normalizados)
    ]

    if pedido_normalizado is not None and pedido_normalizado not in rutas_normalizadas:
        resultado.append(pedido_normalizado)

    return resultado
