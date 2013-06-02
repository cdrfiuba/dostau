import _pylsd
import numpy
from PIL import Image

class PyLSD:

    def __init__(self):
        pass

    @staticmethod
    def lsd(image_file):
        """
        Searchs for all the segments in an image.

        :param image_file: The name of the image file. PIL should be able to open it.
        :returns: A matrix of N segments by 7.
        """
        im = Image.open(image_file)
        X, Y = im.size
        image = numpy.array(im.getdata(), dtype=numpy.float64)
        # Calls the C method with all the suggested parameter values.
        s = _pylsd.line_segment_detection(image, X, Y, 0.8, 0.6, 2.0, 22.5, 0.0, 0.7, 1024)
        ans = numpy.array(s)
        ans = ans.reshape((len(s)/7, 7))
        return ans
