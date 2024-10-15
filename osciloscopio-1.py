import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Button
import serial
import time

# Conectar al puerto serial del Arduino (cambiar por el puerto correcto)
ser = serial.Serial('COM5', 9600, timeout=1)
time.sleep(2)  # Tiempo para que el Arduino inicie
t_data = []
pot_data = []
start_time = time.time()
is_paused = False  # Estado de la animación
current_index = 0  # Índice para movernos en la gráfica cuando está en pausa

# Inicializar la gráfica
fig, ax = plt.subplots()
line, = ax.plot([], [], color='green', lw=2)
ax.set_xlim(0, 10)  # Eje X (tiempo) en segundos
ax.set_ylim(0, 1023)  # Eje Y (valor del potenciómetro)
ax.set_facecolor('#000000')
ax.grid(True, which='both', color='white', linestyle='--')

# Crear botones para pausar/reanudar, avanzar y retroceder en el tiempo
pause_ax = plt.axes([0.7, 0.01, 0.1, 0.05])  # Eje para el botón de pausa
pause_button = Button(pause_ax, 'Pausa', color='lightgray', hovercolor='gray')

forward_ax = plt.axes([0.81, 0.01, 0.08, 0.05])  # Eje para el botón de avanzar
forward_button = Button(forward_ax, 'Adelante', color='lightgray', hovercolor='gray')

backward_ax = plt.axes([0.61, 0.01, 0.08, 0.05])  # Eje para el botón de retroceder
backward_button = Button(backward_ax, 'Atrás', color='lightgray', hovercolor='gray')

# Función que actualiza la gráfica
def update(frame):
    global current_index

    if is_paused:  # Si está en pausa, no actualizar con nuevos datos
        return line,

    # Leer el valor desde el puerto serial
    try:
        pot_value = ser.readline().decode('utf-8').strip()  # Leer dato del serial
        if pot_value:
            pot_value = int(pot_value)  # Convertir a entero
            current_time = time.time() - start_time
            t_data.append(current_time)
            pot_data.append(pot_value)
            current_index = len(t_data) - 1  # Actualizar el índice actual

            # Actualizar los datos en la gráfica
            line.set_data(t_data, pot_data)

            # Ajustar límites del eje X para que se mueva con el tiempo
            ax.relim()
            ax.autoscale_view()

            if current_time > 10:
                ax.set_xlim(current_time - 10, current_time)

    except Exception as e:
        print(f"Error: {e}")

    return line,

# Función para manejar el botón de pausa
def toggle_pause(event):
    global is_paused
    is_paused = not is_paused
    if is_paused:
        pause_button.label.set_text('Reanudar')
    else:
        pause_button.label.set_text('Pausa')

# Función para avanzar en el tiempo cuando la animación está en pausa
def move_forward(event):
    global current_index
    if is_paused and current_index < len(t_data) - 1:  # Avanzar solo si no estamos al final
        current_index += 10
        ax.set_xlim(t_data[current_index] - 10, t_data[current_index])  # Actualizar la vista
        line.set_data(t_data[:current_index + 1], pot_data[:current_index + 1])
        fig.canvas.draw()

# Función para retroceder en el tiempo cuando la animación está en pausa
def move_backward(event):
    global current_index
    if is_paused and current_index > 0:  # Retroceder solo si no estamos al inicio
        current_index -= 10
        ax.set_xlim(t_data[current_index] - 10, t_data[current_index])  # Actualizar la vista
        line.set_data(t_data[:current_index + 1], pot_data[:current_index + 1])
        fig.canvas.draw()

# Conectar los botones con sus respectivas funciones
pause_button.on_clicked(toggle_pause)
forward_button.on_clicked(move_forward)
backward_button.on_clicked(move_backward)

# Animar la gráfica
ani = FuncAnimation(fig, update, interval=0.1)  # Actualiza cada 1ms

# Etiquetas


# Mostrar gráfica
plt.show()

# Cerrar la conexión serial al terminar
ser.close()
