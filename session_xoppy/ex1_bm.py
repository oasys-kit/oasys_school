

def run_bm(BFIELD_T=0.856):
    #
    # script to make the calculations (created by XOPPY:bm)
    #
    from orangecontrib.xoppy.util.xoppy_bm_wiggler import xoppy_calc_bm

    # TYPE_CALC:
    # 0: 'Energy or Power spectra'
    # 1: 'Angular distribution (all wavelengths)'
    # 2: 'Angular distribution (one wavelength)'
    # 3: '2D flux and power (angular,energy) distribution'
    #

    a6, fm, a, energy_ev = xoppy_calc_bm(
        TYPE_CALC=0,
        MACHINE_NAME="bending magnet",
        RB_CHOICE=1,
        MACHINE_R_M=25.2,
        BFIELD_T=BFIELD_T,
        BEAM_ENERGY_GEV=6.0,
        CURRENT_A=0.2,
        HOR_DIV_MRAD=1.0,
        VER_DIV=0,
        PHOT_ENERGY_MIN=100.0,
        PHOT_ENERGY_MAX=100100.0,
        NPOINTS=500,
        LOG_CHOICE=0,
        PSI_MRAD_PLOT=1.0,
        PSI_MIN=-1.0,
        PSI_MAX=1.0,
        PSI_NPOINTS=500,
        FILE_DUMP=True)  # writes output to bm.spec
    #
    # end script
    #
    print(a6.shape)
    print(a6[0,:])
    return a6[:,0].copy(),a6[:,5].copy(),a6[:,6].copy()




from srxraylib.plot.gol import plot


eV, f8, p8 = run_bm(BFIELD_T=0.856)
eV, f55, p55 = run_bm(BFIELD_T=0.55)
eV, f4, p4 = run_bm(BFIELD_T=0.4)
#


print("Max flux: %g  %g  %g at energies [eV]: %d  %d  %d"%(f8.max(),f55.max(),f4.max(),eV[f8.argmax()],eV[f55.argmax()],eV[f4.argmax()]))
print("Critical energy [eV]: %d  %d  %d " % (665*6**2*0.856, 665*6**2*0.55, 665*6**2*0.4))
eStep = eV[1] - eV[0]
print("Integrated power [W]: %4.2f  %4.2f  %4.2f " % (p8.sum()*eStep,p55.sum()*eStep,p4.sum()*eStep))

plot(eV,f8,eV,f55,eV,f4,xlog=True,ylog=True,xtitle="Photon energy [eV]",ytitle="Flux [ph/s/0.1\%bw",legend=["B=0.856T","B=0.55T","B=0.4T"])
