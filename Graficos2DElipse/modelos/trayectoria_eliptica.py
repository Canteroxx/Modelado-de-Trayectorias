import numpy as np

class TrayectoriaEliptica:

    def __init__(self, h, k, a, b, theta=0.0, rut=None):
        self.h = h
        self.k = k
        self.a = a
        self.b = b
        self.theta = theta
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
            theta = 0 if digits[5] % 2 == 0 else np.pi / 2
        else:
            a = digits[5] + digits[6]
            b = digits[4] + digits[2]
            theta = 0 if digits[3] % 2 == 0 else np.pi / 2

        return cls(h, k, a, b, theta, rut)

    def calcular_posicion(self, t):
        x = self.h + self.a * np.cos(t) * np.cos(self.theta) - self.b * np.sin(t) * np.sin(self.theta)
        y = self.k + self.a * np.cos(t) * np.sin(self.theta) + self.b * np.sin(t) * np.cos(self.theta)
        return np.array([x, y])

    def calcular_velocidad(self, t, dt=1e-5):
        pos_adelante = self.calcular_posicion(t + dt)
        pos_atras = self.calcular_posicion(t - dt)
        velocidad = (pos_adelante - pos_atras) / (2 * dt)
        return velocidad

    def trayectoria_completa(self, n_puntos=100):
        T = np.linspace(0, 2 * np.pi, n_puntos)
        return np.array([self.calcular_posicion(t) for t in T])

    def puntos(self, n=100):
        T = np.linspace(0, 2 * np.pi, n)
        puntos = np.array([self.calcular_posicion(t) for t in T])
        return puntos[:, 0], puntos[:, 1]

    def contiene_punto(self, x, y):
        xp = (x - self.h) * np.cos(self.theta) + (y - self.k) * np.sin(self.theta)
        yp = (x - self.h) * np.sin(self.theta) - (y - self.k) * np.cos(self.theta)
        return (xp**2 / self.a**2 + yp**2 / self.b**2) <= 1

    def __repr__(self):
        return (f"TrayectoriaEliptica(centro=({self.h}, {self.k}), a={self.a}, "
                f"b={self.b}, theta={self.theta}, rut={self.rut})")
