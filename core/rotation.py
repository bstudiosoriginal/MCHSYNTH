import math
from pyquaternion.quaternion import Quaternion


from core.measurement import Measurement

class Rotation(Measurement):

    def __init__(self, Q=None, rot_x=0.0, rot_y=0.0, rot_z=0.0, euler=None, euler_order='XYZ', degrees=False) -> None:
        super().__init__('rad')

        """
        Creation of a unit rotation. Euler overrides axis rotation.
        euler: type: List/tuple of lenght 3.
        rot_x: angle of rotation in radians about the x-axis
        rot_y: angle of rotation in radians about the y-axis
        rot_z: angle of rotation in radians about the z-axis

        """
        self._from_ = 'xyz'
        self._rotation = None
        self._euler = None
        self._euler_order = None
        self._xyz = None
        self.degrees = degrees
        self.euler_order = euler_order
        
        if Q is not None:
            self._from_ = 'q'
            self.rotation = Q
        elif euler is not None:
            self._from_ = 'euler'
            self.euler = euler
        else:
            self.xyz = [rot_x, rot_y, rot_z]
    
    @property
    def rotation(self):
        return self._rotation
    
    @rotation.setter
    def rotation(self, value):
        assert isinstance(value, Quaternion)
        self._rotation = value

    @property
    def xyz(self):
        return self._xyz
    
    @xyz.setter
    def xyz(self, value):
        assert isinstance(value, (list, tuple))
        if self.degrees:
            value = [value[i]*math.pi/180 for i in range(len(value))]
        self._xyz = value
        self.rotation = self.xyz_to_quat()

    @property
    def from_euler(self):
        return self._from_euler

    @from_euler.setter
    def from_euler(self, value):
        assert type(value) == bool
        self._from_euler = value
    
    @property
    def euler(self):
        return self._euler

    @euler.setter
    def euler(self, value):
        assert isinstance(value, (list, tuple)) and len(value) == 3
        if self.degrees:
            value = [value[i]*math.pi/180 for i in range(len(value))]
        self._euler = value
        # Change the rotation quaternion
        self.rotation = self.euler_to_quat()

    @property
    def euler_order(self):
        return self._euler_order
    
    @euler_order.setter
    def euler_order(self, value):
        if isinstance(value, str) and value.upper() in ['XYZ', 'YZX', 'ZXY', 'XZY', 'YXZ', 'ZYX']:
            self._euler_order = value

    def euler_to_quat(self):
        """
        Function that converts euler angles to corresponding quaternion
        """
        euler_order = self.euler_order
        axes = []
        for order in euler_order:
            if order.upper() == 'X':
                axes.append([1, 0, 0])
            elif order.upper() == 'Y':
                axes.append([0, 1, 0])
            elif order.upper() == 'Z':
                axes.append([0, 0, 1])
        q = Quaternion(axis=[1, 0, 0], angle=0)
        for axis, e in zip(axes, self.euler):
            q *= Quaternion(axis=axis, angle=e) 
        return q

    def xyz_to_quat(self):
        """
        Function that converts xyz angles to quaternion.
        """
        xyz = self.xyz
        
        q1 = Quaternion(axis=[1, 0, 0], angle=xyz[0])
        q2 = Quaternion(axis=[0, 1, 0], angle=xyz[1])
        q3 = Quaternion(axis=[0, 0, 1], angle=xyz[2])
        q = q1 * q2 * q3
        return q

    def __repr__(self) -> str:
        return f' <Rotation({self.rotation}) in {self.get_unit()}> '
    
    def __str__(self) -> str:
        return f'<Rotation: {self.rotation}>'

    def __add__(self, o):
        assert isinstance(o, Rotation)
        nq = self.rotation + o.rotation
        return Rotation(Q=nq)

    def __sub__(self, o):
        assert isinstance(o, Rotation)
        nq = self.rotation - o.rotation
        return Rotation(Q=nq)

    def __mul__(self, o):
        assert isinstance(o, Rotation)
        nq = self.rotation * o.rotation
        return Rotation(Q=nq)
