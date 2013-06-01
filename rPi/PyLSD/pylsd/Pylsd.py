import _pylsd
import numpy
from PIL import Image

class PyLSD:

    def __init__(self):
        pass

    @staticmethod
    def lsd(image_file):
        """ Searchs for all the segments in an image. """

        im = Image.open(image_file)
        image = numpy.array(im.getdata())
        # Calls the C method with all the suggested parameter values.
        s = _pylsd.line_segment_detection(image, 0.8, 0.6, 2, 22.5, 0, 0.7, 1024)
        return s

