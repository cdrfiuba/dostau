from distutils.core import setup, Extension

_pylsd_c = Extension('_pylsd', sources=['_pylsd_c/pylsd.c', '_pylsd_c/lsd.c'],
                     extra_compile_args=['-O3'])


setup(name='pylsd',
      version='1.0',
      ext_modules=[_pylsd_c],
      packages=['pylsd'],

      # metadata for upload to PyPI
      author = "Lucas Chiesa",
      author_email = "lucas.chiesa@gmail.com",
      description = "PyLSD - a Python wrapper for the LSD library.",
      license = "LGPL",
      keywords = "image lines",
)
