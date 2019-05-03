
import numpy
from PyQt5.QtWidgets import QApplication
from srxraylib.plot.gol import plot
from orangecontrib.xoppy.widgets.optics.xcrystal import OWxcrystal


def run_xcrystal(energy=5000.0):
    w.CRYSTAL_MATERIAL = 32
    w.MILLER_INDEX_H = 1
    w.MILLER_INDEX_K = 1
    w.MILLER_INDEX_L = 1
    w.TEMPER = 1
    w.MOSAIC = 0
    w.GEOMETRY = 0
    w.SCAN = 2
    w.UNIT = 1
    w.SCANFROM = -100
    w.SCANTO = 150
    w.SCANPOINTS = 200
    w.ENERGY = energy
    w.ASYMMETRY_ANGLE = 0.0
    w.THICKNESS = 1.0
    # w.MOSAIC_FWHM = 0
    # w.RSAG = 0
    # w.RMER = 0
    # w.ANISOTROPY = 0
    # w.POISSON = 0
    # w.CUT = ""
    # w.FILECOMPLIANCE = ""

    tmp = w.xoppy_calc_xcrystal()

    a = numpy.loadtxt("diff_pat.dat",skiprows=5)
    # L  Th-ThB{in} [microrad]  Th-ThB{out} [microrad]  phase_p[rad]  phase_s[rad]  Circ Polariz  p-polarized  s-polarized
    print(a.shape)
    plot(a[:,0],a[:,-1],title="Energy = %f eV "%energy)

    step = a[1,0] - a[0,0]
    h = a[:,-1]
    peak = a[:,-1].max()
    integrated_intensity = a[:, -1].sum()*step
    tt = numpy.where(h >= max(h) * 0.5)
    fwhm = step * (tt[0][-1] - tt[0][0])

    print("Peak value = ",peak)
    print("Integrated intensity [urad] = ", integrated_intensity )
    print("FWHM=",fwhm)
    return peak,integrated_intensity,fwhm



app = QApplication([""])
w = OWxcrystal()

P = []
I = []
FWHM = []
ENERGIES = [5000,8000,12000,50000,80000,120000]
for energy in ENERGIES:

    p, i, fwhm = run_xcrystal(energy)
    P.append(p)
    I.append(i)
    FWHM.append(fwhm)

print("Photon energy [eV],   Peak    IntegratedIntensity   FWHM")
for i in range(len(ENERGIES)):
    print("%d  %3.2f  %3.2f  %5.3f "%(ENERGIES[i],P[i],I[i],FWHM[i]))

