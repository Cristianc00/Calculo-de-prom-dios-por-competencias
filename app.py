# app.py
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import file_manager  # Importamos nuestro nuevo módulo

class Application(tk.Tk):
    def __init__(self):
        super().__init__()  # Inicializamos la clase padre tk.Tk

        # --- CONFIGURACIÓN PRINCIPAL ---
        self.title("Cálculo de Promedios por Dimensiones")
        self.geometry("1200x700")
        self.minsize(900, 600)
        self.configure(bg="White")

        # --- VARIABLES DE ESTADO (antes globales) ---
        self.selected_scores = [None] * 5
        self.score_buttons = []
        self.text_boxes = []
        self.entries_dimensiones = []
        self.todos_los_alumnos = []

        # --- CONSTRUIR LA INTERFAZ ---
        self._crear_widgets_superiores()
        self._crear_canvas_dimensiones()
        self._crear_widgets_inferiores()

        # --- CONFIGURAR EXPANSIÓN ---
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

    def _crear_widgets_superiores(self):
        frame_nombre = ttk.Frame(self, padding=10)
        frame_nombre.grid(row=0, column=0, sticky="ew", columnspan=2)
        frame_nombre.columnconfigure(1, weight=1)

        ttk.Label(frame_nombre, text="Ingresar nombre del alumno:").grid(row=0, column=0, sticky="w")
        self.entry_nombre = ttk.Entry(frame_nombre, font=("Arial", 12))
        self.entry_nombre.grid(row=1, column=0, sticky="ew", pady=5, padx=(0, 10))

        ttk.Button(frame_nombre, text="Importar Competencias", command=self.importar_competencias).grid(row=1, column=1, sticky="e", padx=5)
        ttk.Button(frame_nombre, text="Exportar Competencias", command=self.exportar_competencias).grid(row=1, column=2, sticky="e", padx=5)

    def _crear_canvas_dimensiones(self):
        self.canvas = tk.Canvas(self)
        self.canvas.grid(row=1, column=0, sticky="nsew")
        
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        scrollbar.grid(row=1, column=1, sticky="ns")
        self.canvas.configure(yscrollcommand=scrollbar.set)

        self.frame_dimensiones = ttk.Frame(self.canvas)
        self.frame_id = self.canvas.create_window((0, 0), window=self.frame_dimensiones, anchor="nw")

        # Binds para el scroll y ajuste
        self.frame_dimensiones.bind("<Configure>", self._actualizar_scroll)
        self.canvas.bind("<Configure>", self._ajustar_ancho_canvas)

        # Encabezado
        ttk.Label(self.frame_dimensiones, text="Competencia", anchor="center").grid(row=0, column=0, sticky="nsew")
        for col, num in enumerate(range(10, 0, -1), start=1):
            ttk.Label(self.frame_dimensiones, text=str(num), anchor="center").grid(row=0, column=col, sticky="nsew")
        for i in range(11):
            self.frame_dimensiones.columnconfigure(i, weight=1)

        # Creación de dimensiones
        for dim in range(5):
            botones_dim = []
            for col, value in enumerate(range(10, 0, -1), start=1):
                btn = tk.Button(self.frame_dimensiones, text=str(value), bg="white")
                btn.grid(row=2 * dim + 1, column=col, sticky="nsew", padx=1, pady=1)
                botones_dim.append(btn)
            self.score_buttons.append(botones_dim)

            textos_pares = []
            fila_textos = 2 * dim + 2
            
            txt_dim = tk.Text(self.frame_dimensiones, height=3, width=24, wrap="word", font=("Arial", 9))
            txt_dim.insert("1.0", f"Dimensión {dim+1}")
            txt_dim.grid(row=fila_textos, column=0, sticky="nsew", padx=6, pady=4)
            txt_dim.bind("<KeyPress>", self._ajustar_altura)
            txt_dim.bind("<KeyRelease>", self._ajustar_altura)
            self.entries_dimensiones.append(txt_dim)

            pares = [(10, 9), (8, 7), (6, 5), (4, 3), (2, 1)]
            for par in pares:
                col_inicio = 11 - par[0]
                txt = tk.Text(self.frame_dimensiones, height=3, width=24, wrap="word", font=("Arial", 9))
                txt.grid(row=fila_textos, column=col_inicio, columnspan=2, sticky="nsew", padx=6, pady=4)
                txt.bind("<KeyPress>", self._ajustar_altura)
                txt.bind("<KeyRelease>", self._ajustar_altura)
                textos_pares.append(txt)
            self.text_boxes.append(textos_pares)

        # Asignar comandos a botones
        for n in range(5):
            for btn, value in zip(self.score_buttons[n], range(10, 0, -1)):
                btn.configure(command=lambda dim=n, val=value, b=btn: self.select_score(dim, val, b))

    def _crear_widgets_inferiores(self):
        frame_promedio = tk.Frame(self, bg="#e3f2fd", height=50)
        frame_promedio.grid(row=2, column=0, sticky="ew", padx=10, pady=10, columnspan=2)
        frame_promedio.columnconfigure(0, weight=1)

        self.promedio_label = tk.Label(frame_promedio, text="Promedio actual: —", bg="#e3f2fd", font=("Arial", 12, "bold"))
        self.promedio_label.grid(row=0, column=0, pady=10, sticky="n")

        frame_guardar = ttk.Frame(self, padding=10)
        frame_guardar.grid(row=3, column=0, sticky="ew", columnspan=2)
        frame_guardar.columnconfigure(1, weight=1) # Centrar botones (hack)
        frame_guardar.columnconfigure(2, weight=1)

        ttk.Button(frame_guardar, text="Guardar Resultados", command=self.guardar_resultados).grid(row=0, column=0, pady=10, padx=10, sticky="e")
        ttk.Button(frame_guardar, text="Agregar Alumno a Lista", command=self.agregar_alumno_a_lista).grid(row=0, column=1, pady=10, padx=10, sticky="w")
        ttk.Button(frame_guardar, text="Exportar Todos los Promedios", command=self.exportar_todos_los_promedios).grid(row=0, column=2, pady=10, padx=10, sticky="w")

    # --- FUNCIONES DE LÓGICA (Métodos) ---

    def calcular_promedio(self):
        valores = [v for v in self.selected_scores if v is not None]
        if valores:
            promedio = sum(valores) / len(valores)
            self.promedio_label.config(text=f"Promedio actual: {promedio:.2f}")
        else:
            self.promedio_label.config(text="Promedio actual: —")

    def select_score(self, dim_index, value, button):
        for btn in self.score_buttons[dim_index]:
            btn.configure(bg="white")
        button.configure(bg="#b3e5fc")
        self.selected_scores[dim_index] = value
        self.calcular_promedio()

    def guardar_resultados(self):
        """Esta función solo imprime en consola, la mantenemos igual."""
        print("----- RESULTADOS -----")
        print(f"Alumno: {self.entry_nombre.get()}")
        for i, dimension in enumerate(self.text_boxes):
            dimension_texto = self.entries_dimensiones[i].get("1.0", "end").strip()
            print(f"Dimensión {i+1}: {dimension_texto}")
            print(f"Puntaje seleccionado: {self.selected_scores[i] if self.selected_scores[i] else 'Sin selección'}")
            for j, cuadro in enumerate(dimension):
                texto = cuadro.get("1.0", "end").strip()
                print(f"  Cuadro {j+1}: {texto}")
            print("----------------------")
        self.calcular_promedio()

    def agregar_alumno_a_lista(self):
        nombre = self.entry_nombre.get().strip()
        valores = [v for v in self.selected_scores if v is not None]
        if not nombre:
            messagebox.showwarning("Advertencia", "Ingrese el nombre del alumno.")
            return
        if not valores:
            messagebox.showwarning("Advertencia", "Seleccione al menos un puntaje para calcular el promedio.")
            return
        promedio = sum(valores) / len(valores)
        self.todos_los_alumnos.append({"nombre": nombre, "promedio": promedio})
        messagebox.showinfo("Éxito", f"Alumno {nombre} agregado a la lista.\nPromedio: {promedio:.2f}")
        self.entry_nombre.delete(0, "end")
        
        # Resetear puntajes y botones
        for i in range(len(self.selected_scores)):
            self.selected_scores[i] = None
            for btn in self.score_buttons[i]:
                btn.configure(bg="white")
        self.calcular_promedio()

    # --- LÓGICA DE ARCHIVOS (Refactorizada) ---

    def exportar_todos_los_promedios(self):
        if not self.todos_los_alumnos:
            messagebox.showwarning("Advertencia", "No hay alumnos en la lista para exportar.")
            return
        
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Archivo de texto", "*.txt"), ("Archivo CSV", "*.csv")],
            title="Exportar todos los promedios"
        )
        if not file_path:
            return

        if file_path.lower().endswith(".csv"):
            success, error = file_manager.guardar_promedios_csv(file_path, self.todos_los_alumnos)
        else:
            success, error = file_manager.guardar_promedios_txt(file_path, self.todos_los_alumnos)

        if success:
            messagebox.showinfo("Éxito", f"Promedios exportados correctamente en:\n{file_path}")
        else:
            messagebox.showerror("Error", f"No se pudo exportar el archivo:\n{error}")

    def exportar_competencias(self):
        data = []
        for i, cuadros in enumerate(self.text_boxes):
            dimension_data = {
                "nombre": self.entries_dimensiones[i].get("1.0", "end").strip(),
                "textos": [cuadro.get("1.0", "end").strip() for cuadro in cuadros]
            }
            data.append(dimension_data)
        
        file_path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("Archivos JSON", "*.json")],
            title="Guardar Competencias como..."
        )
        if not file_path:
            return
        
        success, error = file_manager.guardar_competencias_json(file_path, data)
        
        if success:
            messagebox.showinfo("Éxito", f"Competencias exportadas correctamente en:\n{file_path}")
        else:
            messagebox.showerror("Error", f"No se pudo exportar el archivo:\n{error}")

    def importar_competencias(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Archivos JSON", "*.json")],
            title="Importar Competencias"
        )
        if not file_path:
            return

        data, error = file_manager.cargar_competencias_json(file_path)

        if error:
            messagebox.showerror("Error", f"No se pudo importar el archivo:\n{error}")
            return

        # Si todo salió bien, poblamos la UI
        for i, dim_data in enumerate(data):
            if i < len(self.entries_dimensiones):
                self.entries_dimensiones[i].delete("1.0", "end")
                self.entries_dimensiones[i].insert("1.0", dim_data["nombre"])
                for j, cuadro in enumerate(self.text_boxes[i]):
                    cuadro.delete("1.0", "end")
                    if j < len(dim_data["textos"]):
                        cuadro.insert("1.0", dim_data["textos"][j])
        messagebox.showinfo("Éxito", "Competencias importadas correctamente.")

    # --- FUNCIONES DE AJUSTE DE UI ---

    def _ajustar_altura(self, event=None):
        widget = event.widget
        if not widget:
            return
        try:
            lineas = int(widget.count("1.0", "end", "displaylines")[0])
        except Exception:
            lineas = int(widget.index("end-1c").split(".")[0])
        
        if not hasattr(widget, "altura_minima"):
            widget.altura_minima = int(widget.cget("height"))
        
        nueva_altura = min(max(lineas, widget.altura_minima), 15)
        widget.configure(height=nueva_altura)

    def _actualizar_scroll(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def _ajustar_ancho_canvas(self, event):
        self.canvas.itemconfig(self.frame_id, width=event.width)