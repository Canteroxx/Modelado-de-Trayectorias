import numpy as np

class TrayectoriaEliptica:
    def __init__(self, h, k, a, b, rut=None):
        self.h = h
        self.k = k
        self.a = a
        self.b = b
        self.rut = rut

    @classmethod
    def desde_rut(cls, rut: str):
        partes = rut.strip().split('-')
        if len(partes) != 2:
            raise ValueError("Formato de RUT incorrecto (debe ser XXXXXXXX-Y)")

        rut_sin_dv = partes[0].replace('.', '')
        dv = partes[1].upper()

        if dv == 'K':
            dv = '10'

        if not dv.isdigit():
            raise ValueError("El dígito verificador debe ser un número o 'K'.")

        digits = [int(d) for d in rut_sin_dv if d.isdigit()]
        if len(digits) < 8:
            raise ValueError("El RUT debe tener al menos 8 dígitos antes del DV.")

        dv_int = int(dv)
        h, k = digits[0], digits[1]

        if dv_int % 2 == 1:
            a = digits[2] + digits[3]
            b = digits[4] + digits[5]
        else:
            a = digits[5] + digits[6]
            b = digits[4] + digits[2]

        return cls(h, k, a, b, rut)

    def calcular_posicion(self, t):
        x = self.h + self.a * np.cos(t)
        y = self.k + self.b * np.sin(t)
        return np.array([x, y])

    def trayectoria_completa(self, n_puntos=100):
        T = np.linspace(0, 2 * np.pi, n_puntos)
        return np.array([self.calcular_posicion(t) for t in T])

    def puntos(self, n=100):
        T = np.linspace(0, 2 * np.pi, n)
        puntos = np.array([self.calcular_posicion(t) for t in T])
        return puntos[:, 0], puntos[:, 1]

    def contiene_punto(self, x, y):
        return ((x - self.h) ** 2) / (self.a ** 2) + ((y - self.k) ** 2) / (self.b ** 2) <= 1

    def __repr__(self):
        return (f"TrayectoriaEliptica(centro=({self.h}, {self.k}), a={self.a}, "
                f"b={self.b}, rut={self.rut})")
