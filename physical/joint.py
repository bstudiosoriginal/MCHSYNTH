from sympy import symbols, Eq, solve, linsolve
import numpy
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

    def force_analysis(self):
        if self.constraint == 'pin':
            # forces at joint F12 etc
            s = symbols(['Fx_'+self.l1.name+'_'+self.l2.name, 'Fy_'+self.l1.name+'_'+self.l2.name, 'Fz_'+self.l1.name+'_'+self.l2.name])
            s2 = symbols(['F_'+self.l1.name+'_'+self.l2.name])
            # print(self.l1.displacement.cylindrical())
            # print(type(self.l2))
            # [s2[0]*numpy.cos(self.l2.displacement.cylindrical()[0]), s2[0]*numpy.sin(self.l2.displacement.cylindrical()[0])]
            return s, s2
            if hasattr(self.l1, '_g') or hasattr(self.l2, '_g'):
                # ground reactions
                s3 = symbols([f'RJx_{self.l1.name}_{self.l2.name}', f'RJy_{self.l1.name}_{self.l2.name}', f'RJz_{self.l1.name}_{self.l2.name}'])
            else:
                s3 = []
            s4 = []
            if self.l1_attach == 'end':
                p1 = -self.l1.displacement
            else:
                p1 = self.l1.displacement
            if self.l2_attach == 'end':
                p2 = -self.l2.displacement
            else:
                p2 = self.l2.displacement
            if p1.abs_displacement():
                cl1 = (p1 * (1/p1.abs_displacement())).position
                
            else:
                cl1 = [0, 0, 0]
            if p2.abs_displacement():
                cl2 = (p2 * (1/p2.abs_displacement())).position
                
            else:
                cl2 = [0, 0, 0]
            if s3:
                eq1 = Eq(s[0] + s[3], -s3[0])
                eq2 = Eq(s[1] + s[4], -s3[1])
                eq3 = Eq(s[2] + s[5], -s3[2])
            else:
                eq1 = Eq(s[0] + s[3], 0)
                eq2 = Eq(s[1] + s[4], 0)
                eq3 = Eq(s[2] + s[5], 0)
            eqx = eq1.subs(s[0], s2[0]*cl1[0]).subs(s[3], s2[1]*cl2[0])
            eqy = eq2.subs(s[1], s2[0]*cl1[1]).subs(s[4], s2[1]*cl2[1])
            eqz = eq3.subs(s[2], s2[0]*cl1[2]).subs(s[5], s2[1]*cl2[2])
            # print(eqx)
            # print(eqy)
            # print(eqz)
            m1=False
            m2=False
            if p1.abs_displacement():
                d1 = p1.abs_displacement()
                m1 = s[0]*p1.dx/d1 +s[1]*p1.dy/d1 +symbols(f'Mz_{self.l1.name}')
                m1 = m1.subs(s[0], s2[0]*cl1[0]).subs(s[3], s2[1]*cl2[0]).subs(s[1], s2[0]*cl1[1]).subs(s[4], s2[1]*cl2[1])
            if p2.abs_displacement():
                d2 = p2.abs_displacement()
                m2 = s[3]*p2.dx/d2 + s[4]*p2.dy/d2 + symbols(f'P_{self.l2.name}')
                m2 = m2.subs(s[0], s2[0]*cl1[0]).subs(s[3], s2[1]*cl2[0]).subs(s[1], s2[0]*cl1[1]).subs(s[4], s2[1]*cl2[1])
            # exp1 = solve(eqx, s2[0], s2[1], dict=True)
            # exp2 = solve(eqy, s2[0], s2[1], dict=True)
            # exp3 = solve(eqz, s2[0], s2[1], dict=True)
            # print(eqx)
            # print(eqy)
            # print(eqz)
            # exp2 = solve(eqy, s2[0], s2[1])
            # print(exp1)
            # print(exp2)
            # print(exp3)
            # print('\n')
        
        elif self.constraint == 'slider':
            # reactions exist
            s = symbols(['Fx_'+self.l1.name+'_'+self.l2.name, 'Fy_'+self.l1.name+'_'+self.l2.name, 'Fz_'+self.l1.name+'_'+self.l2.name])
            s2 = symbols(['F_'+self.l1.name+'_'+self.l2.name])
            return s, s2
            s3 = symbols([f'RJx_{self.l1.name}_{self.l2.name}', f'RJy_{self.l1.name}_{self.l2.name}', f'RJz_{self.l1.name}_{self.l2.name}'])
            if self.l2.displacement.abs_displacement():
                d = self.l2.displacement * (1/self.l2.displacement.abs_displacement())
                s3 = [s3[0]*d.dx,s3[1]*d.dy,s3[2]*d.dz] 
            if self.l1_attach == 'end':
                p1 = -self.l1.displacement
            else:
                p1 = self.l1.displacement
            
            if p1.abs_displacement():
                cl1 = (p1 * (1/p1.abs_displacement())).position
            else:
                cl1 = [0, 0, 0]
            
            if s3:
                eq1 = Eq(s[0] + s[3], -s3[0])
                eq2 = Eq(s[1] + s[4], -s3[1])
                eq3 = Eq(s[2] + s[5], -s3[2])
            else:
                eq1 = Eq(s[0] + s[3], 0)
                eq2 = Eq(s[1] + s[4], 0)
                eq3 = Eq(s[2] + s[5], 0)
            eqx = eq1.subs(s[0], s2[0]*cl1[0])
            eqy = eq2.subs(s[1], s2[0]*cl1[1])
            eqz = eq3.subs(s[2], s2[0]*cl1[2])
            m1 = False
            m2 = False
            if p1.abs_displacement():
                d1 = p1.abs_displacement()
                m1 = s[0]*p1.dx/d1 +s[1]*p1.dy/d1 +symbols(f'Mz_{self.l1.name}')
            
            
            m2 =  symbols(f'P_{self.l2.name}')
            # print(eqx)
            # print(eqy)
            # print(eqz)
            # exp1 = solve(eqx, s2[0], s2[1], dict=True)
            # exp2 = solve(eqy, s2[0], s2[1], dict=True)
            # exp3 = solve(eqz, s2[0], s2[1], dict=True)
            # sol = solve([eqx, eqy, eqz], s2+s3)
            # exp2 = solve(eqy, s2[0], s2[1])
            # print(exp1)
            # print(exp2)
            # print(exp3)
            # print('\n')
        # return [[eqx, eqy, eqz], [m1, m2]]
            