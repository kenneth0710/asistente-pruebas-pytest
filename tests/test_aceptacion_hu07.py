import pytest

from asistente.exclusion import ArchivoExcluidoError, seleccionar_archivos


@pytest.fixture
def repositorio_panaderia(tmp_path):
    archivos = {
        ".asistenteignore": ".env\nclientes_panaderia.csv\npedidos.db\n",
        ".env": "API_KEY=clave_ficticia_de_prueba\n",
        "clientes_panaderia.csv": (
            "id,nombre\n"
            "1,Cliente ficticio\n"
        ),
        "pedidos.db": "Contenido ficticio de prueba",
        "pedidos/__init__.py": "",
        "pedidos/modelos.py": "class Pedido:\n    pass\n",
        "pedidos/servicios.py": "def crear_pedido():\n    pass\n",
    }

    for ruta, contenido in archivos.items():
        archivo = tmp_path / ruta
        archivo.parent.mkdir(parents=True, exist_ok=True)
        archivo.write_text(contenido, encoding="utf-8")

    return tmp_path


def leer_patrones(repositorio):
    contenido = (repositorio / ".asistenteignore").read_text(
        encoding="utf-8"
    )

    return [
        linea.strip()
        for linea in contenido.splitlines()
        if linea.strip() and not linea.strip().startswith("#")
    ]


def listar_archivos(repositorio):
    return sorted(
        archivo.relative_to(repositorio).as_posix()
        for archivo in repositorio.rglob("*")
        if archivo.is_file()
    )


@pytest.mark.criterio("HU-07-E1")
def test_archivos_excluidos_no_se_incluyen(repositorio_panaderia):
    # Dado: la lista de exclusión contiene .env,
    # clientes_panaderia.csv y pedidos.db.
    patrones = leer_patrones(repositorio_panaderia)
    rutas = listar_archivos(repositorio_panaderia)

    # Cuando: el desarrollador pide pruebas para el módulo de pedidos.
    resultado = seleccionar_archivos(rutas, patrones)

    # Entonces: ninguno de esos 3 archivos se incluye en lo que
    # se envía al servicio de IA.
    assert ".env" not in resultado
    assert "clientes_panaderia.csv" not in resultado
    assert "pedidos.db" not in resultado

    assert resultado == [
        ".asistenteignore",
        "pedidos/__init__.py",
        "pedidos/modelos.py",
        "pedidos/servicios.py",
    ]


@pytest.mark.criterio("HU-07-E2")
def test_pedido_explicito_de_archivo_excluido(repositorio_panaderia):
    # Dado: .env está en la lista de exclusión.
    patrones = leer_patrones(repositorio_panaderia)
    rutas = listar_archivos(repositorio_panaderia)

    # Cuando: el desarrollador pide al asistente revisar .env.
    with pytest.raises(ArchivoExcluidoError) as error:
        seleccionar_archivos(rutas, patrones, archivo_pedido=".env")

    # Entonces: el asistente no envía el archivo y avisa
    # que está excluido.
    assert ".env" in str(error.value)
    assert "excluido" in str(error.value).lower()
