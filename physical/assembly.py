from typing import List
from physical.link import Link, Ground
from core.position import Position


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
        
    def plot(self):
        ax = None
        for link_id in range(len(self.links)):
            show = link_id == (len(self.links)-1)
            ax = self.links[link_id].view(ax, show)

    def mobility(self):
        L = len(self.links)
        G = len([i for i in self.links if isinstance(i, Ground)])
        # print(L, 'L', G, 'G')
        j = [i.classify() for i in self.joints]
        j1 = len([i for i in j if i == 'J1']) 
        j2 = len([i for i in j if i == 'J2']) 
        return 3*(L) - 2*j1 - j2 - 3*G
    
    def forces_analysis(self):
        for j in self.joints:
            j.force_analysis()
