from sympy import symbols, Eq, solve, solve_linear_system

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
            # reactions exist
            s = symbols(['Fx_'+self.l1.name, 'Fy_'+self.l1.name, 'Fz_'+self.l1.name, 'Fx_'+self.l2.name, 'Fy_'+self.l2.name, 'Fz_'+self.l2.name])
            s2 = symbols(['F_'+self.l1.name, 'F_'+self.l2.name])
            if hasattr(self.l1, '_g') or hasattr(self.l2, '_g'):
                # ground reactions
                s3 = symbols([f'RJx_{self.l1.name}_{self.l2.name}', f'RJy_{self.l1.name}_{self.l2.name}', f'RJz_{self.l1.name}_{self.l2.name}'])
            else:
                s3 = []
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
            exp1 = solve(eqx, s2[0], s2[1], dict=True)
            exp2 = solve(eqy, s2[0], s2[1], dict=True)
            exp3 = solve(eqz, s2[0], s2[1], dict=True)
            # exp2 = solve(eqy, s2[0], s2[1])
            # print(exp1)
            # print(exp2)
            # print(exp3)
            # print('\n')
        
        elif self.constraint == 'slider':
            # reactions exist
            s = symbols(['Fx_'+self.l1.name, 'Fy_'+self.l1.name, 'Fz_'+self.l1.name, 'Fx_'+self.l2.name, 'Fy_'+self.l2.name, 'Fz_'+self.l2.name])
            s2 = symbols(['F_'+self.l1.name, 'F_'+self.l2.name])
            s3 = symbols([f'RJx_{self.l1.name}_{self.l2.name}', f'RJy_{self.l1.name}_{self.l2.name}', f'RJz_{self.l1.name}_{self.l2.name}'])
            
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
            exp1 = solve(eqx, s2[0], s2[1], dict=True)
            exp2 = solve(eqy, s2[0], s2[1], dict=True)
            exp3 = solve(eqz, s2[0], s2[1], dict=True)
            # exp2 = solve(eqy, s2[0], s2[1])
            # print(exp1)
            # print(exp2)
            # print(exp3)
            print('\n')
        return exp1, exp2, exp3
            