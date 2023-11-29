from google.cloud import storage
import os
from cryptography.fernet import Fernet
import base64
import tkinter as tk

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = 'cred.json'  # Credenciales Cloud Google

def descargar_archivo(bucket_name, nombre_archivo, ruta_local):
    client = storage.Client()
    bucket = client.get_bucket(bucket_name)
    blob = bucket.blob(nombre_archivo)
    blob.download_to_filename(ruta_local)
    print(f"Se descargó el archivo {nombre_archivo} en {ruta_local}")

def actualizar_contenido():
    descargar_archivo('criptoteltesting2023', 'datos_sensor.txt', 'texto.txt')
    descargar_archivo('criptoteltesting2023', 'clave_sensor', 'clave.txt')

    with open('clave.txt', 'rb') as file:
        clave = file.read()
    with open('texto.txt', 'rb') as file:
        texto = file.read()

    cipher_suite = Fernet(clave)
    texto_desencriptado = cipher_suite.decrypt(texto)
    texto_decodificado = texto_desencriptado.decode('utf-8')

    # Actualizar etiquetas o elementos de la interfaz con los nuevos valores
    etiqueta_clave.config(text=clave)
    etiqueta_texto.config(text=texto_decodificado)

# Crear la interfaz gráfica
ventana = tk.Tk()
ventana.title("Visualización de Archivos")

# Crear etiquetas para mostrar el contenido de clave.txt y texto.txt
etiqueta_clave = tk.Label(ventana, text="")
etiqueta_clave.pack()

etiqueta_texto = tk.Label(ventana, text="")
etiqueta_texto.pack()

# Botón para actualizar el contenido
boton_actualizar = tk.Button(ventana, text="Actualizar", command=actualizar_contenido)
boton_actualizar.pack()

# Ejecutar el bucle principal de la interfaz gráfica
ventana.mainloop()