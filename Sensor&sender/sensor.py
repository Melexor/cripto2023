import random
import time
from datetime import datetime
import tkinter as tk
import threading
contador_mediciones = 0
def reiniciar_y_enviar():
    global contador_mediciones
    if contador_mediciones == 24:
        with open("senal_envio.txt", "w") as senal:
            senal.write("Enviar")
            print("pumba")
    time.sleep(5)
    with open("datos_sensor.txt", "w") as archivo:
        archivo.write("Hora, Temperatura (°C)\n")
    contador_mediciones = 0
def actualizar_interfaz():
    with open("datos_sensor.txt", "r") as archivo:
        datos = archivo.read()
    etiqueta.config(text=datos)

def simular_sensor():
    global contador_mediciones
    def crear_interfaz():
        ventana = tk.Tk()
        ventana.title("Datos del Sensor")

        global etiqueta
        etiqueta = tk.Label(ventana, font=("Arial", 12), justify="left")
        etiqueta.pack(padx=20, pady=20)
        ventana.mainloop()
    thread_interfaz = threading.Thread(target=crear_interfaz)
    thread_interfaz.start()
    reiniciar_y_enviar()
    while True:
        temperatura = round(random.uniform(0, 35), 2)
        # Obtener la hora actual
        hora_actual = datetime.now().strftime("%H:%M:%S")  # Formato: HH:MM:SS
        with open("datos_sensor.txt", "a") as archivo:
            archivo.write(f"{hora_actual}, {temperatura}\n")
        contador_mediciones += 1
        if contador_mediciones == 24:
            reiniciar_y_enviar()
        else:
            with open("senal_envio.txt", "w") as senal:
                senal.write("Esperar")
                print("espero")
        actualizar_interfaz()
        time.sleep(0.3)
thread_sensor = threading.Thread(target=simular_sensor)
thread_sensor.start()
