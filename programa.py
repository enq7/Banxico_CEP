import os
import platform
from procesar_txt import seleccionar_archivo, procesar_archivo, guardar_resultado
from comparar_prov import comparar_proveedores

def procesar_txt():
    print("Selecciona el archivo txt a procesar:")
    ruta_archivo = seleccionar_archivo()

    if ruta_archivo:
        resultados, total_lineas = procesar_archivo(ruta_archivo)
        
        if resultados:
            guardar_resultado(resultados, total_lineas)
        else:
            print("No se encontraron datos válidos en el archivo.")
    else:
        print("No se seleccionó ningún archivo.")

def esperar_para_salir():
    print("\nPresiona cualquier tecla para terminar el programa...")
    
    if platform.system() == "Windows":
        import msvcrt
        msvcrt.getch()
    else:
        input()

def main():
    print("Seleccione lo que desea hacer:")
    print("1. Procesar archivo TXT")
    print("2. Comparar proveedores")
    
    opcion = input("Ingrese 1 o 2: ")

    if opcion == "1":
        procesar_txt()
    elif opcion == "2":
        comparar_proveedores()
    else:
        print("Opción no válida. Por favor, seleccione 1 o 2.")
    
    esperar_para_salir()

if __name__ == "__main__":
    main()
