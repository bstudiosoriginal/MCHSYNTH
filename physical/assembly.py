from physical.link import Link
from core.position import Position
class Assembly(object):

    def __init__(self, *links) -> None:
        # assemling links in order
        self.links = []
        for link in links:
            link.attach(link)
            self.links.append(link)
    
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
        
    def control(self, link_name, linear_velocity, angular_velocity, linear_acceleration, angular_acceleration):
        pass
