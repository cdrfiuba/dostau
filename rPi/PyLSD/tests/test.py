import pylsd.Pylsd
from numpy import around

lsd = pylsd.Pylsd.PyLSD()

segs = lsd.from_file('chairs.png')
lsd.write_seg_file('python-generated.txt', segs)
