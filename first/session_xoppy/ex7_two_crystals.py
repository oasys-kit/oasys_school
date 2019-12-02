

import numpy
from srxraylib.plot.gol import plot


def autoconvolution(x,y):
    c = numpy.convolve(y, y)
    # normalization factor = 1/sqrt( integral(f1)*integral(f2) )
    c /= y.sum()
    x0 = x[0] - 0.5 * (x[-1] - x[0])
    x1 = x[-1] + 0.5 * (x[-1] - x[0])
    xnew = numpy.arange(x0, x1, x[1] - x[0])
    if xnew.size != c.size:
        imax = numpy.min([c.size,xnew.size])
        xnew = xnew[0:(imax - 1)]
        c = c[0:(imax - 1)]
    return xnew,c

a = numpy.loadtxt("diff_pat.dat", skiprows=5)
# L  Th-ThB{in} [microrad]  Th-ThB{out} [microrad]  phase_p[rad]  phase_s[rad]  Circ Polariz  p-polarized  s-polarized
x = a[:,0]
y = a[:,-1]


xnew, c = autoconvolution(x,y)

plot(x,y,x,y**2,xnew,c,xtitle="Angle [urad]",ytitle="Reflectivity",legend=["Single reflection","double reflection","Rocking curve"])
