# https://gitlab.esrf.fr/srio/ebs-readiness/blob/master/bm05/scan_energies.py

#
# Python script to run shadow3. Created automatically with ShadowTools.make_python_script_from_list().
#
import Shadow
import numpy
import srxraylib.sources.srfunc as srfunc


def run_preprocessor(photon_energy):
    wigFile = "xshwig.sha"
    inData = ""

    nPer = 1  # 50
    nTrajPoints = 501
    ener_gev = 6.0
    trajFile = "tmp.traj"
    shift_x_flag = 4
    shift_x_value = 0.0
    shift_betax_flag = 5
    shift_betax_value = 0.0055

    # magnetic field from B(s) map
    (traj, pars) = srfunc.wiggler_trajectory(b_from=1, nPer=1, nTrajPoints=100, \
                                             ener_gev=ener_gev,
                                             inData="http://ftp.esrf.eu/pub/scisoft/syned/resources/SW_2PA.txt",
                                             trajFile="tmp.traj",
                                             shift_x_flag=shift_x_flag, shift_x_value=shift_x_value,
                                             shift_betax_flag=shift_betax_flag, shift_betax_value=shift_betax_value
                                             )

    # traj[0,ii] = yx[i]
    # traj[1,ii] = yy[i]+j * per - start_len
    # traj[2,ii] = 0.0
    # traj[3,ii] = betax[i]
    # traj[4,ii] = betay[i]
    # traj[5,ii] = 0.0
    # traj[6,ii] = curv[i]
    # traj[7,ii] = bz[i]

    # plot(traj[1,:],traj[0,:])
    # print(pars)

    #
    # calculate cdf and write file for Shadow/Source
    #
    srfunc.wiggler_cdf(traj,
                       enerMin=photon_energy,
                       enerMax=photon_energy + 10,
                       enerPoints=1001,
                       outFile=wigFile,
                       elliptical=False)

    print("CDF written to file %s \n" % (str(wigFile)))

    return traj


def run_shadow():
    #
    # Python script to run shadow3. Created automatically with ShadowTools.make_python_script_from_list().
    #
    # write (1) or not (0) SHADOW files start.xx end.xx star.xx
    iwrite = 0

    #
    # initialize shadow3 source (oe0) and beam
    #
    beam = Shadow.Beam()
    oe0 = Shadow.Source()
    oe1 = Shadow.OE()

    #
    # Define variables. See meaning of variables in:
    #  https://raw.githubusercontent.com/srio/shadow3/master/docs/source.nml
    #  https://raw.githubusercontent.com/srio/shadow3/master/docs/oe.nml
    #

    oe0.BENER = 6.0
    oe0.CONV_FACT = 100.0
    oe0.EPSI_DX = 89.4
    oe0.EPSI_DZ = -104.8
    oe0.EPSI_X = 2.16e-08
    oe0.EPSI_Z = 5e-10
    oe0.FDISTR = 0
    oe0.FILE_TRAJ = b'xshwig.sha'
    oe0.FSOUR = 0
    oe0.FSOURCE_DEPTH = 0
    oe0.F_COLOR = 0
    oe0.F_PHOT = 0
    oe0.F_WIGGLER = 1
    oe0.HDIV1 = 1.0
    oe0.HDIV2 = 1.0
    oe0.IDO_VX = 0
    oe0.IDO_VZ = 0
    oe0.IDO_X_S = 0
    oe0.IDO_Y_S = 0
    oe0.IDO_Z_S = 0
    oe0.ISTAR1 = 5676561
    oe0.NCOL = 0
    oe0.NPOINT = 100000
    oe0.NTOTALPOINT = 0
    oe0.N_COLOR = 0
    oe0.PH1 = 1000.0
    oe0.POL_DEG = 0.0
    oe0.SIGMAX = 0.0008757
    oe0.SIGMAY = 0.0
    oe0.SIGMAZ = 0.0001647
    oe0.VDIV1 = 1.0
    oe0.VDIV2 = 1.0
    oe0.WXSOU = 0.0
    oe0.WYSOU = 0.0
    oe0.WZSOU = 0.0

    oe1.DUMMY = 1.0
    oe1.FWRITE = 3
    oe1.F_REFRAC = 2
    oe1.F_SCREEN = 1
    oe1.I_SLIT = numpy.array([1, 0, 0, 0, 0, 0, 0, 0, 0, 0])
    oe1.N_SCREEN = 1
    oe1.RX_SLIT = numpy.array([12.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
    oe1.RZ_SLIT = numpy.array([6.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
    oe1.T_IMAGE = 0.0
    oe1.T_INCIDENCE = 0.0
    oe1.T_REFLECTION = 180.0
    oe1.T_SOURCE = 5800.0

    # Run SHADOW to create the source

    if iwrite:
        oe0.write("start.00")

    beam.genSource(oe0)

    if iwrite:
        oe0.write("end.00")
        beam.write("begin.dat")

    #
    # run optical element 1
    #
    print("    Running optical element: %d" % (1))
    if iwrite:
        oe1.write("start.01")

    beam.traceOE(oe1, 1)

    if iwrite:
        oe1.write("end.01")
        beam.write("star.01")

    # Shadow.ShadowTools.plotxy(beam,1,3,nbins=101,nolost=1,title="Real space")
    # Shadow.ShadowTools.plotxy(beam,1,4,nbins=101,nolost=1,title="Phase space X")
    # Shadow.ShadowTools.plotxy(beam,3,6,nbins=101,nolost=1,title="Phase space Z")

    return beam


if __name__ == "__main__":

    from srxraylib.plot.gol import plot, plot_image

    traj = run_preprocessor(photon_energy=1000)
    e, f2, tmp = srfunc.wiggler_spectrum(traj, enerMin=100.0, enerMax=150000.0, nPoints=111, \
                                         electronCurrent=0.2, outFile="tmp.dat", elliptical=False)
    plot(e, f2, xlog=1, ylog=1)


    f = open("scan_energies.dat", "w")
    f.write(
        "# photon_energy[eV] fraction_in_12x6cm_slit_at_58m  FWHM_H[um] FWHM_V[um] Flux(full emission)[ph/s/0.1%bw] Flux(in slit)[ph/s/0.1%bw]\n")

    for i in range(e.size):
        run_preprocessor(photon_energy=e[i])
        beam = run_shadow()


        intens = beam.intensity(nolost=1)
        tktH = beam.histo1(1, nbins=100, nolost=1, ref=23, )
        tktV = beam.histo1(3, nbins=100, nolost=1, ref=23, xrange=[-3.0, 3.0])

        print("Energy: %f " % (e[i]))
        print("Intensity: %f " % (intens / 100000))
        print("H fwhm: %f mm" % (10 * tktH["fwhm"]))
        print("V fwhm: %f mm" % (10 * tktV["fwhm"]))

        f.write("%f  %f  %f  %f  %g  %g \n" % (
            (e[i]),
            (intens / 100000),
            (10 * tktH["fwhm"]),
            (10 * tktV["fwhm"]),
            f2[i],
            f2[i] * intens / 100000.0,
        ))

    f.close()
    print("File written to disk: scan_energies.dat")


