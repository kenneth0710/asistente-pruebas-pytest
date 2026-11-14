"""Lista de exclusión del asistente (HU-07)."""

from fnmatch import fnmatchcase


class ArchivoExcluidoError(Exception):
    """El desarrollador pidió un archivo que está en la lista de exclusión."""


def _normalizar_ruta(ruta: str) -> str:
    """Convierte las barras invertidas de Windows en barras normales."""
    return ruta.replace("\\", "/")


def _normalizar_para_comparar(ruta: str) -> str:
    """Normaliza equivalencias de rutas sin modificar la ruta que se devuelve."""
    ruta = _normalizar_ruta(ruta)
    componentes = []

    for componente in ruta.split("/"):
        if len(componente) == 2 and componente[1] == ":":
            componente = componente.lower()
        elif ":" in componente:
            componente = componente.split(":", 1)[0]

        componente = componente.rstrip(" .")
        if componente in ("", "."):
            continue
        if componente == "..":
            if componentes and componentes[-1] != "..":
                componentes.pop()
            elif not ruta.startswith("/"):
                componentes.append(componente)
            continue
        componentes.append(componente)

    prefijo = "/" if ruta.startswith("/") else ""
    return (prefijo + "/".join(componentes)).lower()


def _coincide_con_patron(ruta: str, patron: str) -> bool:
    """Comprueba el patrón contra la ruta completa o cualquier sufijo."""
    componentes = ruta.split("/")
    if fnmatchcase(ruta, patron):
        return True

    return any(
        fnmatchcase("/".join(componentes[indice:]), patron)
        for indice in range(len(componentes))
    )


def _esta_excluido(ruta: str, patrones_normalizados: list[str]) -> bool:
    """Indica si la ruta coincide con un patrón por ruta o por nombre."""
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
    """Devuelve las rutas permitidas en una lista nueva y conserva su orden."""
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
