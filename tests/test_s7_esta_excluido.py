
import pytest

from asistente.exclusion import _esta_excluido


@pytest.mark.criterio("HU-07-E1")
@pytest.mark.parametrize(
    "ruta, patrones_normalizados, esperado",
    [
        # E01: Límite - lista de patrones vacía.
        pytest.param(
            ".env", [], False,
            id="E01",
        ),

        # E03: Límite - un patrón que coincide.
        pytest.param(
            ".env", [".env"], True,
            id="E03",
        ),

        # E04: Límite - un patrón que no coincide.
        pytest.param(
            "main.py", [".env"], False,
            id="E04",
        ),

        # E05: Partición - coincidencia con la ruta completa.
        pytest.param(
            "datos/pedidos.db", ["datos/pedidos.db"], True,
            id="E05",
        ),

        # E06: Partición - coincidencia con un final de la ruta.
        pytest.param(
            "c:/repo/datos/clientes_panaderia.csv",
            ["datos/clientes_panaderia.csv"],
            True,
            id="E06",
        ),

        # E07: Partición - coincidencia con el nombre del archivo.
        pytest.param(
            "src/config/.env", [".env"], True,
            id="E07",
        ),

        # E08: Partición - componente parecido no coincide.
        pytest.param(
            "misdatos/pedidos.db", ["datos/pedidos.db"], False,
            id="E08",
        ),

        # E09: Partición - nombre parecido no coincide.
        pytest.param(
            "archivo.env", [".env"], False,
            id="E09",
        ),

        # E10: Partición - patrón al comienzo, no al final.
        pytest.param(
            "datos/pedidos.db/copia.py",
            ["datos/pedidos.db"],
            False,
            id="E10",
        ),

        # E11: Partición - comodín glob que coincide.
        pytest.param(
            "datos/pedidos.db", ["*.db"], True,
            id="E11",
        ),

        # E12: Partición - comodín glob que no coincide.
        pytest.param(
            "datos/pedidos.csv", ["*.db"], False,
            id="E12",
        ),

        # E17: Partición - varios patrones sin coincidencias.
        pytest.param(
            "main.py", [".env", "*.db", "*.csv"], False,
            id="E17",
        ),

        # E20: Partición - coincide el último patrón.
        pytest.param(
            "clientes_panaderia.csv",
            [".env", "*.db", "*.csv"],
            True,
            id="E20",
        ),

        # E23: Partición - ruta escrita en mayúsculas.
        pytest.param(
            "DATOS/PEDIDOS.DB", ["datos/pedidos.db"], True,
            id="E23",
        ),

        # E24: Partición - separadores de Windows.
        pytest.param(
            "datos\\pedidos.db", ["datos/pedidos.db"], True,
            id="E24",
        ),

        # E25: Partición - componentes "." y barras dobles.
        pytest.param(
            "./datos//./pedidos.db", ["datos/pedidos.db"], True,
            id="E25",
        ),

        # E36: Partición de abuso - ".." dentro de la carpeta.
        pytest.param(
            "datos/x/../pedidos.db", ["datos/pedidos.db"], True,
            id="E36",
        ),

        # E27: Partición - ".." sobre la raíz absoluta.
        pytest.param(
            "/../.env", [".env"], True,
            id="E27",
        ),

        # E28: Límite - espacio al final.
        pytest.param(
            ".env ", [".env"], True,
            id="E28",
        ),

        # E29: Límite - punto al final.
        pytest.param(
            ".env.", [".env"], True,
            id="E29",
        ),

        # E30: Partición - flujo alternativo NTFS.
        pytest.param(
            ".env::$DATA", [".env"], True,
            id="E30",
        ),

        # E31: Partición - sufijo con dos puntos y número.
        pytest.param(
            "datos/clientes_panaderia.csv:1",
            ["clientes_panaderia.csv"],
            True,
            id="E31",
        ),

        # E32: Límite - barra al final.
        pytest.param(
            "datos/pedidos.db/", ["pedidos.db"], True,
            id="E32",
        ),

        # E33: Partición - ruta y patrón absolutos.
        pytest.param(
            "/datos/pedidos.db", ["/datos/pedidos.db"], True,
            id="E33",
        ),

        # E34: Partición - ruta relativa y patrón absoluto.
        pytest.param(
            "datos/pedidos.db", ["/datos/pedidos.db"], False,
            id="E34",
        ),
    ],
)
def test_determinar_si_ruta_esta_excluida(
    ruta, patrones_normalizados, esperado
):
    resultado = _esta_excluido(ruta, patrones_normalizados)

    assert resultado is esperado

