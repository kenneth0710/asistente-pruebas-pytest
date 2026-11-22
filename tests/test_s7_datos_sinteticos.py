import csv

import pytest

from asistente.exclusion import seleccionar_archivos


@pytest.fixture
def repo_panaderia(tmp_path):
    """Crea un repositorio ficticio con datos exclusivamente sintéticos."""

    archivos = {
        ".asistenteignore": (
            ".env\n"
            "clientes_panaderia.csv\n"
            "pedidos.db\n"
            "*.bak\n"
        ),
        ".env": "GEMINI_API_KEY=clave-falsa-solo-para-pruebas\n",
        "datos/pedidos.db": "",
        "datos/respaldo_pedidos.bak": "Respaldo ficticio para pruebas.\n",
        "app/main.py": "def iniciar():\n    return 'Panadería'\n",
        "app/pedidos/validación_año.py": (
            "def validar():\n    return True\n"
        ),
        "app/Pedidos de Doña Ana's.py": (
            "def listar_pedidos():\n    return []\n"
        ),
        "app/Inventario.PY": (
            "def consultar_inventario():\n    return []\n"
        ),
        "app/cálculo de precios.py": (
            "def calcular_total(precio, cantidad):\n"
            "    return precio * cantidad\n"
        ),
    }

    for ruta_relativa, contenido in archivos.items():
        archivo = tmp_path / ruta_relativa
        archivo.parent.mkdir(parents=True, exist_ok=True)
        archivo.write_text(contenido, encoding="utf-8")

    # Todos los registros son inventados y exclusivos para pruebas.
    clientes = [
        [1, "Ámbar Castañuelo", "Cándido Leguízamo", "300 000 0001", 0],
        [2, "Nicolás Piñaluz", "Las Granjas", "300 000 0002", 12500],
        [3, "Érika D'Avellana", "Santa Inés", "300 000 0003", 8000],
        [4, "Maíra Sueñaflor", "El Jardín", "300 000 0004", 3500],
        [5, "Julián Trigaluna", "Los Mártires", "300 000 0005", 16200],
        [6, "", "La Gaitana", "300 000 0006", 0],
        [7, "Lucía Cañaviento", "Las Palmas", "300 000 0007", 7200],
        [8, "Simón D'Espigal", "El Altico", "300 000 0008", 4500],
    ]

    archivo_csv = tmp_path / "datos/clientes_panaderia.csv"

    with archivo_csv.open("w", encoding="utf-8", newline="") as archivo:
        escritor = csv.writer(archivo)
        escritor.writerow(
            ["id", "nombre", "barrio", "telefono", "saldo_fiado"]
        )
        escritor.writerows(clientes)

    # Devuelve todas las rutas relativas con "/" y en orden alfabético.
    return sorted(
        archivo.relative_to(tmp_path).as_posix()
        for archivo in tmp_path.rglob("*")
        if archivo.is_file()
    )


@pytest.mark.criterio("HU-07-E1")
def test_filtrar_repositorio_panaderia(repo_panaderia, tmp_path):
    """Comprueba exactamente qué archivos permite el filtro."""

    archivo_ignore = tmp_path / ".asistenteignore"

    patrones = archivo_ignore.read_text(
        encoding="utf-8"
    ).splitlines()

    esperado = [
        ".asistenteignore",
        "app/Inventario.PY",
        "app/Pedidos de Doña Ana's.py",
        "app/cálculo de precios.py",
        "app/main.py",
        "app/pedidos/validación_año.py",
    ]

    resultado = seleccionar_archivos(repo_panaderia, patrones)

    assert resultado == esperado


@pytest.mark.criterio("HU-07-E1")
def test_verificar_datos_sinteticos_del_csv(repo_panaderia, tmp_path):
    """Comprueba las características de los datos sintéticos."""

    archivo_csv = tmp_path / "datos/clientes_panaderia.csv"

    with archivo_csv.open("r", encoding="utf-8", newline="") as archivo:
        clientes = list(csv.DictReader(archivo))

    # Comprueba la cantidad exacta de clientes sintéticos.
    assert len(clientes) == 8

    # Comprueba que existe al menos un nombre vacío.
    assert any(cliente["nombre"] == "" for cliente in clientes) is True

    # Comprueba que existe al menos un nombre con ñ.
    assert any("ñ" in cliente["nombre"] for cliente in clientes) is True

    # Comprueba que existe al menos un nombre con apóstrofo.
    assert any("'" in cliente["nombre"] for cliente in clientes) is True

    # Comprueba que existe al menos un cliente con saldo cero.
    assert any(
        cliente["saldo_fiado"] == "0" for cliente in clientes
    ) is True

    # Comprueba que todos los teléfonos tienen el prefijo sintético.
    assert all(
        cliente["telefono"].startswith("300 000")
        for cliente in clientes
    ) is True
