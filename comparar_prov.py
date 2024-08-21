import re
import tkinter as tk
from tkinter import filedialog
import os
from PyPDF2 import PdfReader

def seleccionar_archivo():
    root = tk.Tk()
    root.withdraw()
    archivo_seleccionado = filedialog.askopenfilename(filetypes=[("Archivos de texto", "*.txt")])
    return archivo_seleccionado

def seleccionar_carpeta():
    root = tk.Tk()
    root.withdraw()
    carpeta_seleccionada = filedialog.askdirectory()
    return carpeta_seleccionada

def extraer_proveedor_y_clave(linea):
    proveedor = re.search(r"[A-Z\s]{31}", linea)
    proveedor = proveedor.group().strip() if proveedor else None

    clave_rastreo = re.search(r"\b\d{24}\b", linea)
    clave_rastreo = clave_rastreo.group() if clave_rastreo else None

    if proveedor and clave_rastreo:
        return proveedor, clave_rastreo
    else:
        return None, None

def procesar_extracto(ruta_archivo):
    with open(ruta_archivo, 'r') as archivo:
        lineas = archivo.readlines()

    proveedores_encontrados = []
    total_lineas = len(lineas)

    for linea in lineas:
        proveedor, clave_rastreo = extraer_proveedor_y_clave(linea)
        if proveedor and clave_rastreo:
            proveedores_encontrados.append((proveedor, clave_rastreo))

    return proveedores_encontrados, total_lineas

def comparar_proveedores():
    print("Selecciona el archivo del extracto bancario:\n")
    ruta_archivo = seleccionar_archivo()

    if ruta_archivo:
        proveedores_encontrados, total_lineas = procesar_extracto(ruta_archivo)

        if proveedores_encontrados:
            for proveedor, clave_rastreo in proveedores_encontrados:
                print(f"{proveedor} - {clave_rastreo}")

            print(f"\n{len(proveedores_encontrados)} líneas procesadas de {total_lineas} líneas leídas.")

            confirmar = input("\n¿La información es correcta? (s/n): ")
            if confirmar.lower() == 's':
                print("Selecciona la carpeta donde están los archivos PDF:\n")
                ruta_carpeta = seleccionar_carpeta()

                if ruta_carpeta:
                    comparar_con_pdfs(ruta_carpeta, proveedores_encontrados)
            else:
                print("Operación cancelada por el usuario.")
        else:
            print("No se encontraron proveedores en el archivo.")
    else:
        print("No se seleccionó ningún archivo.")

def comparar_con_pdfs(carpeta, proveedores_encontrados):
    todos_coinciden = True

    for archivo in os.listdir(carpeta):
        if archivo.endswith(".pdf"):
            for proveedor, clave_rastreo in proveedores_encontrados:
                if clave_rastreo in archivo:
                    ruta_pdf = os.path.join(carpeta, archivo)
                    titular_cuenta = buscar_titular_en_pdf(ruta_pdf, proveedor)

                    if titular_cuenta:
                        if titular_cuenta[:30].strip().upper() != proveedor[:30].strip().upper():
                            print(f"{titular_cuenta[:30].strip()} - {proveedor[:30].strip()} - INCORRECTO")
                            todos_coinciden = False
    if todos_coinciden:
        print("Todos los proveedores coinciden")


def buscar_titular_en_pdf(ruta_pdf, proveedor):
    try:
        reader = PdfReader(ruta_pdf)
        texto_completo = ""
        for page in reader.pages:
            texto_completo += page.extract_text()

        lineas = texto_completo.splitlines()
        if len(lineas) >= 30:
            nombre_titular = lineas[29].strip()

            if nombre_titular[:30].strip().upper() == proveedor[:30].strip().upper():
                return nombre_titular[:30].strip()

            if len(nombre_titular) < 30 and len(lineas) > 30:
                nombre_titular += " " + lineas[30].strip()

            return nombre_titular[:30].strip()

    except Exception as e:
        print(f"Error al procesar {ruta_pdf}: {e}")
    return None