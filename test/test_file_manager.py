import os
import json
import pytest
import file_manager

@pytest.fixture
def sample_data():
    return [
        {
            "nombre": "Dimensión 1: Comprensión lectora",
            "textos": ["Identifica ideas principales", "Reconoce la intención del autor"]
        },
        {
            "nombre": "Dimensión 2: Resolución de problemas",
            "textos": ["Aplica estrategias lógicas", "Verifica coherencia de resultados"]
        }
    ]

@pytest.fixture
def sample_alumnos():
    return [
        {"nombre": "Juan Pérez", "promedio": 8.5},
        {"nombre": "Ana Gómez", "promedio": 9.2}
    ]

def test_guardar_y_cargar_json(tmp_path, sample_data):
    file_path = tmp_path / "competencias_test.json"
    success, error = file_manager.guardar_competencias_json(file_path, sample_data)
    assert success and error is None

    data, error = file_manager.cargar_competencias_json(file_path)
    assert error is None
    assert data == sample_data

def test_guardar_promedios_csv(tmp_path, sample_alumnos):
    file_path = tmp_path / "promedios.csv"
    success, error = file_manager.guardar_promedios_csv(file_path, sample_alumnos)
    assert success and error is None
    content = file_path.read_text(encoding="utf-8")
    assert "Alumno,Promedio" in content
    assert "Juan Pérez" in content
    assert "8.50" in content

def test_guardar_promedios_txt(tmp_path, sample_alumnos):
    file_path = tmp_path / "promedios.txt"
    success, error = file_manager.guardar_promedios_txt(file_path, sample_alumnos)
    assert success and error is None
    content = file_path.read_text(encoding="utf-8")
    assert "Alumno: Juan Pérez" in content
    assert "Promedio: 8.50" in content

def test_error_cargar_json_inexistente():
    data, error = file_manager.cargar_competencias_json("no_existe.json")
    assert data is None
    assert isinstance(error, Exception)

def test_formato_salida_csv_y_txt(tmp_path, sample_alumnos):
    csv_path = tmp_path / "test_output.csv"
    txt_path = tmp_path / "test_output.txt"
    file_manager.guardar_promedios_csv(csv_path, sample_alumnos)
    file_manager.guardar_promedios_txt(txt_path, sample_alumnos)

    csv_content = csv_path.read_text(encoding="utf-8").strip().splitlines()
    txt_content = txt_path.read_text(encoding="utf-8")

    assert csv_content[0] == "Alumno,Promedio"
    assert all("," in line for line in csv_content[1:])
    assert "----- RESULTADO -----" in txt_content