import math
from pyquaternion.quaternion import Quaternion


from core.measurement import Measurement


class Position(Measurement):

    def __init__(self, x=0, y=0, z=0, unit='m') -> None:
        super().__init__('m')
        self._position = None
        """
        Creation of a unit position. Euler overrides axis position.
        
        x: position in meters on the x-axis
        y: position in meters on the y-axis
        z: position in meters on the z-axis

        """
        self._bunit = None
        self.bunit = unit
        self.position = [self.convert_to_meters(x, unit), self.convert_to_meters(y, unit), self.convert_to_meters(z, unit)]
    
    @staticmethod
    def convert_to_meters(value, unit):
        if unit == 'cm':
            value *= 0.01
        elif unit == 'mm':
            value *= 0.001
        elif unit == 'in':
            value *= 0.0254
        elif unit == 'ft':
            value *= 0.3048
        elif unit == 'm':
            value *= 1
        return value

    @staticmethod
    def convert_from_meters(value, unit):
        if unit == 'cm':
            value /= 0.01
        elif unit == 'mm':
            value /= 0.001
        elif unit == 'in':
            value /= 0.0254
        elif unit == 'ft':
            value /= 0.3048
        elif unit == 'm':
            value /= 1
        return value

    @property
    def position(self):
        return self._position
    
    @position.setter
    def position(self, value):
        assert isinstance(value, (list, tuple))
        self._position = value
    
    @property
    def bunit(self):
        return self._bunit
    
    @bunit.setter
    def bunit(self, value):
        assert isinstance(value, str)
        self._bunit = value.lower()


    def __repr__(self) -> str:
        return f' <Position({self.position}) in {self.get_unit()}> '
    
    def __str__(self) -> str:
        return f'<Position: {self.position}>'

    def __add__(self, o):
        if isinstance(o, Displacement):
            x = self.position[0] + o.position[0]
            y = self.position[1] + o.position[1]
            z = self.position[2] + o.position[2]
            return Position(x=x, y=y, z=z)
        elif isinstance(o, Position):
            x = self.position[0] + o.position[0]
            y = self.position[1] + o.position[1]
            z = self.position[2] + o.position[2]
            return Displacement(dx=x, dy=y, dz=z)
        else:
            raise ValueError("Cannot add non position type")

    def __sub__(self, o):
        if isinstance(o, Displacement):
            x = self.position[0] - o.position[0]
            y = self.position[1] - o.position[1]
            z = self.position[2] - o.position[2]
            return Position(x=x, y=y, z=z)
        elif isinstance(o, Position):
            x = self.position[0] - o.position[0]
            y = self.position[1] - o.position[1]
            z = self.position[2] - o.position[2]
            return Displacement(dx=x, dy=y, dz=z)
        else:
            raise ValueError("Cannot subtract non position type")

    def __mul__(self, o):
        if isinstance(o, Displacement):
            x = self.position[0] * o.position[0]
            y = self.position[1] * o.position[1]
            z = self.position[2] * o.position[2]
            return Position(x=x, y=y, z=z)
        elif isinstance(o, Position):
            x = self.position[0] * o.position[0]
            y = self.position[1] * o.position[1]
            z = self.position[2] * o.position[2]
            return Displacement(dx=x, dy=y, dz=z)
        elif isinstance(o, (int, float)):
            x = self.position[0] * o
            y = self.position[1] * o
            z = self.position[2] * o
            return Position(x=x, y=y, z=z)
        else:
            raise ValueError("Cannot multiply non position type")

    def __neg__(self):
        if isinstance(self, Displacement):
            x = -self.position[0] 
            y = -self.position[1]
            z = -self.position[2]
            return Displacement(dx=x, dy=y, dz=z)
        else:
            x = -self.position[0] 
            y = -self.position[1]
            z = -self.position[2]
            return Position(x=x, y=y, z=z)


class Displacement(Position):

    def __init__(self, dx=0, dy=0, dz=0, unit='m') -> None:
        super().__init__(dx, dy, dz, unit)

    @property
    def dx(self):
        return self._position[0]

    @property
    def dy(self):
        return self._position[1]

    @property
    def dz(self):
        return self._position[2]

    def abs_displacement(self):
        return math.sqrt(self.dx**2 + self.dy**2 + self.dz**2)

    def displacement_2D(self):
        return math.sqrt(self.dx**2 + self.dy**2)

    def angles(self):
        return [math.atan2(self.dx, self.dy), math.atan2(self.dz, self.dx), math.atan2(self.dz, self.dy)]

    def spherical(self):
        return [self.abs_displacement(), math.atan2(self.dz, self.displacement_2D()), math.atan2(self.dy, self.dx)]

    def cylindrical(self):
        return [math.atan2(self.dy, self.dx), self.displacement_2D(), self.dz]

    def __repr__(self) -> str:
        return f' <Displacement({self.position}) in {self.get_unit()}> '
    
    def __str__(self) -> str:
        return f'<Displacement: {self.position}>'

    def __mul__(self, o):
        if isinstance(o, Displacement):
            x = self.position[0] * o.position[0]
            y = self.position[1] * o.position[1]
            z = self.position[2] * o.position[2]
            return Displacement(dx=x, dy=y, dz=z)
        elif isinstance(o, Position):
            x = self.position[0] * o.position[0]
            y = self.position[1] * o.position[1]
            z = self.position[2] * o.position[2]
            return Displacement(dx=x, dy=y, dz=z)
        elif isinstance(o, (int, float)):
            x = self.position[0] * o
            y = self.position[1] * o
            z = self.position[2] * o
            return Displacement(dx=x, dy=y, dz=z)
        else:
            raise ValueError("Cannot multiply non position type")

    
    def __add__(self, o):
        if isinstance(o, Displacement):
            x = self.position[0] + o.position[0]
            y = self.position[1] + o.position[1]
            z = self.position[2] + o.position[2]
            return Displacement(dx=x, dy=y, dz=z)
        elif isinstance(o, Position):
            x = self.position[0] + o.position[0]
            y = self.position[1] + o.position[1]
            z = self.position[2] + o.position[2]
            return Position(x=x, y=y, z=z)
        else:
            raise ValueError("Cannot add non position type")

    def __sub__(self, o):
        if isinstance(o, Displacement):
            x = self.position[0] - o.position[0]
            y = self.position[1] - o.position[1]
            z = self.position[2] - o.position[2]
            return Displacement(dx=x, dy=y, dz=z)
        elif isinstance(o, Position):
            x = self.position[0] - o.position[0]
            y = self.position[1] - o.position[1]
            z = self.position[2] - o.position[2]
            return Position(x=x, y=y, z=z)
        else:
            raise ValueError("Cannot subtract non position type")