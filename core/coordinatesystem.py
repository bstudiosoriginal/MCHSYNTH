import numpy as np
from core.position import Position, Displacement


class SphericalCoordinateSystem(object):

    def __init__(self, rho, phi, theta) -> None:
        self.__rho = rho
        self.__phi = phi
        self.__theta = theta
    
    def get_params(self):
        return {
            'rho': self.__rho,
            'phi': self.__phi,
            'theta': self.__theta
        }

    def get_xyz(self, type='p'):
        lenght, phi, theta = self.__rho, self.__phi, self.__theta
        z = lenght * np.cos(phi)
        y = lenght * np.sin(phi) * np.sin(theta)
        x = lenght * np.sin(phi) * np.cos(theta)
        if type == 'p':
            return Position(x, y, z)
        return Displacement(x, y, z)
        
class CylindricalCoordinateSystem(object):

    def __init__(self, r, theta, z) -> None:
        self.__r = r
        self.__theta = theta
        self.__z = z
    
    def get_params(self):
        return {
            'r': self.__r,
            'z': self.__z,
            'theta': self.__theta
        }

    def get_xyz(self, type='p'):
        lenght, phi, z = self.__r, self.__theta, self.__z
        x = lenght * np.cos(phi)
        y = lenght * np.sin(phi)
        if type == 'p':
            return Position(x, y, z)
        return Displacement(x, y, z)
