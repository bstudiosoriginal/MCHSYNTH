from typing import List
from physical.link import Link, Ground
from core.position import Position
import numpy as np
from sympy import Eq, solve, symbols

class Assembly(object):

    def __init__(self, links: List[Link], order: List[dict]=None, closed=False, closed_constraint='pin') -> None:
        # assemling links in order
        """
        @param: order: A list of dicts that of size len(links)-1. It must contain parameters: 'index' > integers that mark its parent's relative position from it. 'attached_from' > ['start' 'end'] 'attacked_to' > ['start' 'end']
        """
        if order is None:
            order = [{'index': 0, 'attached_from': 'start', 'attached_to': 'end', 'constraint': 'pin'} for _ in links]
        self.links = links
        self.order = order
        self.joints = []
        for link_id in range(len(links)-1):
            joint = self.links[link_id+1].attach_to(self.links[link_id+order[link_id]['index']], point={'self': order[link_id]['attached_from'], 'other': order[link_id]['attached_to']}, constraint=order[link_id]['constraint'])
            self.joints.append(joint)
        # if closed:
        #     linkb = Ground()
        #     order = {'index': 0, 'attached_from': 'start', 'attached_to': 'end', 'constraint': 'pin'}
        #     linkb.attach_to(self.links[-1], point={'self': 'start', 'other': 'end'}, constraint=closed_constraint)
        #     self.links.append(linkb)
        #     self.order.append(order)
    
    @staticmethod
    def create_order(idx=0, attached_from='start', attached_to='end', constraint='pin'):
        return {'index': idx, 'attached_from': attached_from, 'attached_to': attached_to, 'constraint': constraint}

    def link_between(self, l1, l2, point):
        l = None
        if isinstance(l1, Link) and isinstance(l2, Link):
            if point[0] == 'start' and point[1] == 'start':
                l = Link(start_pos=Position(*l1.start_pos.position), end_pos=Position(*l2.start_pos.position))
            elif point[0] == 'end' and point[1] == 'start':
                l = Link(start_pos=Position(*l1.end_pos.position), end_pos=Position(*l2.start_pos.position))
            elif point[0] == 'start' and point[1] == 'end':
                l = Link(start_pos=Position(*l1.start_pos.position), end_pos=Position(*l2.end_pos.position))
            elif point[0] == 'end' and point[1] == 'end':
                l = Link(start57_pos=Position(*l1.end_pos.position), end_pos=Position(*l2.end_pos.position))
            return l
        
    def plot(self, xlim=[-10, 10], ylim=[-10, 10]):
        ax = None
        for link_id in range(len(self.links)):
            show = link_id == (len(self.links)-1)
            # if ax and show:
            #     set_axes_equal(ax)
            ax = self.links[link_id].view(ax, xlim, ylim, show, eq=show)
        
    @staticmethod
    def symbol(v):
        return symbols(v)

    def mobility(self):
        L = len(self.links)
        G = len([i for i in self.links if isinstance(i, Ground)])
        # print(L, 'L', G, 'G')
        j = [i.classify() for i in self.joints]
        j1 = len([i for i in j if i == 'J1']) 
        j2 = len([i for i in j if i == 'J2']) 
        return 3*(L) - 2*j1 - j2 - 3*G
    
    def forces_analysis(self, link_F_R={}):
        sysx = []
        sysy = []
        sysmom = []
        for j in range(len(self.joints)-1):
            eqns1 = self.joints[j].force_analysis()
            eqns2 = self.joints[j+1].force_analysis()
            mid_link = set({self.joints[j].l1, self.joints[j].l2}).intersection({self.joints[j+1].l1, self.joints[j+1].l2}).pop()
            #  external forces
            if mid_link.name in link_F_R:
                Fextx = link_F_R[mid_link.name]['EXTERNAL_FORCE_X']
                Fexty = link_F_R[mid_link.name]['EXTERNAL_FORCE_Y']
                Rextx = link_F_R[mid_link.name]['EXTERNAL_FORCE_POSITION_X']
                Rexty = link_F_R[mid_link.name]['EXTERNAL_FORCE_POSITION_Y']
                Mext = link_F_R[mid_link.name]['EXTERNAL_MOMENT']
            else:
                Fextx = [0]
                Fexty = [0]
                Rextx = [0]
                Rexty = [0]
                Mext = [0]
            #sum fx
            Fx = sum(Fextx) + (-1 if j != 0 or j == (len(self.joints)-1) else 1)*eqns1[0][0]+ eqns2[0][0]
            #sum fy
            Fy = sum(Fexty) + (-1 if j != 0 or j == (len(self.joints)-1) else 1)*eqns1[0][1]+ eqns2[0][1]

            # external moments
            M = 0
            for i in range(len(Rextx)):
                # print(Rexty[i], Rextx[i])
                M += sum(Mext) - Fextx[i] * Rexty[i] + Fexty[i] * Rextx[i]
            # internal moment
            M += (-eqns2[0][0] * mid_link.displacement.dy) + (eqns2[0][1] * mid_link.displacement.dx)
            eq1 = Eq(Fx, 0)
            eq2 = Eq(Fy, 0)
            eq3 = Eq(M, 0)
            sysx.append(eq1)
            sysy.append(eq2)
            sysmom.append(eq3)
            # print(Fx, Fy, M)
            print(eq1, 'x equations', mid_link.name)
            print(eq2, 'y equations', mid_link.name)
            print(eq3, 'z equations', mid_link.name)
        sol = solve(sysx+sysy+sysmom, set=True)
        print(sol)


def set_axes_equal(ax):
    '''Make axes of 3D plot have equal scale so that spheres appear as spheres,
    cubes as cubes, etc..  This is one possible solution to Matplotlib's
    ax.set_aspect('equal') and ax.axis('equal') not working for 3D.

    Input
      ax: a matplotlib axis, e.g., as output from plt.gca().
    '''

    x_limits = ax.get_xlim3d()
    y_limits = ax.get_ylim3d()
    z_limits = ax.get_zlim3d()

    x_range = abs(x_limits[1] - x_limits[0])
    x_middle = np.mean(x_limits)
    y_range = abs(y_limits[1] - y_limits[0])
    y_middle = np.mean(y_limits)
    z_range = abs(z_limits[1] - z_limits[0])
    z_middle = np.mean(z_limits)

    # The plot bounding box is a sphere in the sense of the infinity
    # norm, hence I call half the max range the plot radius.
    plot_radius = 0.5*max([x_range, y_range, z_range])

    ax.set_xlim3d([x_middle - plot_radius, x_middle + plot_radius])
    ax.set_ylim3d([y_middle - plot_radius, y_middle + plot_radius])
    ax.set_zlim3d([z_middle - plot_radius, z_middle + plot_radius])
