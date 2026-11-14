"""Pruebas de abuso para las evasiones del filtro de exclusión HU-07."""

import pytest

from asistente.exclusion import ArchivoExcluidoError, seleccionar_archivos


@pytest.mark.criterio("HU-07-E1")
@pytest.mark.parametrize(
    "ruta",
    [
        "./datos/clientes_panaderia.csv",
        "x/../datos/clientes_panaderia.csv",
        "datos//clientes_panaderia.csv",
        "C:/repo/datos/clientes_panaderia.csv",
        "/home/ana/repo/datos/clientes_panaderia.csv",
    ],
)
def test_HU07_E1_excluye_rutas_equivalentes_con_patron_de_carpeta(ruta):
    resultado = seleccionar_archivos(
        [ruta, "app/pedidos/validaciones.py"],
        ["datos/clientes_panaderia.csv"],
    )

    assert resultado == ["app/pedidos/validaciones.py"]


@pytest.mark.criterio("HU-07-E1")
@pytest.mark.parametrize("ruta", [".env ", ".env.", ".env::$DATA"])
def test_HU07_E1_excluye_variantes_de_nombre_de_windows(ruta):
    resultado = seleccionar_archivos(
        [ruta, "app/pedidos/validaciones.py"],
        [".env"],
    )

    assert resultado == ["app/pedidos/validaciones.py"]


@pytest.mark.criterio("HU-07-E2")
def test_HU07_E2_pedir_env_con_espacio_final_lanza_error():
    with pytest.raises(ArchivoExcluidoError):
        seleccionar_archivos(
            ["app/pedidos/validaciones.py"],
            [".env"],
            ".env ",
        )


@pytest.mark.criterio("HU-07-E1")
def test_HU07_E1_env_ejemplo_sigue_permitido():
    resultado = seleccionar_archivos([".env.ejemplo"], [".env"])

    assert resultado == [".env.ejemplo"]
