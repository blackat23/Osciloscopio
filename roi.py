import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
import datetime as date
from pathlib import Path
import serial
import time
import pandas as pd

arduino = serial.Serial(port='COM9', baudrate=9600, timeout=.01)

def enviar_datos_serial(valor):
    # Enviar el valor como un string con salto de línea para que Arduino lo lea con readStringUntil('\n')
    arduino.write(f"{valor}\n".encode())
    time.sleep(0.01)  # Añadir un pequeño delay para asegurar que los datos lleguen bien

def guardar_y_enviar():
    global arreglo_y
    x = [i for i in range(500)]  # Generar el array de tiempos
    datos = zip(x, arreglo_y)  # Combinar el tiempo con los valores de la señal
    
    for _, y in datos:
        valor_a_enviar = int(y)  
        enviar_datos_serial(valor_a_enviar)
    
    print("Datos enviados a Arduino.")

def leer_y_graficar_csv():
    global ax
    file_path = tk.filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    
    if file_path:
        try:
            # Leer el archivo CSV, sin encabezados
            data = pd.read_csv(file_path, header=None, names=['x', 'y'])
            
            ax.clear()
            ax.set_facecolor('#000000')
            ax.plot(data['x'], data['y'], color='#FF5733')  # Graficar desde CSV con color diferente
            ax.grid(True, which='both', color='white', linestyle='--')

            ax.set_title(f'Gráfica desde {Path(file_path).name}', color='white')
            ax.set_xlabel('Tiempo (s)', color='white')
            ax.set_ylabel('Amplitud (V)', color='white')
            canvas.draw()
        except Exception as e:
            print(f"Error al leer el archivo: {e}")

def generar_senal(tipo, frecuencia, amplitud, offset=0):
    t = np.linspace(0, 1, 500)
    if tipo == "sinusoidal":
        y = amplitud * np.sin(2 * np.pi * frecuencia * t) + offset
    elif tipo == "cuadrada":
        y = amplitud * np.sign(np.sin(2 * np.pi * frecuencia * t)) + offset
    elif tipo == "triangular":
        y = (2 * amplitud / np.pi) * np.arcsin(np.sin(2 * np.pi * frecuencia * t)) + offset
    return t, y

def actualizar_grafica():
    global frecuencia, amplitud, tipo_senal_actual, offset
    global arreglo_y
    t, y = generar_senal(tipo_senal_actual, frecuencia, amplitud, offset)
    arreglo_y = y.tolist()
    ax.clear()
    ax.set_facecolor('#000000')  # Fondo negro
    ax.plot(t, y, color='#00FF00')  # Señal verde
    ax.grid(True, which='both', color='white', linestyle='--')  
    
    ax.set_xlim(0, 1)  
    ax.set_ylim(0, 260)  # Cambiado de -256, 256 a 0, 260
    
    ax.set_xticks(np.linspace(0, 1, 11))  
    ax.set_yticks(np.linspace(0, 260, 11))  # Cambiado para que las marcas Y estén entre 0 y 260

    ax.set_title(f'Señal {tipo_senal_actual.capitalize()}', color='white')
    ax.set_xlabel('Tiempo (s)', color='white')  
    ax.set_ylabel('Amplitud (V)', color='white')  
    
    canvas.draw()

def calcular_voltaje_max():
    global arreglo_y, voltajemax
    valor_maximo_y = max(arreglo_y)  # Obtén el valor máximo de y
    voltajemax = (5 / 255) * valor_maximo_y  # Calcula el voltaje máximo
    print(f"El voltaje máximo es: {voltajemax} V")

def aumentar_offset():
    global offset
    offset += 1
    variable_offset.set(offset)
    actualizar_grafica()
    calcular_voltaje_max()
    


def disminuir_offset():
    global offset
    offset -= 1
    variable_offset.set(offset)
    actualizar_grafica()
    calcular_voltaje_max()

def cambio_offset():
    global offset
    try:
        offset = int(variable_offset.get()) 
        actualizar_grafica()
    except ValueError:
        print("Por favor, introduce un número válido para el offset.")

def aumentar_frecuencia():
    global frecuencia
    frecuencia += 1
    variablefre.set(frecuencia)
    actualizar_grafica()
    calcular_voltaje_max()

def disminuir_frecuencia():
    global frecuencia
    frecuencia -= 1
    variablefre.set(frecuencia)
    actualizar_grafica()
    calcular_voltaje_max()

def cambio_fre():
    global frecuencia
    try:
        frecuencia = int(variablefre.get()) 
        actualizar_grafica()
    except ValueError:
        print("Por favor, introduce un número válido para la frecuencia.")

def aumentar_amplitud():
    global amplitud
    amplitud += 1
    variableam.set(amplitud)
    actualizar_grafica()
    calcular_voltaje_max()

def disminuir_amplitud():
    global amplitud
    amplitud -= 1
    variableam.set(amplitud)
    actualizar_grafica()
    calcular_voltaje_max()

def cambio_am():
    global amplitud
    try:
        amplitud = int(variableam.get()) 
        actualizar_grafica()
    except ValueError:
        print("Por favor, introduce un número válido para la amplitud.")
        calcular_voltaje_max()
    
def seleccionar_senal(tipo):
    global tipo_senal_actual
    tipo_senal_actual = tipo
    actualizar_grafica()

def cerrar():
    root.quit()  
    root.destroy()  

def guardar():
    global arreglo_y
    x = [i for i in range(500)]
    fecha = date.datetime.now()
    texto = ""

    for j in range(500):
        texto += f"{x[j]},{arreglo_y[j]}\n"
        
    p = Path(f'carpeta1/grafica{fecha.hour}{fecha.minute}{fecha.second}.csv')
    p.write_text(texto)
    print(f"Datos guardados en {p}")


# Variables iniciales
frecuencia = 100
amplitud = 125
arreglo_y = [0] * 500
tipo_senal_actual = "sinusoidal"
offset = 125
voltajemax=0

# En la interfaz, añadir controles para el offset

# Configuración de la ventana principal
# Configuración de la ventana principal
root = tk.Tk()
root.configure(bg="gray")
root.title("Generador de Señales")

fig, ax = plt.subplots(figsize=(8, 5), dpi=150)
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Frame para controles de señal
frame_controles = tk.Frame(root, bg="gray")
frame_controles.pack(side=tk.RIGHT, fill=tk.Y, padx=10, pady=10)

# Frame para opciones de guardado y lectura
frame_guardar_leer = tk.Frame(root, bg="gray")
frame_guardar_leer.pack(side=tk.BOTTOM, fill=tk.Y, padx=10, pady=10)

# Controles de señal en frame_controles
tk.Button(frame_controles, text="Sinusoidal", command=lambda: seleccionar_senal("sinusoidal"),
          width=10, height=3, bg="#BBBBBB", fg="black").pack(padx=10, pady=5)
tk.Button(frame_controles, text="Cuadrada", command=lambda: seleccionar_senal("cuadrada"),
          width=10, height=3, bg="#BBBBBB", fg="black").pack(padx=10, pady=5)
tk.Button(frame_controles, text="Triangular", command=lambda: seleccionar_senal("triangular"),
          width=10, height=3, bg="#BBBBBB", fg="black").pack(padx=10, pady=5)

variablefre = tk.StringVar()
variablefre.set(frecuencia)
tk.Label(frame_controles, text="Frecuencia:", bg="gray", fg="white").pack(pady=10)
tk.Entry(frame_controles, textvariable=variablefre, bg="gray", fg="white").pack(pady=10)
tk.Button(frame_controles, text="Cambiar Frecuencia", command=cambio_fre, width=15, height=2,
          bg="#BBBBBB", fg="black").pack(pady=5)
tk.Button(frame_controles, text="+", command=aumentar_frecuencia, width=5, height=2,
          bg="#BBBBBB", fg="black").pack(pady=5)
tk.Button(frame_controles, text="-", command=disminuir_frecuencia, width=5, height=2,
          bg="#BBBBBB", fg="black").pack(pady=5)

variableam = tk.StringVar()
variableam.set(amplitud)
tk.Label(frame_controles, text="Amplitud:", bg="gray", fg="white").pack(pady=10)
tk.Entry(frame_controles, textvariable=variableam, bg="gray", fg="white").pack(pady=10)
tk.Button(frame_controles, text="Cambiar Amplitud", command=cambio_am, width=15, height=2,
          bg="#BBBBBB", fg="black").pack(pady=5)
tk.Button(frame_controles, text="+", command=aumentar_amplitud, width=5, height=2,
          bg="#BBBBBB", fg="black").pack(pady=5)
tk.Button(frame_controles, text="-", command=disminuir_amplitud, width=5, height=2,
          bg="#BBBBBB", fg="black").pack(pady=5)

variable_offset = tk.StringVar()
variable_offset.set(offset)
tk.Label(frame_controles, text="Offset:", bg="gray", fg="white").pack(pady=10)
tk.Entry(frame_controles, textvariable=variable_offset, bg="gray", fg="white").pack(pady=10)
tk.Button(frame_controles, text="Cambiar Offset", command=cambio_offset, width=15, height=2,
          bg="#BBBBBB", fg="black").pack(pady=5)
tk.Button(frame_controles, text="+", command=aumentar_offset, width=5, height=2,
          bg="#BBBBBB", fg="black").pack(pady=5)
tk.Button(frame_controles, text="-", command=disminuir_offset, width=5, height=2,
          bg="#BBBBBB", fg="black").pack(pady=5)

# Controles de guardado y lectura en frame_guardar_leer
tk.Label(frame_guardar_leer, text="VoltajeMax:", bg="gray", fg="white").pack(pady=10)
tk.Entry(frame_guardar_leer, textvariable=voltajemax, bg="gray", fg="white").pack(pady=10)
tk.Button(frame_guardar_leer, text="Guardar", command=guardar, width=12, height=2,
          bg="#BBBBBB", fg="black").pack(pady=5)
tk.Button(frame_guardar_leer, text="Guardar y enviar", command=guardar_y_enviar, width=12, height=2,
          bg="#BBBBBB", fg="black").pack(pady=5)
tk.Button(frame_guardar_leer, text="Abrir CSV", command=leer_y_graficar_csv, width=12, height=2,
          bg="#BBBBBB", fg="black").pack(pady=5)

root.protocol("WM_DELETE_WINDOW", cerrar)

actualizar_grafica()
root.mainloop()