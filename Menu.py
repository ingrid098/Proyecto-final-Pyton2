# PROYECTO FINAL PYTHON 2
# Validar la entrada del usuario
while True:
    print("\n---------------Seleccione que tipo de dataset quiere analizar-------------\n")
    print("1. Dataset sobre el hundimiento del titanic")
    print("2. Dataset de ventas de una empresa automotriz")
    print("0. Salir")
    seleccion = input("\nSelecciona una opcion:\n")
    try:
        if seleccion == "1":
            # Ejecutar el código de "titanic.py"
            try:
                with open('C:/Users/ingri/OneDrive/Escritorio/dataframe/Proyecto_Python2/titanic.py', 'r') as file:
                    codigo_titanic = file.read()
                    exec(codigo_titanic)
            except FileNotFoundError:
                print("Archivo 'titanic.py' no encontrado en la ubicación especificada.")

        elif seleccion == "2":
            # Ejecutar el código de "titanic.py"
            try:
                with open('C:/Users/ingri/OneDrive/Escritorio/dataframe/Proyecto_Python2/Auto.py', 'r') as file:

                    codigo_Auto = file.read()
                    exec(codigo_Auto)
            except FileNotFoundError:
                print("Archivo 'titanic.py' no encontrado en la ubicación especificada.")

        elif seleccion == "0":
            print("Muchas gracias por tu participacion")
            break
        else:
            print("Opción no válida. Por favor, selecciona una opción válida.")

    except ValueError:
        print("Entrada no válida. Por favor, ingresa un número.")

    seleccion = input("\nSelecciona una opción:\n")

