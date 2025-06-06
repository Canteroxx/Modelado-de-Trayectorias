import numpy as np

class TrayectoriaEliptica:
    def __init__(self, h, k, a, b, rut=None, orientacion='horizontal'):
        self.h = h
        self.k = k
        self.a = a
        self.b = b
        self.rut = rut
        self.orientacion = orientacion

    @classmethod
    def desde_rut(cls, rut: str):
        partes = rut.strip().split('-')
        if len(partes) != 2:
            raise ValueError("Formato de RUT incorrecto (debe ser XXXXXXXX-Y)")

        cuerpo_rut = partes[0].replace('.', '')
        dv = partes[1].upper()

        if dv == 'K':
            grupo = 10
        elif dv.isdigit():
            grupo = int(dv)
        else:
            raise ValueError("El dígito verificador debe ser un número o 'K'.")

        digitos = [int(d) for d in cuerpo_rut if d.isdigit()]
        if len(digitos) < 8:
            raise ValueError("El RUT debe tener al menos 8 dígitos antes del DV.")

        h, k = digitos[0], digitos[1]

        if grupo % 2 != 0:  # grupo impar
            semieje_x = digitos[2] + digitos[3]
            semieje_y = digitos[4] + digitos[5]
            orientacion = 'horizontal' if digitos[7] % 2 == 0 else 'vertical'
        else:  # grupo par
            semieje_x = digitos[5] + digitos[6]
            semieje_y = digitos[7] + digitos[2]
            orientacion = 'horizontal' if digitos[3] % 2 == 0 else 'vertical'

        if orientacion == 'horizontal':
            a, b = max(semieje_x, semieje_y), min(semieje_x, semieje_y)
        else:
            a, b = max(semieje_y, semieje_x), min(semieje_y, semieje_x)

        return cls(h, k, a, b, rut, orientacion)

    def calcular_posicion(self, t):
        if self.orientacion == 'horizontal':
            x = self.h + self.a * np.cos(t)
            y = self.k + self.b * np.sin(t)
        else:
            x = self.h + self.b * np.cos(t)
            y = self.k + self.a * np.sin(t)
        return np.array([x, y])

    def trayectoria_completa(self, n_puntos=100):
        angulos = np.linspace(0, 2 * np.pi, n_puntos)
        return np.array([self.calcular_posicion(t) for t in angulos])

    def puntos(self, n=100):
        trayectoria = self.trayectoria_completa(n)
        return trayectoria[:, 0], trayectoria[:, 1]

    def contiene_punto(self, x, y):
        if self.orientacion == 'horizontal':
            return ((x - self.h) ** 2) / (self.a ** 2) + ((y - self.k) ** 2) / (self.b ** 2) <= 1
        else:
            return ((x - self.h) ** 2) / (self.b ** 2) + ((y - self.k) ** 2) / (self.a ** 2) <= 1

    def __repr__(self):
        return (f"TrayectoriaEliptica(centro=({self.h}, {self.k}), a={self.a}, "
                f"b={self.b}, orientación={self.orientacion}, rut={self.rut})")
