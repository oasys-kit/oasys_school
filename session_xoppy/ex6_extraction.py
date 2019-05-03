
import numpy
from srxraylib.plot.gol import plot

a = numpy.loadtxt("/users/srio/OASYS1.1d/oasys_school/session1.1_xoppy/power.spec",skiprows=23)
print(a.shape)

#L  Photon Energy [eV]  Source  [oe 1] Total CS cm2/g  [oe 1] Mu cm^-1  [oe 1] Transmitivity   [oe 1] Absorption   Intensity after oe #1  [oe 2] 1-Re[n]=delta  [oe 2] Im[n]=beta  [oe 2] delta/beta  [oe 2] Reflectivity-s  [oe 2] Transmitivity  Intensity after oe #2  [oe 3] Total CS cm2/g  [oe 3] Mu cm^-1  [oe 3] Transmitivity   [oe 3] Absorption   Intensity after oe #3  [oe 4] Total CS cm2/g  [oe 4] Mu cm^-1  [oe 4] Transmitivity   [oe 4] Absorption   Intensity after oe #4
#   0                   1       2                      3                4                      5                   6                      7                     8                  9                  10                     11                    12                     13

plot(a[:,0],a[:,4],
     a[:,0],a[:,4+6],
     a[:,0],a[:,4+6+5],
     a[:,0],a[:,4+6+5+5],
     xtitle="Photon ENergy [eV]",ytitle="Transmittance",legend=["Attenuator Be 500 um","Mirror Rh 3mrad","Attenuator Al 50 um","Attenuatot Mo 10 um"])