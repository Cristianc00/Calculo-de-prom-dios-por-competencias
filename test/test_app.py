import pytest
import tkinter as tk
from app import Application

@pytest.fixture
def app_instance():
    """Crea una instancia de la aplicación en modo no interactivo."""
    app = Application()
    yield app
    app.destroy()

def test_app_inicializa_correctamente(app_instance):
    """Verifica que la app se inicializa sin errores y crea elementos clave."""
    assert isinstance(app_instance, tk.Tk)
    assert hasattr(app_instance, "entry_nombre")
    assert hasattr(app_instance, "score_buttons")
    assert len(app_instance.score_buttons) == 5  # 5 dimensiones

def test_select_score_y_promedio(app_instance):
    """Selecciona valores y verifica el cálculo de promedio."""
    app = app_instance
    app.select_score(0, 10, app.score_buttons[0][0])
    app.select_score(1, 8, app.score_buttons[1][2])
    app.select_score(2, 6, app.score_buttons[2][4])
    valores = [v for v in app.selected_scores if v is not None]
    promedio = sum(valores) / len(valores)
    assert abs(promedio - 8.0) < 0.01
    assert "8.00" in app.promedio_label.cget("text")

def test_guardar_resultados_no_falla(app_instance, capsys):
    """Verifica que guardar_resultados imprime información sin errores."""
    app = app_instance
    app.entry_nombre.insert(0, "Juan Pérez")
    app.select_score(0, 9, app.score_buttons[0][1])
    app.guardar_resultados()
    captured = capsys.readouterr()
    assert "RESULTADOS" in captured.out
    assert "Juan Pérez" in captured.out

def test_agregar_alumno_a_lista(app_instance, monkeypatch):
    """Simula agregar un alumno y verifica que se añade correctamente."""
    app = app_instance
    app.entry_nombre.insert(0, "María López")
    app.selected_scores = [10, 9, 8, 7, 6]
    
    # Evita ventanas emergentes
    monkeypatch.setattr("tkinter.messagebox.showinfo", lambda *a, **k: None)
    monkeypatch.setattr("tkinter.messagebox.showwarning", lambda *a, **k: None)
    
    app.agregar_alumno_a_lista()
    assert any(a["nombre"] == "María López" for a in app.todos_los_alumnos)
    assert abs(app.todos_los_alumnos[-1]["promedio"] - 8.0) < 0.01

def test_exportar_todos_los_promedios_sin_datos(app_instance, monkeypatch):
    """Prueba que al intentar exportar sin datos se muestra advertencia."""
    app = app_instance
    mensajes = []
    monkeypatch.setattr("tkinter.messagebox.showwarning", lambda t, m: mensajes.append(m))
    app.exportar_todos_los_promedios()
    assert any("No hay alumnos" in msg for msg in mensajes)