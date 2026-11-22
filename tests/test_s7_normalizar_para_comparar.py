import pytest

from asistente.exclusion import _normalizar_para_comparar


@pytest.mark.criterio("HU-07-E1")
@pytest.mark.parametrize(
    "ruta, esperado",
    [
        # N01: Límite - cadena vacía.
        pytest.param(
            "", "",
            id="N01",
        ),

        # N03: Partición - ruta ya normalizada.
        pytest.param(
            "datos/pedidos.db", "datos/pedidos.db",
            id="N03",
        ),

        # N04: Partición - separadores de Windows.
        pytest.param(
            "datos\\pedidos.db", "datos/pedidos.db",
            id="N04",
        ),

        # N06: Límite - barra doble.
        pytest.param(
            "datos//pedidos.db", "datos/pedidos.db",
            id="N06",
        ),

        # N08: Límite - barra al final.
        pytest.param(
            "datos/", "datos",
            id="N08",
        ),

        # N09: Límite - ruta absoluta.
        pytest.param(
            "/datos/pedidos.db", "/datos/pedidos.db",
            id="N09",
        ),

        # N10: Límite - únicamente la raíz.
        pytest.param(
            "/", "/",
            id="N10",
        ),

        # N12: Partición - componente "." al inicio.
        pytest.param(
            "./.env", ".env",
            id="N12",
        ),

        # N13: Partición - componente "." intermedio.
        pytest.param(
            "datos/./pedidos.db", "datos/pedidos.db",
            id="N13",
        ),

        # N15: Límite - únicamente el componente ".".
        pytest.param(
            ".", "",
            id="N15",
        ),

        # N16: Partición - ".." elimina el componente anterior.
        pytest.param(
            "x/../.env", ".env",
            id="N16",
        ),

        # N17: Partición - varios componentes "..".
        pytest.param(
            "a/b/../../.env", ".env",
            id="N17",
        ),

        # N18: Partición - ".." sin anterior en ruta relativa.
        pytest.param(
            "../datos/pedidos.db", "../datos/pedidos.db",
            id="N18",
        ),

        # N19: Partición - ".." sin anterior en ruta absoluta.
        pytest.param(
            "/../.env", "/.env",
            id="N19",
        ),

        # N20: Límite - ".." deja la ruta vacía.
        pytest.param(
            "a/..", "",
            id="N20",
        ),

        # N21: Límite - ".." regresa a la raíz.
        pytest.param(
            "/a/..", "/",
            id="N21",
        ),

        # N22: Límite - espacio al final.
        pytest.param(
            ".env ", ".env",
            id="N22",
        ),

        # N24: Límite - punto al final.
        pytest.param(
            ".env.", ".env",
            id="N24",
        ),

        # N26: Partición - puntos y espacios finales combinados.
        pytest.param(
            ".env. . ", ".env",
            id="N26",
        ),

        # N27: Partición - limpieza de un componente intermedio.
        pytest.param(
            "datos. /pedidos.db", "datos/pedidos.db",
            id="N27",
        ),

        # N28: Partición - conserva el espacio al inicio.
        pytest.param(
            " .env", " .env",
            id="N28",
        ),

        # N29: Partición - conserva los puntos internos.
        pytest.param(
            "archivo.test.py", "archivo.test.py",
            id="N29",
        ),

        # N30: Partición - elimina el flujo alternativo NTFS.
        pytest.param(
            ".env::$DATA", ".env",
            id="N30",
        ),

        # N31: Partición - dos puntos en un componente intermedio.
        pytest.param(
            "datos:flujo/pedidos.db", "datos/pedidos.db",
            id="N31",
        ),

        # N32: Límite - letra de unidad sola.
        pytest.param(
            "C:", "c:",
            id="N32",
        ),

        # N33: Partición - ruta con unidad de Windows.
        pytest.param(
            "C:\\Datos\\PEDIDOS.DB", "c:/datos/pedidos.db",
            id="N33",
        ),

        # N34: Partición - convierte las mayúsculas a minúsculas.
        pytest.param(
            "DATOS/CLIENTES_PANADERIA.CSV",
            "datos/clientes_panaderia.csv",
            id="N34",
        ),

        # N36: Partición - combinación de varias reglas.
        pytest.param(
            "/DATOS//./x/../.ENV. ", "/datos/.env",
            id="N36",
        ),

        # N38: Partición - nombre de una letra con flujo NTFS no es una unidad.
        pytest.param(
            "a:$DATA", "a",
            id="N38",
        ),
    ],
)
def test_normalizar_ruta_para_comparar(ruta, esperado):
    resultado = _normalizar_para_comparar(ruta)

    assert resultado == esperado
