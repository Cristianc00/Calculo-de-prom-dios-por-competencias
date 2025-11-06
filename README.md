# Cálculo de Promedios por Dimensiones

Aplicación desarrollada en **Python con Tkinter** para facilitar la evaluación por dimensiones de competencias.  
Permite registrar alumnos, asignar puntajes a cada dimensión, calcular promedios, guardar los resultados y exportar o importar descripciones de competencias.

## Instrucciones de instalación y ejecución

### Requisitos previos
- **Python 3.8 o superior**
- Librerías estándar de Python (no requiere instalación adicional):
  - `tkinter`
  - `json`
  - `csv`

### Instalación
1. Clonar o descargar el repositorio:
   ```bash
   git clone https://github.com/Cristianc00/Calculo-de-prom-dios-por-competencias
   ```
2. Ingresar al directorio del proyecto:
   ```bash
   cd promedios-por-dimensiones
   ```

### Ejecución
Ejecutar el archivo principal:
```bash
python main.py
```

La interfaz se abrirá automáticamente.  
Desde allí se pueden cargar, editar y exportar datos de alumnos y competencias.

## Descripción del diseño y decisiones de desarrollo

### Estructura general del proyecto
- **`main.py`**  
  Punto de entrada de la aplicación. Crea la instancia principal y ejecuta el bucle de Tkinter.
- **`app.py`**  
  Contiene toda la interfaz gráfica y la lógica central del programa. Maneja la interacción del usuario, el cálculo de promedios y la visualización dinámica.
- **`file_manager.py`**  
  Módulo separado para la gestión de archivos (lectura y escritura de JSON, CSV y TXT). Facilita el mantenimiento y la extensión futura.

### Diseño de la interfaz
- Se utiliza un **Canvas con barra de desplazamiento vertical**, permitiendo visualizar varias dimensiones en pantallas pequeñas.
- Los puntajes se eligen mediante **botones numéricos del 1 al 10**, que cambian de color al ser seleccionados.
- Cada dimensión cuenta con cuadros de texto independientes para describir competencias específicas.
- Se incluye un área inferior para mostrar el **promedio actual** y opciones de **guardar, agregar alumno y exportar datos**.

### Hitos principales del desarrollo
1. Implementación del sistema de selección de puntajes y cálculo automático de promedios.  
2. Incorporación del guardado de datos en distintos formatos (`.txt`, `.csv`, `.json`).  
3. Refactorización del código para separar la lógica de archivos en un módulo independiente.  
4. Integración de un **scroll** y ajuste automático de altura en los cuadros de texto.  
5. Diseño estético limpio, con colores pastel y tipografía legible.

## Justificación del uso de librerías elegidas

- **Tkinter:**  
  Se eligió por ser parte de la biblioteca estándar de Python, de fácil distribución y sin dependencias externas.  
  Permite desarrollar interfaces gráficas rápidas, ligeras y fácilmente personalizables para contextos educativos.

- **json / csv / io estándar:**  
  Se emplean las librerías nativas para garantizar compatibilidad y simplicidad en la lectura/escritura de datos.  
  JSON se utiliza para guardar estructuras jerárquicas (competencias y dimensiones), mientras que CSV/TXT son formatos más simples para exportar promedios de alumnos.

## Fundamento didáctico

### Aprendizajes y desafíos
El desarrollo de esta aplicación permitió comprender la relación entre **interfaces gráficas y estructuras de datos** en Python.  
Entre los principales aprendizajes destacan:
- Diseño modular: separar la interfaz, la lógica y la gestión de archivos.  
- Uso de eventos (`bind`) para lograr una interfaz más dinámica.  
- Control del tamaño y el desplazamiento de elementos mediante `Canvas` y `Frame`.

El mayor desafío fue implementar una interfaz adaptable que mantuviera claridad visual incluso con gran cantidad de información.

### Reflexión del proceso
El proyecto integra tanto la dimensión **técnica** como la **pedagógica**, al poner en práctica el diseño de herramientas digitales que faciliten procesos de evaluación.  
A través de este desarrollo se fortalecieron competencias en:
- Pensamiento computacional.
- Planificación de software educativo.
- Evaluación por dimensiones en el contexto docente.

La experiencia demostró que la programación puede ser de gran ayuda para mejorar la organización y la transparencia en la evaluación formativa.

## Futuras mejoras
- Incorporar una base de datos local (SQLite) para gestionar historiales de alumnos.  
- Añadir opciones de personalización de escalas de puntaje.  
- Permitir exportación en formato PDF.  
- Implementar un modo oscuro o tema de contraste alto para accesibilidad.

## Autores
Proyecto desarrollado por **Juan Rondán** y **Cristian Carro** 
Estudiantes de Profesorado de Informática – CERP Suroeste, Colonia del Sacramento (Uruguay).

## Licencia
Este proyecto se distribuye bajo licencia **MIT**, permitiendo su libre uso y modificación con fines educativos.
