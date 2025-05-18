from rut import convertir_rut
from conicas import Canonica, convertir
while True:
    print("""
Cuantas Formas Canonicas Necesitas Crear?
    1.- 1
    2.- 2
    3.- Salir
""")
    try:
        opcion = int(input("escoja una opcion: "))
    except ValueError:
        print("Por favor, ingrese un número válido.")
        continue

    if opcion == 1:
        rut = input("ingrese su rut: ")
        datos = convertir_rut(rut)
        grupo = int(input("ingrese su grupo: "))

        while True:
            print("""
Ahora que tenemos su rut y su grupo, escoja que quiere hacer:
    1.- Forma Canonica
    2.- Forma General
    3.- Cambiar Rut
    4.- Cambiar grupo
    5.- Salir
            """)
            try:
                opcion2 = int(input("escoja una opcion: "))
            except ValueError:
                print("Por favor, ingrese un número válido.")
                continue

            if opcion2 == 1:
                expresion, h, k, a, b, ejeFocal = Canonica(datos, grupo)
                print(expresion)
            elif opcion2 == 2:
                canonic, h, k, a, b, ejeFocal = Canonica(datos, grupo)
                convertir(canonic, h, k, a, b, ejeFocal)
            elif opcion2 == 3:
                rut = input("ingrese su rut: ")
                datos = convertir_rut(rut)
            elif opcion2 == 4:
                grupo = int(input("ingrese su grupo: "))
            elif opcion2 == 5:
                break
            else:
                print("escoja otra opcion")

    elif opcion == 2:
        rut1 = input("ingrese el 1er rut: ")
        rut2 = input("ingrese el 2do rut: ")
        datos1 = convertir_rut(rut1)
        datos2 = convertir_rut(rut2)
        grupo = int(input("ingrese su grupo: "))

        while True:
            print("""
Ahora que tenemos sus ruts y grupo, escoja que quiere hacer:
    1.- Forma Canonica
    2.- Forma General
    3.- Cambiar Ruts
    4.- Cambiar grupo
    5.- Salir
            """)
            try:
                opcion2 = int(input("escoja una opcion: "))
            except ValueError:
                print("Por favor, ingrese un número válido.")
                continue

            if opcion2 == 1:
                expresion1, h, k, a, b, ejeFocal = Canonica(datos1, grupo)
                expresion2, h, k, a, b, ejeFocal = Canonica(datos2, grupo)
                print("1era Forma Canonica")
                print(expresion1)
                print("2da Forma Canonica")
                print(expresion2)
            elif opcion2 == 2:
                canonic1, h, k, a, b, ejeFocal = Canonica(datos1, grupo)
                canonic2, h, k, a, b, ejeFocal = Canonica(datos2, grupo)
                print("Forma Canonica 1")
                convertir(canonic1, h, k, a, b, ejeFocal)
                print("Forma Canonica 2")
                convertir(canonic2, h, k, a, b, ejeFocal)
            elif opcion2 == 3:
                rut1 = input("ingrese el 1er rut: ")
                rut2 = input("ingrese el 2do rut: ")
                datos1 = convertir_rut(rut1)
                datos2 = convertir_rut(rut2)
            elif opcion2 == 4:
                grupo = int(input("ingrese su grupo: "))
            elif opcion2 == 5:
                break
            else:
                print("escoja otra opcion")

    elif opcion == 3:
        break
    else:
        print("escoja una opcion correcta")
