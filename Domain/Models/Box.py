
class Box:
    def __init__(self, x1, y1, x2, y2):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
    
    @classmethod
    def from_dict(cls, dict : dict) -> 'Box':
        return cls(
                x1 = dict['x1'], 
                y1 = dict['y1'], 
                x2 = dict['x2'], 
                y2 = dict['y2']
            ) 
    
    def to_dict(self) -> dict:
        return {
            'x1' : self.x1,
            'y1' : self.y1,
            'x2' : self.x2,
            'y2' : self.y2
        }
    
    def to_tuple(self) -> tuple:
        return (self.x1, self.y1, self.x2, self.y2)
    
    @classmethod
    def from_tuple(cls, tuple : tuple) -> 'Box':
        """ This method creates a Box object from a tuple of 4 elements
        the order of the elements must be (x1, y1, x2, y2)"""
        
        return cls(
                x1 = tuple[0], 
                y1 = tuple[1], 
                x2 = tuple[2], 
                y2 = tuple[3]
            )