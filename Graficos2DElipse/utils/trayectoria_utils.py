def ecuacion_canonica(tr):
    h, k, a, b = tr.h, tr.k, tr.a, tr.b
    return r"\frac{(x-%s)^2}{%s^2} + \frac{(y-%s)^2}{%s^2} = 1" % (h, a, k, b)

def ecuacion_general(tr):
    h, k, a, b = tr.h, tr.k, tr.a, tr.b
    if tr.orientacion == 'vertical':
        a, b = b, a

    A = b ** 2
    B = a ** 2
    D = -2 * b ** 2 * h
    E = -2 * a ** 2 * k
    F = b ** 2 * h ** 2 + a ** 2 * k ** 2 - a ** 2 * b ** 2

    terms = [
        f"{A}x^2",
        f" + {B}y^2",
        f"{'+' if D >= 0 else '-'} {abs(D)}x",
        f"{'+' if E >= 0 else '-'} {abs(E)}y",
        f"{'+' if F >= 0 else '-'} {abs(F)}"
    ]
    return  " ".join(terms) + " = 0"

def excentricidad(a, b):
    if a < b:
        a, b = b, a
    return (1 - (b ** 2) / (a ** 2)) ** 0.5

def distancia_focal(a, b):
    if a < b:
        a, b = b, a
    return (a ** 2 - b ** 2) ** 0.5

def focos(h, k, a, b, tipo=None):
    if tipo == 'horizontal':
        dx = distancia_focal(a, b)
        F1 = (h + dx, k)
        F2 = (h - dx, k)
    else:
        dx = distancia_focal(a, b)
        F1 = (h, k + dx)
        F2 = (h, k - dx)
    return F1, F2

def vertices(h, k, a, b, tipo=None):

    if tipo == 'horizontal':
        dx = a
        V1 = (h + dx, k)
        V2 = (h - dx, k)

        dy = b
        V3 = (h, k + dy)
        V4 = (h, k - dy)

    else:
        dy = b
        V1 = (h, k + dy)
        V2 = (h, k - dy)

        dx = a
        V3 = (h + dx, k)
        V4 = (h - dx, k)
    return V1, V2, V3, V4

def lados_rectos(a, b):
    return (2 * b ** 2 / a)

def parametros_elipse(tr):
    h, k, a, b, tipo = tr.h, tr.k, tr.a, tr.b, tr.orientacion
    e = excentricidad(a, b)
    c = distancia_focal(a, b)
    F1, F2 = focos(h, k, a, b)
    V1, V2, V3, V4 = vertices(h, k, a, b)
    lado_recto = lados_rectos(a, b)
    return {
        "centro": (h, k),
        "semieje_mayor": max(a, b),
        "semieje_menor": min(a, b),
        "tipo": tipo,
        "excentricidad": e,
        "distancia_focal": c,
        "focos": (F1, F2),
        "vertices_mayor": (V1, V2),
        "vertices_menor": (V3, V4),
        "lado_recto": lado_recto
    }

def texto_parametros_elipse(parametros):
    tipo = parametros["tipo"]
    txt = f"""<b>Tipo:</b> {tipo.capitalize()}<br>
    <b>Centro:</b> {parametros['centro']}<br>
    <b>Semieje mayor (a):</b> {parametros['semieje_mayor']}<br>
    <b>Semieje menor (b):</b> {parametros['semieje_menor']}<br>
    <b>Excentricidad:</b> {parametros['excentricidad']:.3f}<br>
    <b>Distancia focal (c):</b> {parametros['distancia_focal']:.3f}<br>
    <b>Focos:</b> {parametros['focos'][0]}, {parametros['focos'][1]}<br>
    <b>Vértices del eje mayor:</b> {parametros['vertices_mayor'][0]}, {parametros['vertices_mayor'][1]}<br>
    <b>Vértices del eje menor:</b> {parametros['vertices_menor'][0]}, {parametros['vertices_menor'][1]}<br>
    <b>Lado recto:</b> {parametros['lado_recto'] if parametros['lado_recto'] is not None else '-'}
    """
    return txt

