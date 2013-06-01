import numpy.linalg
import numpy
import pygame


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
        if self.y1 < self.y2:
            temp = self.y1
            self.y1 = self.y2
            self.y2 = temp
            temp = self.x1
            self.x1 = self.x2
            self.x2 = temp
            
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
        
def testAngles():
    entrada = open("pista1.txt", "r")
    lines = [Line(s) for s in entrada.readlines()]
    angles = [l.angle() for l in lines]
    print "Pista 1:"
    print "Median = ", numpy.median(angles)
    print "Mean = ", numpy.mean(angles)

    print

    entrada = open("pista2.txt", "r")
    lines = [Line(s) for s in entrada.readlines()]
    angles = [l.angle() for l in lines]
    print "Pista 2:"
    print "Median = ", numpy.median(angles)
    print "Mean = ", numpy.mean(angles)
    
def testVideo():
    pygame.init()
    video = pygame.movie.Movie("/home/ernesto/Videos/Webcam/pista.mpg")
    
    s = video.get_size()
    screen = pygame.display.set_mode(s)
    
    video.set_display(screen)
    #video.play()
    
    f = 0
    playing = True
    while playing:
        rf = video.render_frame(f)
        if rf != f:
            playing = False
        else:
            f += 1
    

if __name__ == "__main__":
    #testAngles()
    testVideo()
    
