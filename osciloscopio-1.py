import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import serial
import time
#comentario de prueba
#prueba 2 
# Conectar al puerto serial del Arduino (cambiar por el puerto correcto)
ser = serial.Serial('COM7', 9600, timeout=1)
time.sleep(2)  # Tiempo para que el Arduino inicie

# Crear listas para almacenar tiempo y valores
#prueba numero 3, ultima prueba de comentarios
t_data = []
pot_data = []
start_time = time.time()

# Inicializar la gráfica
fig, ax = plt.subplots()
line, = ax.plot([], [], color='red', lw=2)
ax.set_xlim(0, 10)  # Eje X (tiempo) en segundos
ax.set_ylim(0, 1023)  # Eje Y (valor del potenciómetro)

# Función que actualiza la gráfica
def update(frame):
    # Leer el valor desde el puerto serial
    try:
        pot_value = ser.readline().decode('utf-8').strip()  # Leer dato del serial
        if pot_value:
            pot_value = int(pot_value)  # Convertir a entero
            current_time = time.time() - start_time
            t_data.append(current_time)
            pot_data.append(pot_value)

            # Actualizar los datos en la gráfica
            line.set_data(t_data, pot_data)
            
            # Ajustar límites del eje X para que se mueva con el tiempo
            ax.relim()
            ax.autoscale_view()

            if current_time > 10:
                ax.set_xlim(current_time - 10, current_time)

    except Exception as e:
        print(f"Error : {e}")

    return line,

# Animar la gráfica
ani = FuncAnimation(fig, update, interval=1)  # Actualiza cada 100ms

# Etiquetas
plt.xlabel('Tiempo (s)')
plt.ylabel('Valor del potenciómetro2')
plt.title('Lectura del potenciómetro en tiempo real')

# Mostrar gráfica
plt.show()
print(line)

# Cerrar la conexión serial al terminar
ser.close()
