from typing import Iterable

class Side(set):
    '''Essentially a set but equality is containment (i'm lazy)'''
    def __eq__(self, other): #override
        return other in list(self)
    
    def __contains__(self, other):
        for item in self:
            if other in item:
                return True
            
    def is_transformable(self):
        if "trash" in self:
            return False
        if "wall" in self:
            return False
        return True
