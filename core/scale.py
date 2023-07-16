import math
from pyquaternion.quaternion import Quaternion


from core.measurement import Measurement


class Scale(Measurement):

    def __init__(self, x=1, y=1, z=1, unit='m') -> None:
        super().__init__('m')
        self._scale = None
        """
        Creation of a unit scale. Euler overrides axis scale.
        
        x: scale in meters on the x-axis
        y: scale in meters on the y-axis
        z: scale in meters on the z-axis

        """
        self._bunit = None
        self.bunit = unit
        self.scale_factor = [self.convert_to_meters(x, unit), self.convert_to_meters(y, unit), self.convert_to_meters(z, unit)]
    
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
    def scale_factor(self):
        return self._scale
    
    @scale_factor.setter
    def scale_factor(self, value):
        assert isinstance(value, (list, tuple))
        self._scale = value
    
    @property
    def bunit(self):
        return self._bunit
    
    @bunit.setter
    def bunit(self, value):
        assert isinstance(value, str)
        self._bunit = value.lower()


    def __repr__(self) -> str:
        return f' <Scale({self.scale_factor}) in {self.get_unit()}> '
    
    def __str__(self) -> str:
        return f'<Scale: {self.scale_factor}>'

    def __add__(self, o):
        if isinstance(o, Scale):
            x = self.scale_factor[0] + o.scale_factor[0]
            y = self.scale_factor[1] + o.scale_factor[1]
            z = self.scale_factor[2] + o.scale_factor[2]
            return Scale(x=x, y=y, z=z)
        else:
            raise ValueError("Cannot add non scale_factor type")

    def __sub__(self, o):
        if isinstance(o, Scale):
            x = self.scale_factor[0] - o.scale_factor[0]
            y = self.scale_factor[1] - o.scale_factor[1]
            z = self.scale_factor[2] - o.scale_factor[2]
            return Scale(x=x, y=y, z=z)
        else:
            raise ValueError("Cannot subtract non scale_factor type")

    def __mul__(self, o):
        if isinstance(o, Scale):
            x = self.scale_factor[0] * o.scale_factor[0]
            y = self.scale_factor[1] * o.scale_factor[1]
            z = self.scale_factor[2] * o.scale_factor[2]
            return Scale(x=x, y=y, z=z)
        else:
            raise ValueError("Cannot multiply non scale_factor type")

    def scale(self, point):
        return point[0]*self.scale_factor[0], point[1]*self.scale_factor[1], point[2]*self.scale_factor[2]


    
