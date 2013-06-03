import numpy.linalg
import numpy
import pygame
import math
import os
from PIL import Image

# LSD wrapper
import pylsd.Pylsd


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
        return numpy.angle(numpy.complex(self.x2 - self.x1, self.y2 - self.y1), deg=False)
        
def toGray(surf):
    img = Image.fromstring("RGB", surf.get_size(), pygame.image.tostring(surf, "RGB", False))
    img = img.convert("L")
    img = img.convert("RGB")
    newsurf = pygame.image.fromstring(img.tostring(), surf.get_size(), "RGB", False)
    return newsurf
    
def getArray(surf):
    pxarray = pygame.surfarray.array3d(surf)
    a = pxarray[:, :, 1]  # obtain only one channel from a gray-scale image
    a = a.transpose()  # put image in the format that LSD likes
    b = numpy.ravel(a)  # linearize array
    return b
    
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
    lsd = pylsd.Pylsd.PyLSD()
    pygame.init()
    video = pygame.movie.Movie("./pista.mpg")

    s = video.get_size()
    screen = pygame.display.set_mode(s)
    videosurf = pygame.Surface(s)
    
    video.set_display(videosurf)
    #video.play()

    f = 2
    playing = True
    while playing:
        rf = video.render_frame(f)  # render frame f in video buffer
        pygame.event.pump()  # force keyboard event polling

        if rf != f or pygame.key.get_pressed()[pygame.K_ESCAPE]:
            playing = False
        else:
            if (f%1) == 0:  # skip some frames for faster processing
                #grayvideosurf = toGray(videosurf)
                grayvideosurf = videosurf  # if using an already gray video
                X, Y = grayvideosurf.get_size()
                a = getArray(grayvideosurf)
                segs = lsd.from_pixels(a, X, Y)
                lsd.write_seg_file('extract.txt', segs)
                #pygame.image.save(videosurf, "extract.tga")
                #os.system("convert extract.tga extract.pgm")
                #os.system("./lsd extract.pgm extract.txt")
                entrada = open("extract.txt", "r")
                lines = [Line(s) for s in entrada.readlines()]
                angles = [l.angle() for l in lines]
                alfa = numpy.median(angles)
                x0 = screen.get_width()/2
                y0 = screen.get_height()
                x1 = x0 + math.cos(alfa)*200
                y1 = y0 + math.sin(alfa)*200
                pygame.draw.line(grayvideosurf, (255, 0, 0), (x0, y0), (x1, y1), 5)
                #pygame.image.save(videosurf, "frame%04u.tga"%f)
                screen.blit(grayvideosurf, (0, 0))
                pygame.display.flip()
            f += 1

    #os.system("rm extract.txt")
    # generate movie
    #os.system("""mencoder "mf://frame*.tga" -mf fps=25 -ovc lavc -lavcopts vhq:vbitrate=600 -o movie.avi""")
    # delete the frames
    #os.system("rm frame*.tga")
    
def testLsd():
    lsd = pylsd.Pylsd.PyLSD()
    segs = lsd.from_file("pista1.pgm")
    lsd.write_seg_file('extract.txt', segs)

if __name__ == "__main__":
    #testAngles()
    testVideo()
    #testLsd()
