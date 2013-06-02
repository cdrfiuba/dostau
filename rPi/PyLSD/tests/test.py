import pylsd.Pylsd
from numpy import around

lsd = pylsd.Pylsd.PyLSD()

segs = lsd.lsd('chairs.png')

salida = open('python-generated.txt', 'w')
for seg in segs:
    seg = around(seg, decimals=6)
    line = ' '.join("%.6f" % i for i in seg)
    salida.write(line + ' \n')
