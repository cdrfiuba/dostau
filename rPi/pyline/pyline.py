import numpy.linalg
import numpy
import pygame
import math
import os


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
            deg=False)
        
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
    videosurf = pygame.Surface(s)
    
    video.set_display(videosurf)
    #video.play()
    
    f = 1
    playing = True
    while playing:
        rf = video.render_frame(f)
        
        pygame.event.pump()
        
        if rf != f or pygame.key.get_pressed()[pygame.K_ESCAPE]:
            playing = False
        else:
            if (f%5) == 0:
                pygame.image.save(videosurf, "frame.tga")
                os.system("convert frame.tga frame.pgm")
                os.system("./lsd frame.pgm frame.txt")
                entrada = open("frame.txt", "r")
                lines = [Line(s) for s in entrada.readlines()]
                angles = [l.angle() for l in lines]
                alfa = numpy.median(angles)
                x0 = screen.get_width()/2
                y0 = screen.get_height()
                x1 = x0 + math.cos(alfa)*200
                y1 = y0 + math.sin(alfa)*200
                pygame.draw.line(videosurf, (255, 0, 0), (x0, y0), (x1, y1), 5)
                screen.blit(videosurf, (0, 0))
                pygame.display.flip()
            f += 1
    
    os.system("rm frame.tga frame.pgm frame.txt")


if __name__ == "__main__":
    #testAngles()
    testVideo()
    
