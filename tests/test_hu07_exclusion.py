"""Pruebas de la HU-07: el asistente ignora los archivos de la lista de exclusión.

Base propuesta por ChatGPT (bitácora, entrada 1) y revisada a mano:
- se rechazó la prueba que esperaba enviar «.ENV» (entrada 2) y se cambió el contrato;
- se agregaron las pruebas de comodín y de archivo pedido repetido (entrada 3);
- se agregó la comprobación de que se devuelve una lista nueva.
Todos los datos son inventados.
"""

import pytest

from asistente.exclusion import ArchivoExcluidoError, seleccionar_archivos


# =====================================================
# HU-07-E1: los archivos excluidos no se envían a la IA
# =====================================================


@pytest.mark.criterio("HU-07-E1")
def test_HU07_E1_env_clientes_y_pedidos_no_se_envian():
    rutas = [
        "app/pedidos/validaciones.py",
        ".env",
        "datos/clientes_panaderia.csv",
        "pedidos.db",
    ]
    patrones = [".env", "clientes_panaderia.csv", "pedidos.db"]

    resultado = seleccionar_archivos(rutas, patrones)

    assert resultado == ["app/pedidos/validaciones.py"]


@pytest.mark.criterio("HU-07-E1")
def test_HU07_E1_conserva_el_orden_de_archivos_permitidos():
    rutas = [
        "app/pedidos/modelos.py",
        "app/pedidos/validaciones.py",
        ".env",
        "app/pedidos/servicio.py",
    ]
    patrones = [".env"]

    resultado = seleccionar_archivos(rutas, patrones)

    assert resultado == [
        "app/pedidos/modelos.py",
        "app/pedidos/validaciones.py",
        "app/pedidos/servicio.py",
    ]


@pytest.mark.criterio("HU-07-E1")
def test_HU07_E1_agrega_archivo_pedido_permitido_al_final():
    rutas = ["app/pedidos/validaciones.py"]
    patrones = [".env"]

    resultado = seleccionar_archivos(rutas, patrones, "tests/pedidos/test_hu03.py")

    assert resultado == [
        "app/pedidos/validaciones.py",
        "tests/pedidos/test_hu03.py",
    ]


@pytest.mark.criterio("HU-07-E1")
def test_HU07_E1_patron_con_comodin_excluye_por_extension():
    rutas = ["app/pedidos/validaciones.py", "datos/pedidos.db", "copia.db"]
    patrones = ["*.db"]

    resultado = seleccionar_archivos(rutas, patrones)

    assert resultado == ["app/pedidos/validaciones.py"]


# =====================================================
# HU-07-E1: casos límite
# =====================================================


@pytest.mark.criterio("HU-07-E1")
def test_HU07_E1_lista_de_rutas_vacia_devuelve_lista_vacia():
    resultado = seleccionar_archivos([], [".env"])

    assert resultado == []


@pytest.mark.criterio("HU-07-E1")
def test_HU07_E1_sin_patrones_se_envian_todas_en_una_lista_nueva():
    rutas = [".env", "pedidos.db", "app/pedidos/validaciones.py"]

    resultado = seleccionar_archivos(rutas, [])

    assert resultado == rutas
    assert resultado is not rutas


@pytest.mark.criterio("HU-07-E1")
def test_HU07_E1_archivo_excluido_en_subcarpeta_no_se_envia():
    rutas = ["app/pedidos/validaciones.py", "config/.env", "tests/test_pedidos.py"]
    patrones = [".env"]

    resultado = seleccionar_archivos(rutas, patrones)

    assert resultado == ["app/pedidos/validaciones.py", "tests/test_pedidos.py"]


@pytest.mark.criterio("HU-07-E1")
def test_HU07_E1_rutas_de_windows_se_normalizan_y_se_filtran():
    rutas = [r"app\pedidos\validaciones.py", r"config\.env"]
    patrones = [".env"]

    resultado = seleccionar_archivos(rutas, patrones)

    assert resultado == ["app/pedidos/validaciones.py"]


@pytest.mark.criterio("HU-07-E1")
def test_HU07_E1_archivo_con_nombre_parecido_si_se_envia():
    rutas = [".env.ejemplo", "app/pedidos/validaciones.py"]
    patrones = [".env"]

    resultado = seleccionar_archivos(rutas, patrones)

    assert resultado == [".env.ejemplo", "app/pedidos/validaciones.py"]


@pytest.mark.criterio("HU-07-E1")
def test_HU07_E1_env_en_mayusculas_tampoco_se_envia():
    rutas = [".env", ".ENV", "config/.Env", "app/pedidos/validaciones.py"]
    patrones = [".env"]

    resultado = seleccionar_archivos(rutas, patrones)

    assert resultado == ["app/pedidos/validaciones.py"]


@pytest.mark.criterio("HU-07-E1")
def test_HU07_E1_conserva_rutas_repetidas():
    rutas = ["app/pedidos/modelos.py", "app/pedidos/modelos.py", ".env"]
    patrones = [".env"]

    resultado = seleccionar_archivos(rutas, patrones)

    assert resultado == ["app/pedidos/modelos.py", "app/pedidos/modelos.py"]


@pytest.mark.criterio("HU-07-E1")
def test_HU07_E1_archivo_pedido_que_ya_venia_no_se_repite():
    rutas = ["app/pedidos/validaciones.py"]
    patrones = [".env"]

    resultado = seleccionar_archivos(rutas, patrones, r"app\pedidos\validaciones.py")

    assert resultado == ["app/pedidos/validaciones.py"]


# =====================================================
# HU-07-E2 (error): pedir explícitamente un archivo excluido
# =====================================================


@pytest.mark.criterio("HU-07-E2")
def test_HU07_E2_pedir_env_lanza_error_y_avisa_la_ruta():
    with pytest.raises(ArchivoExcluidoError) as error:
        seleccionar_archivos(["app/pedidos/validaciones.py"], [".env"], ".env")

    assert ".env" in str(error.value)


@pytest.mark.criterio("HU-07-E2")
def test_HU07_E2_pedir_env_en_subcarpeta_lanza_error():
    with pytest.raises(ArchivoExcluidoError) as error:
        seleccionar_archivos(["app/pedidos/validaciones.py"], [".env"], "config/.env")

    assert "config/.env" in str(error.value)
