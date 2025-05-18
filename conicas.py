from sympy import symbols, pretty, pprint
from orientacion import horizontal_canonic, horizontal_general, vertical_canonic, vertical_general

def Canonica(lista, grupo):
    h, k = lista[0] , lista[1]
    x, y = symbols('x y')
    if grupo % 2 == 0:
        ejeFocal = lista[3]
        a, b = lista[5] + lista[6], lista[7] + lista[2]
        if ejeFocal % 2 == 0:
            expresion = horizontal_canonic(x,h,a,y,k,b)
        else:
            expresion = vertical_canonic(x,h,a,y,k,b)
    else:
        ejeFocal = lista[6]
        a, b = lista[2] + lista[3], lista[4] + lista[5]
        if ejeFocal % 2 == 0:
            expresion = horizontal_canonic(x,h,a,y,k,b)
        else:
            expresion = vertical_canonic(x,h,a,y,k,b)

    return pretty(expresion), h, k, a, b, ejeFocal

def convertir(expresion, h, k, a, b, ejeFocal):
    x, y = symbols('x y')
    print(f"Vamos a convertir la siguiente expresion a forma General")
    print(expresion)
    if ejeFocal % 2 == 0:
        exp1, exp2, exp3, exp4 = horizontal_general(x, h, a, y, k, b)
        print("Paso 1:")
        pprint(exp1)
        print("\nPaso 2:")
        pprint(exp2)
        print("\nPaso 3:")
        pprint(exp3)
        print("\nPaso 4:")
        pprint(exp4)
    else:
        exp1, exp2, exp3, exp4 = vertical_general(x, h, a, y, k, b)
        print("Paso 1:")
        pprint(exp1)
        print("\nPaso 2:")
        pprint(exp2)
        print("\nPaso 3:")
        pprint(exp3)
        print("\nPaso 4:")
        pprint(exp4)