import _pylsd
import numpy
from PIL import Image

class PyLSD:

    def __init__(self):
        pass

    def _lsd_defaults(self, im, X, Y):
        """
        Calls the LSD library with all the suggested values for the parameters.

        :param im: The pixel list. It should be some iterable.
        :para X: The size of the image in X
        :param Y: The size of the image in Y
        :returns: A matrix of N segments by 7.
        """

        image = numpy.array(im.getdata(), dtype=numpy.float64)
        # Calls the C method with all the suggested parameter values.
        s = _pylsd.line_segment_detection(image, X, Y, 0.8, 0.6, 2.0, 22.5, 0.0, 0.7, 1024)
        ans = numpy.array(s)
        ans = ans.reshape((len(s)/7, 7))
        return ans

    def write_seg_file(self, name, segs):
        """
        Writes the file with the segment information to emulate the original LSD cmd.

        :param name: The name of the desired file.
        :param segs: The calculated segments.
        """

        salida = open(name, 'w')
        for seg in segs:
            seg = numpy.around(seg, decimals=6)
            line = ' '.join("%.6f" % i for i in seg)
            salida.write(line + ' \n')

    def from_file(self, image_file):
        """
        Searchs for all the segments in an image.

        :param image_file: The name of the image file. PIL should be able to open it.
        :returns: A matrix of N segments by 7.
        """
        im = Image.open(image_file)
        X, Y = im.size
        return self._lsd_defaults(im, X, Y)

    def from_pixels(self, pixels, X, Y):
        """
        Lower level interface.

        :param pixels: The list of pixels. Should be an iterable.
        :para X: The size of the image in X
        :param Y: The size of the image in Y
        :returns: A matrix of N segments by 7.
        """
        return self._lsd_defaults(pixels, X, Y)
