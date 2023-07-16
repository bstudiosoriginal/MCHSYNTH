import numpy as np
from core.position import Position, Displacement
from core.rotation import Rotation
from core.coordinatesystem import SphericalCoordinateSystem, CylindricalCoordinateSystem


def link_creation_test():
    from physical.link import Link
    
    # normal creation
    link0 = Link(start_pos=Position(10, 1, 0), end_pos=Position(40, 2, 3))
    link0.check_valid()
    print('\n')

    link1 = Link(start_pos=Position(1, 3, 0), displacement=Displacement(4, 5, 0))
    link1.check_valid()
    print('\n')

    link2 = Link(end_pos=Position(1, 3, 0), displacement=Displacement(4, 5, 0))
    link2.check_valid()
    print('\n')

    link3 = Link(start_pos=Position(0, 0, 0), displacement=Displacement(3, 4, 0))
    link3.check_valid()
    print('\n')

    link4 = Link(start_pos=Position(0, 0, 0), spherical_displacement=SphericalCoordinateSystem(5, np.pi/6, np.pi/4))
    link4.check_valid()
    print('\n')

    link5 = Link(start_pos=Position(1, 3, 5), cylindrical_displacement=CylindricalCoordinateSystem(3, np.radians(30), 4))
    link5.check_valid()
    print('\n')

    link6 = Link(start_pos=Position(1, 3, 5), spherical=[SphericalCoordinateSystem(5, np.pi/6, np.pi/4), SphericalCoordinateSystem(10, np.pi/6, np.pi/4)])
    link6.check_valid()
    print('\n')

    clist = [CylindricalCoordinateSystem(3, np.radians(60), 4), CylindricalCoordinateSystem(3, np.radians(90), 4)]
    # print(clist[0].get_xyz())
    link7 = Link( cylindrical=clist)
    link7.check_valid()
    print('\n')

    print(link2.get_normal(), link3.get_normal(), link1.get_normal(), link5.get_normal())
    link1.attach(link3)
    link1.check_valid()
    

    
    

if __name__ == '__main__':
    link_creation_test()