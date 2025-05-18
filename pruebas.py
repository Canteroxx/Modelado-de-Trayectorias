from sympy import symbols, Eq, expand, pprint, Mul, Add

def horizontal_general(x, h, a, y, k, b):
    # Paso 1: forma general
    expresion1 = (b**2)*(x - h)**2 + (a**2)*(y - k)**2 - 1

    # Paso 2: expandimos binomios, pero NO distribuimos los coeficientes
    binomio_x = expand((x - h)**2)
    binomio_y = expand((y - k)**2)

    # Usamos Mul con evaluate = False para evitar que multiplique
    termino1 = Mul(b**2, binomio_x, evaluate=False)
    termino2 = Mul(a**2, binomio_y, evaluate=False)
    expresion2 = Add(termino1, termino2, evaluate=False)  # mantiene la suma sin desarrollar

    # Paso 3: expansión total
    expresion3 = expand(expresion2)

    return Eq(expresion1, 0), Eq(expresion2, 0), Eq(expresion3, 0)

# Ejemplo
x, y = symbols('x y')
res1, res2, res3 = horizontal_general(x, 2, 12, y, 1, 13)

print("Paso 1:")
pprint(res1)
print("\nPaso 2:")
pprint(res2)
print("\nPaso 3:")
pprint(res3)
