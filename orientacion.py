from sympy import expand, Eq, Mul, Add

def horizontal_canonic(x, h, a, y, k, b):
    print("Como el eje es Horizontal utilizaremos esta Forma Canónica")
    expresion = (((x - h)**2) / a**2 + ((y - k)**2) / b**2)
    return Eq(expresion, 1)

def vertical_canonic(x, h, a, y, k, b):
    print("Como el eje es Vertical utilizaremos esta Forma Canónica")
    expresion = (((x - h)**2) / b**2 + ((y - k)**2) / a**2)
    return Eq(expresion, 1)

def horizontal_general(x, h, a, y, k, b):
    # paso 1
    expresion1 = (b**2)*(x - h)**2 + (a**2)*(y - k)**2
    # paso 2
    expresion2, expresion3 = factorizar(x, h, y, k)
    termino1 = Mul(b**2, expresion2, evaluate=False)
    termino2 = Mul(a**2, expresion3, evaluate=False)
    expresion4 = Add(termino1, termino2, evaluate=False)
    # paso 3
    expresion5 = expand(expresion4)
    # paso 4
    expresion6 =  expresion5 - 1

    return Eq(expresion1, 1), Eq(expresion4, 1), Eq(expresion5, 1), Eq(expresion6, 0)

def vertical_general(x, h, a, y, k, b):
    # paso 1
    expresion1 = (a**2)*(x - h)**2 + (b**2)*(y - k)**2
    # paso 2
    expresion2, expresion3 = factorizar(x, h, y, k)
    termino1 = Mul(a**2, expresion2, evaluate=False)
    termino2 = Mul(b**2, expresion3, evaluate=False)
    expresion4 = Add(termino1, termino2, evaluate=False)
    # paso 3
    expresion5 = expand(expresion4)
    # paso 4
    expresion6 =  expresion5 - 1

    return Eq(expresion1, 1), Eq(expresion4, 1), Eq(expresion5, 1), Eq(expresion6, 0)


def factorizar(x,h,y,k):
    primera = expand((x - h)**2)
    segunda = expand((y - k)**2)
    return primera, segunda