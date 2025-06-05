def ecuacion_canonica(tr):
    h, k, a, b = tr.h, tr.k, tr.a, tr.b
    return r"\frac{(x-%s)^2}{%s^2} + \frac{(y-%s)^2}{%s^2} = 1" % (h, a, k, b)
