import numpy as np

class TrayectoriaEliptica3D:
    """
    Representa una trayectoria elíptica en 3D:
      - Centro (h, k) en el plano XY
      - z0: altura (plano paralelo a XY)
      - a, b: semiejes
      - theta: ángulo de inclinación (en radianes, antihorario desde X+)
    """
    def __init__(self, h, k, a, b, z0=0.0, theta=0.0, rut=None, orientacion='horizontal'):
        self.h = h
        self.k = k
        self.a = a
        self.b = b
        self.z0 = z0
        self.theta = theta  # en radianes
        self.rut = rut
        self.orientacion = orientacion  # 'horizontal' o 'vertical'

    @classmethod
    def desde_rut(cls, rut: str, z0=0.0, theta=0.0):
        """
        Crea una elipse a partir de un RUT (debe venir SIN puntos y con guion).
        Puedes especificar z0 y theta (en radianes).
        """
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

        # Definir semiejes y orientación
        if grupo % 2 != 0:  # grupo impar
            eje_1 = digitos[2] + digitos[3]
            eje_2 = digitos[4] + digitos[5]
            orientacion = 'horizontal' if digitos[7] % 2 == 0 else 'vertical'
        else:  # grupo par
            eje_1 = digitos[5] + digitos[6]
            eje_2 = digitos[7] + digitos[2]
            orientacion = 'horizontal' if digitos[3] % 2 == 0 else 'vertical'

        if orientacion == 'horizontal':
            a, b = max(eje_1, eje_2), min(eje_1, eje_2)
        else:
            a, b = max(eje_2, eje_1), min(eje_2, eje_1)

        if a == 0 or b == 0:
            raise ValueError("Los semiejes no pueden ser cero.")

        return cls(h, k, a, b, z0=float(z0), theta=float(theta), rut=rut, orientacion=orientacion)

    def puntos_3d(self, n=100):
        """
        Devuelve arrays (x, y, z) para graficar la elipse en 3D,
        aplicando rotación theta (en radianes) y z0 como altura.
        """
        t = np.linspace(0, 2 * np.pi, n)
        # Eje mayor/minor según orientación
        if self.orientacion == 'horizontal':
            x0 = self.a * np.cos(t)
            y0 = self.b * np.sin(t)
        else:
            x0 = self.b * np.cos(t)
            y0 = self.a * np.sin(t)
        # Rotar en XY (si theta != 0)
        x = self.h + x0 * np.cos(self.theta) - y0 * np.sin(self.theta)
        y = self.k + x0 * np.sin(self.theta) + y0 * np.cos(self.theta)
        z = np.full_like(x, self.z0)
        return x, y, z

    def info_parametros(self):
        return {
            "centro": (self.h, self.k, self.z0),
            "a": self.a,
            "b": self.b,
            "rut": self.rut,
            "orientacion": self.orientacion,
            "theta (rad)": self.theta
        }

    def __repr__(self):
        return (f"TrayectoriaEliptica3D(centro=({self.h}, {self.k}, {self.z0}), "
                f"a={self.a}, b={self.b}, θ={self.theta} rad, "
                f"orientacion={self.orientacion}, rut={self.rut})")
