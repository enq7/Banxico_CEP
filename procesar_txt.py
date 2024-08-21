import re
import tkinter as tk
from tkinter import filedialog

def seleccionar_archivo():
    root = tk.Tk()
    root.withdraw()
    archivo_seleccionado = filedialog.askopenfilename(filetypes=[("Archivos de texto", "*.txt")])
    return archivo_seleccionado

def extraer_datos(linea):
    fecha = re.search(r"\d{4}-\d{2}-\d{2}", linea)
    fecha = fecha.group() if fecha else None

    clave_rastreo = re.search(r"\b\d{24}\b", linea)
    clave_rastreo = clave_rastreo.group() if clave_rastreo else None

    clabe_proveedor = re.search(r"\b\d{18}\b", linea)
    clabe_proveedor = clabe_proveedor.group() if clabe_proveedor else None
    
    monto = re.search(r"\d+\.\d{2}", linea)
    monto = monto.group() if monto else None
    
    constante_1 = "40012"
    constante_2 = "40" + clabe_proveedor[:3] if clabe_proveedor else None
    
    if fecha and clave_rastreo and clabe_proveedor and monto and constante_2:
        return f"{fecha},{clave_rastreo},{constante_1},{constante_2},{clabe_proveedor},{monto}"
    else:
        return None

def procesar_archivo(ruta_archivo):
    with open(ruta_archivo, 'r') as archivo:
        lineas = archivo.readlines()

    resultados = []
    for linea in lineas:
        linea_procesada = extraer_datos(linea)
        if linea_procesada:
            resultados.append(linea_procesada)
    
    return resultados, len(lineas)

def guardar_resultado(resultados, total_lineas):
    procesadas = len(resultados)
    
    for resultado in resultados:
        print(resultado)
    
    print(f"\n{procesadas} líneas procesadas de {total_lineas} líneas leídas.")
    
    confirmar = input("\n¿La información es correcta? (s/n): ")
    if confirmar.lower() == 's':
        ruta_guardado = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Archivos de texto", "*.txt")])
        if ruta_guardado:
            with open(ruta_guardado, 'w') as archivo:
                for resultado in resultados:
                    archivo.write(resultado + '\n')
            print(f"Archivo guardado en: {ruta_guardado}")