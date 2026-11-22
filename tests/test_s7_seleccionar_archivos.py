import re

import pytest

from asistente.exclusion import (
    ArchivoExcluidoError,
    seleccionar_archivos,
)


@pytest.mark.criterio("HU-07-E1")
@pytest.mark.parametrize(
    "rutas, patrones, esperado",
    [
        # S03: Límite - una ruta permitida.
        pytest.param(
            ["main.py"], [".env"], ["main.py"],
            id="S03",
        ),

        # S04: Límite - una ruta excluida.
        pytest.param(
            [".env"], [".env"], [],
            id="S04",
        ),

        # S07: Partición - rutas permitidas y excluidas mezcladas.
        pytest.param(
            ["main.py", ".env", "test.py", "pedidos.db"],
            [".env", "pedidos.db"],
            ["main.py", "test.py"],
            id="S07",
        ),

        # S08: Límite - lista de patrones vacía.
        pytest.param(
            ["main.py", ".env"], [], ["main.py", ".env"],
            id="S08",
        ),

        # S09: Partición - conserva las rutas permitidas repetidas.
        pytest.param(
            ["a.py", "a.py"], [".env"], ["a.py", "a.py"],
            id="S09",
        ),

        # S10: Partición - elimina todas las rutas excluidas repetidas.
        pytest.param(
            [".env", ".env"], [".env"], [],
            id="S10",
        ),

        # S12: Partición - convierte separadores de Windows.
        pytest.param(
            ["src\\main.py"], [], ["src/main.py"],
            id="S12",
        ),

        # S13: Partición - archivo excluido en mayúsculas.
        pytest.param(
            [".ENV"], [".env"], [],
            id="S13",
        ),

        # S14: Partición - conserva las mayúsculas en la salida.
        pytest.param(
            ["Main.PY"], [".env"], ["Main.PY"],
            id="S14",
        ),

        # S15: Partición - la salida solo cambia los separadores.
        pytest.param(
            ["./src//main.py"], [".env"], ["./src//main.py"],
            id="S15",
        ),

        # S29: Partición de abuso - ".." no evade un patrón de carpeta.
        pytest.param(
            ["datos/x/../clientes_panaderia.csv", "main.py"],
            ["datos/clientes_panaderia.csv"],
            ["main.py"],
            id="S29",
        ),

        # S30: Partición - patrón escrito en mayúsculas.
        pytest.param(
            [".env", "main.py"], [".ENV"], ["main.py"],
            id="S30",
        ),
    ],
)
def test_filtrar_rutas(rutas, patrones, esperado):
    resultado = seleccionar_archivos(rutas, patrones)

    assert resultado == esperado


@pytest.mark.criterio("HU-07-E2")
@pytest.mark.parametrize(
    "rutas, patrones, archivo_pedido, esperado",
    [
        # S17: Decisión R1 - sin archivo pedido, solo filtra.
        pytest.param(
            ["a.py", ".env"], [".env"], None, ["a.py"],
            id="S17",
        ),

        # S21: Decisión R3 - pedido permitido y presente.
        pytest.param(
            ["a.py", "b.py"], [], "a.py", ["a.py", "b.py"],
            id="S21",
        ),

        # S22: Decisión R4 y límite - lista de rutas vacía.
        pytest.param(
            [], [".env"], "a.py", ["a.py"],
            id="S22",
        ),

        # S26: Decisión R4 - pedido nuevo con separadores de Windows.
        pytest.param(
            ["a.py"], [], "src\\b.py", ["a.py", "src/b.py"],
            id="S26",
        ),
    ],
)
def test_gestionar_archivo_pedido(
    rutas, patrones, archivo_pedido, esperado
):
    resultado = seleccionar_archivos(
        rutas, patrones, archivo_pedido
    )

    assert resultado == esperado


@pytest.mark.criterio("HU-07-E2")
@pytest.mark.parametrize(
    "rutas, patrones, archivo_pedido, mensaje_esperado",
    [
        # S18: Decisión R2 - pedido excluido y presente.
        pytest.param(
            ["a.py", ".env"], [".env"], ".env", ".env",
            id="S18",
        ),

        # S19: Decisión R2 - pedido excluido y ausente.
        pytest.param(
            ["a.py"], ["pedidos.db"], "pedidos.db", "pedidos.db",
            id="S19",
        ),

        # S27: Decisión R2 - pedido excluido mediante flujo NTFS.
        pytest.param(
            ["a.py"], [".env"], ".env::$DATA", ".env::$DATA",
            id="S27",
        ),
    ],
)
def test_rechazar_archivo_pedido_excluido(
    rutas, patrones, archivo_pedido, mensaje_esperado
):
    with pytest.raises(
        ArchivoExcluidoError,
        match=re.escape(mensaje_esperado),
    ):
        seleccionar_archivos(rutas, patrones, archivo_pedido)
