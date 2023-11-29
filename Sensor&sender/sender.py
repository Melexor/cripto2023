import tkinter as tk
import threading
from google.cloud import storage
import os
import base64
from cryptography.fernet import Fernet

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = 'cred.json'  # Credenciales Cloud Google

def enviar_a_bucket(data, nombre_bucket, nombre_remoto):
    client = storage.Client()
    bucket = client.get_bucket(nombre_bucket)
    blob = bucket.blob(nombre_remoto)
    blob.upload_from_string(data)

def encriptar_y_guardar(texto, clave):
    cipher_suite = Fernet(clave)
    texto_encriptado = cipher_suite.encrypt(texto.encode())
    return texto_encriptado

def generar_clave():
    clave = Fernet.generate_key()
    return clave

def leer_senal_envio():
    try:
        with open("senal_envio.txt", "r") as archivo:
            senal = archivo.read().strip()
            etiqueta_senal.config(text=f"Señal de envío: {senal}")
            if senal == "Enviar":
                with open("datos_sensor.txt", "r") as archivo_datos:
                    contenido = archivo_datos.read()
                    clave = generar_clave()
                    print(clave)

                    # Enviar la clave al bucket
                    enviar_a_bucket(clave, "criptoteltesting2023", "clave_sensor")

                    # Decodificar la clave base64 para usarla
                    texto_encriptado = encriptar_y_guardar(contenido, clave)

                    # Almacenar el texto encriptado en Cloud Storage
                    enviar_a_bucket(texto_encriptado, "criptoteltesting2023", "datos_sensor.txt")
    except FileNotFoundError:
        etiqueta_senal.config(text="Archivo no encontrado")
    ventana.after(1000, leer_senal_envio)

ventana = tk.Tk()
ventana.title("Señal de Envío")
etiqueta_senal = tk.Label(ventana, font=("Arial", 12))
etiqueta_senal.pack(padx=20, pady=20)
thread_leer_senal = threading.Thread(target=leer_senal_envio)
thread_leer_senal.start()
ventana.mainloop()
