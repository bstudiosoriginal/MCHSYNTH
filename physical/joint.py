from sympy import symbols, Eq, solve, linsolve
import numpy as np

class Joint():

    def __init__(self, l1, l2, constraint, l1_attach, l2_attach, child=1) -> None:
        self.l1 = l1
        self.l2 = l2
        self.constraint = constraint
        self.l1_attach = l1_attach
        self.l2_attach = l2_attach
        self.child = child

    def classify(self):
        if self.constraint in ['pin', 'slider']:
            return 'J1'
        elif self.constraint in ['form-closed', 'force-closed']:
            return 'J2'
        else:
            raise ValueError('Unknown type')

    def static_force_analysis(self):
        if self.constraint == 'pin':
            # forces at joint F12 etc
            s = symbols(['Fx_'+self.l1.name+'_'+self.l2.name, 'Fy_'+self.l1.name+'_'+self.l2.name, 'Fz_'+self.l1.name+'_'+self.l2.name])
            s2 = symbols(['F_'+self.l1.name+'_'+self.l2.name])
            # print(self.l1.displacement.cylindrical())
            # print(type(self.l2))
            # [s2[0]*numpy.cos(self.l2.displacement.cylindrical()[0]), s2[0]*numpy.sin(self.l2.displacement.cylindrical()[0])]
            return s, s2
        elif self.constraint == 'slider':
            # reactions exist
            s = symbols(['Fx_'+self.l1.name+'_'+self.l2.name, 'Fy_'+self.l1.name+'_'+self.l2.name, 'Fz_'+self.l1.name+'_'+self.l2.name])
            s2 = symbols(['F_'+self.l1.name+'_'+self.l2.name])
            print(type(self.l1), self.l1.name)
            return [s[0].subs(s[0], s2[0]*np.cos(self.l1._direction.xyz[1])), s[1].subs(s[1], s2[0]*np.sin(self.l1._direction.xyz[1]))], s2