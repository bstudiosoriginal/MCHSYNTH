import numpy as np
from core.position import Position, Displacement
from core.rotation import Rotation
from core.scale import Scale
from core.coordinatesystem import SphericalCoordinateSystem, CylindricalCoordinateSystem
import random
import time

class Link(object):

    _start_pos = None

    _end_pos = None

    _displacement = None

    _direction = None

    _thickness = 0.1

    _lenght = None

    def __hash__(self):
        return hash(self.name)

    def __init__(self, start_pos=None, end_pos=None, displacement=None, spherical_displacement=None, cylindrical_displacement=None, spherical=None, cylindrical=None, name=None) -> None:
        if name is None:
            name = str(time.time())
        self.name = name
        self.displacement = displacement
        self.start_pos = start_pos
        self.end_pos = end_pos
        # print(self.check_valid(v=False))
        if isinstance(spherical_displacement, SphericalCoordinateSystem) and not self.check_valid(False):
            displacement = spherical_displacement.get_xyz('d')
            self.displacement = displacement
        if isinstance(cylindrical_displacement, CylindricalCoordinateSystem) and not self.check_valid(False):
            displacement = cylindrical_displacement.get_xyz('d')
            self.displacement = displacement
        if spherical is not None and not self.check_valid(False):
            if len(spherical) == 2:
                start_pos = spherical[0].get_xyz('p')
                end_pos = spherical[1].get_xyz('p')
                self.start_pos = start_pos
                self.end_pos = end_pos
        if cylindrical is not None and not self.check_valid(False):
            if len(cylindrical) == 2:
                start_pos = cylindrical[0].get_xyz('p')
                end_pos = cylindrical[1].get_xyz('p')
                self.start_pos = start_pos
                self.end_pos = end_pos

    def check_valid(self, v=True):
        if v:
            print('start pos', self.start_pos, self.start_pos is not None)
            print('end pos', self.end_pos, self.end_pos is not None)
            print('displacement', self.displacement, self.displacement is not None)
            print('length', self._lenght, self._lenght is not None)
            print('direction', self._direction, self._direction is not None)
            
        return self._start_pos is not None and self._end_pos is not None and self._lenght is not None and self._displacement is not None and self._direction is not None
    @property
    def start_pos(self):
        return self._start_pos
    
    @start_pos.setter
    def start_pos(self, val):
        if isinstance(val, Position):
            self._start_pos = val
        # validate completeness
        if self._start_pos and self.displacement:
            self._end_pos = self.start_pos + self.displacement
        elif self._start_pos and self._end_pos:
            self.displacement = self._end_pos - self._start_pos
            
    @property
    def displacement(self):
        return self._displacement

    @displacement.setter
    def displacement(self, val):        
        if isinstance(val, Displacement):
            self._displacement = val
            self._lenght = self._displacement.abs_displacement()
            phi = np.arccos(self._displacement.dz / self._lenght)
            theta = np.arctan2(self._displacement.dy, self._displacement.dx)
            self._direction = Rotation(None, 0, theta, phi)
        if self.displacement and self.start_pos:
            self._end_pos = self.start_pos + self.displacement
        elif self.displacement and self.end_pos:
            self._start_pos = self.end_pos - self.displacement

    @property
    def end_pos(self):
        return self._end_pos

    @end_pos.setter
    def end_pos(self, val):
        if isinstance(val, Position):
            self._end_pos = val
        if self._end_pos and self.displacement:
            self._start_pos = self.end_pos - self.displacement
        elif self._end_pos and self._start_pos:
            self.displacement = self._end_pos - self._start_pos
       
    
    def get_normal(self):
        n = np.cross(np.array(self.start_pos.position), np.array(self.end_pos.position))
        ndet = np.sqrt(np.sum(n**2))
        if ndet == 0:
            ndet = 1
        return (n/ndet)
    
    def attach(self, other, point={'self': 'start', 'other': 'end'}, constraint='pin'):
        aligned = False
        if isinstance(other, Link):
            n1 =  self.get_normal()
            n2 = other.get_normal()
            if np.sum(n1) != 0 and np.sum(n2) != 0:
                if (n1[0] == n2[0] and n1[1] == n2[1] and n1[2] == n2[2]) or (n1[0] == -n2[0] and n1[1] == -n2[1] and n1[2] == -n2[2]):
                        # aligned
                    # print('aligned')
                    aligned = True
                else:
                    # not aligned 
                    # print('not aligned')
                    aligned = False
            else:
                # print('1')
                if np.sum(n1) == 0 and np.sum(n2) != 0:
                    
                    # we are zero here. lets use displacement as our vector
                    n1 = np.cross(np.array(self.displacement.position), np.array(other.start_pos.position))
                    n1det = np.sqrt(np.sum(n1**2))
                    if n1det == 0:
                        n1det = 1
                    n1 = n1 / n1det
                    if (n1[0] == n2[0] and n1[1] == n2[1] and n1[2] == n2[2]) or (n1[0] == -n2[0] and n1[1] == -n2[1] and n1[2] == -n2[2]):
                        # aligned
                        # print('aligned')
                        aligned = True
                    else:
                        # not aligned
                        # print('not aligned')
                        aligned = False
                elif np.sum(n2) == 0 and np.sum(n1) != 0:
                    print('2')
                    # we are zero here. lets use displacement as our vector
                    n2 = np.cross(np.array(other.displacement.position), np.array(self.start_pos.position))
                    n2det = np.sqrt(np.sum(n2**2))
                    if n2det == 0:
                        n2det = 1
                    n2 = n2 / n2det
                    if (n1[0] == n2[0] and n1[1] == n2[1] and n1[2] == n2[2]) or (n1[0] == -n2[0] and n1[1] == -n2[1] and n1[2] == -n2[2]):
                        # aligned
                        aligned = True
                        print('aligned')
                        pass
                    else:
                        # not aligned
                        aligned = False
                        print('not aligned')
                        pass
                else:
                    # we are zero here. lets use displacement as our vector
                    # aligned
                    aligned = True
                    print('aligned')
                    pass
        if aligned:
            # perform attachment
            self._attach(other, point, constraint)
        else:
            # do not attach
            raise ValueError('Cannot attach non aligned links')
        
    def r(self):
        return np.array(self.displacement.position)

    def vectorize(self):
        return np.array(self.start_pos.position), np.array(self.end_pos.position)
    
    def redefine(self, displacement, elastic=False):
        # makes sure start position is fixed.
        if not isinstance(displacement, Displacement):
            raise ValueError()
        if not elastic:
            assert displacement.abs_displacement() ==  self.displacement.abs_displacement()
            self.displacement = displacement
        else:
            self.displacement = displacement

    def _attach(self, other, point, constraint):
        if constraint == 'pin':
            # pin joint
            # move to point
            if point['self'] == 'start' and point['other'] == 'end':
                self.start_pos = Position(*other.end_pos.position)
            elif point['self'] == 'end' and point['other'] == 'start':
                self.end_pos = Position(*other.start_pos.position)
            elif point['self'] == 'start' and point['other'] == 'start':
                self.start_pos = Position(*other.start_pos.position)
            elif point['self'] == 'end' and point['other'] == 'end':
                self.end_pos = Position(*other.end_pos.position)
            