import numpy.linalg

import numpy


class Line:
    """ This class represents a line segment built upon an LSD description. """
    
    def __init__(self, text_line):
        """
        :param text_line: String containing a list of numbers separated by
            spaces. Format: x1, y1, x2, y2, width, p, -log10(NFA)
        :type text_line: string
        """
        text_line = text_line.strip()
        self.x1, self.y1, self.x2, self.y2, self.width, self.p, self.NFA = \
            [float(n) for n in text_line.split(" ")]
            
    def norm(self):
        """
        Returns the norm (length) of the line segment.
        """
        return numpy.linalg.norm([self.x2 - self.x1, self.y2 - self.y1])
        
    def angle(self):
        """
        Returns the angle of the line segment in radians.
        """
        
        return numpy.angle(numpy.complex(self.x2 - self.x1, self.y2 - self.y1),
            deg=True)
        
        
if __name__ == "__main__":
    entrada = open("pista2.txt", "r")
    
    lines = [Line(s) for s in entrada.readlines()]
    
    angles = [l.angle() for l in lines]
    print numpy.median(angles)
