# Importar do pacote.
from raycaster.objects import Intersectionable
# Importar do projeto.
from raycaster.physics import Point, Vector, Line
# Importar bibliotecas.
import math
from typing import Union


class Plane(Intersectionable):
    def __init__(self, origin: Point, normal: Vector) -> None:
        self.origin = origin
        self.normal = normal

    @property
    def origin(self) -> Point:
        return self._origin

    @origin.setter
    def origin(self, value: Point) -> None:
        self._origin = value

    @property
    def normal(self) -> Vector:
        return self._normal

    @normal.setter
    def normal(self, value: Vector) -> None:
        self._normal = value

    def __str__(self):
        return "O: {0} N: {1}".format(self.origin, self.normal)

    def __matmul__(self, other):
        # Argumento é uma reta.
        if isinstance(other, Line):
            # Interseção reta-plano.
            return Plane.intersection(self, other)
        else:
            raise TypeError(
                "Classe '{0}' não possui suporte para interseção com objetos de tipo '{1}'."
                .format(self.__class__.__name__, type(other))
            )

    def intersection(self, line: Line, coef: bool = True, fwrd: bool = True) -> Union[None, Point, float]:
        v = line.direction
        n = self.normal
        prpl = self.origin - line.origin

        # Cálculos repetidos.
        v_scalar_n = v * n

        # Verificar se o plano e a reta são perpendiculares.
        if not math.isclose(v_scalar_n, 0):
            # Não são perpendiculares. Há uma única interseção.
            t = (prpl * n) / v_scalar_n

            return None if (fwrd and t < 0) else (t if coef else line(t))
        else:
            # São perpendiculares.
            if math.isclose(prpl * n, 0):
                # A reta está sobre o plano. A interseção é a própria reta. Retornar a origem da reta.
                return 0 if coef else line.origin
            else:
                # A reta é paralela ao plano. Não há interseção.
                return None

    def _true_intersection(self, line: Line):
        v = line.direction
        n = self.normal
        prpl = self.origin - line.origin

        # Verificar se a reta e o plano são perpendiculares.
        if not math.isclose(v * n, 0):
            # Não são perpendiculares. Há uma única interseção.
            return line((prpl * n) / (v * n))
        else:
            # São perpendiculares.
            if math.isclose(prpl * n, 0):
                # A reta está sobre o plano. A interseção é a própria reta.
                return line
            else:
                # A reta é paralela ao plano. Não há interseção.
                return None
