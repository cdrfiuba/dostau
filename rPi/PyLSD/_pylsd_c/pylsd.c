#include "Python.h"
#include "numpy/arrayobject.h"
#include "lsd.h"
#include <math.h>

static PyObject *line_segment_detection(PyObject *self, PyObject *args);
double *pyvector_to_Carrayptrs(PyArrayObject *arrayin);

/* Method docstrings */
char _pylsd_docs[] =
"This module wraps the LSD line segment detection library.\n \
 More information on http://www.ipol.im/pub/art/2012/gjmr-lsd/";

char line_segment_detection_docs[] =
"line_segment_detection(img, X, Y, scale, sigma_scale, quant, ang_th, log_eps, density_th, n_bins)\n \
 Looks for all the line segments in the image.\n \
 \n \
 :param img: Pointer to input image data. It must be an array of\n \
   doubles of size X x Y, and the pixel at coordinates\n \
   (x,y) is obtained by img[x+y*X].\n \
 :param X: The size of the image in pixels, in the X axis.\n \
 :param Y: The size of the image in pixels, in the Y axis.\n \
 :param scale: When different from 1.0, LSD will scale the input image\n \
   by 'scale' factor by Gaussian filtering, before detecting\n \
   line segments.\n \
   Example: if scale=0.8, the input image will be subsampled\n \
   to 80% of its size, before the line segment detector\n \
   is applied.\n \
   Suggested value: 0.8\n \
 :param sigma_scale: When scale!=1.0, the sigma of the Gaussian filter is:\n \
   sigma = sigma_scale / scale,   if scale <  1.0\n \
   sigma = sigma_scale,           if scale >= 1.0\n \
   Suggested value: 0.6\n \
 :param quant: Bound to the quantization error on the gradient norm.\n \
   Example: if gray levels are quantized to integer steps,\n \
   the gradient (computed by finite differences) error\n \
   due to quantization will be bounded by 2.0, as the\n \
   worst case is when the error are 1 and -1, that\n \
   gives an error of 2.0.\n \
   Suggested value: 2.0\n \
 :param ang_th: Gradient angle tolerance in the region growing\n \
   algorithm, in degrees.\n \
   Suggested value: 22.5\n \
 :param log_eps: Detection threshold, accept if -log10(NFA) > log_eps.\n \
   The larger the value, the more strict the detector is,\n \
   and will result in less detections.\n \
   (Note that the 'minus sign' makes that this\n \
   behavior is opposite to the one of NFA.)\n \
   The value -log10(NFA) is equivalent but more\n \
   intuitive than NFA:\n \
   - -1.0 gives an average of 10 false detections on noise\n \
   -  0.0 gives an average of 1 false detections on noise\n \
   -  1.0 gives an average of 0.1 false detections on nose\n \
   -  2.0 gives an average of 0.01 false detections on noise\n \
   Suggested value: 0.0\n \
 :param density_th: Minimal proportion of 'supporting' points in a rectangle.\n \
   Suggested value: 0.7\n \
 :param n_bins: Number of bins used in the pseudo-ordering of gradient\n \
   modulus.\n \
   Suggested value: 1024\n \
 :returns: A double array of size 7 x n_out, containing the list\n \
   of line segments detected. The array contains first\n \
   7 values of line segment number 1, then the 7 values\n \
   of line segment number 2, and so on, and it finish\n \
   by the 7 values of line segment number n_out.\n \
   The seven values are:\n \
   - x1,y1,x2,y2,width,p,-log10(NFA)\n \
   for a line segment from coordinates (x1,y1) to (x2,y2),\n \
   a width 'width', an angle precision of p in (0,1) given\n \
   by angle_tolerance/180 degree, and NFA value 'NFA'.\n \
   If 'out' is the returned pointer, the 7 values of\n \
   line segment number 'n+1' are obtained with\n \
   'out[7*n+0]' to 'out[7*n+6]'.";

// Method table. States the name of the functions inside Python.
static PyMethodDef _pylsdMethods[] = {
  {"line_segment_detection", line_segment_detection, METH_VARARGS, line_segment_detection_docs}
};

// Module initialization function.
PyMODINIT_FUNC init_pylsd(void) {
  (void) Py_InitModule3("_pylsd", _pylsdMethods, _pylsd_docs);
  // Must be present for NumPy.  Called first after above line.
  import_array();
}


static PyObject* line_segment_detection(PyObject* self, PyObject* args)
{
  // Python Object pointers
  PyArrayObject *pyImage;
  PyObject* py_return_value = NULL;
  // C array pointers
  double *cImage;
  double *segs;
  // LSD tunning parameters
  double scale, sigma_coef, quant, ang_th, log_eps, density_th;
  int n_bins, X, Y;
  // number of segments (return value from lsd)
  int n, i, len;

  // parse python arguments into C vars.
  if (!PyArg_ParseTuple(args, "O!iiddddddi", &PyArray_Type, &pyImage, &X, &Y, &scale,
        &sigma_coef, &quant, &ang_th, &log_eps, &density_th, &n_bins)) return NULL;

  cImage = pyvector_to_Carrayptrs(pyImage);

  // Call the LSD library.
  segs = LineSegmentDetection(&n, cImage, X, Y, scale, sigma_coef, quant, ang_th,
      log_eps, density_th, n_bins, NULL, NULL, NULL);

  len = n * 7; // n segments 7 values each.
  py_return_value = PyTuple_New(len);
  for(i=0; i < len; i++) {
    PyTuple_SET_ITEM(py_return_value, i, PyFloat_FromDouble(segs[i]));
  }
  return py_return_value;
}

/* Create 1D Carray from PyArray Assumes PyArray is contiguous in memory. */
double *pyvector_to_Carrayptrs(PyArrayObject *arrayin)  {
  /* pointer to arrayin data as double */
  return (double *) arrayin->data;
}
