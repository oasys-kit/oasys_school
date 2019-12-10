try:
    from oasys_srw.srwlib import *
    from oasys_srw.uti_plot import *
except:
    from srwlib import *
    from uti_plot import *

import numpy

if not srwl_uti_proc_is_master(): exit()

####################################################
# LIGHT SOURCE

part_beam = SRWLPartBeam()
part_beam.Iavg               = 0.2
part_beam.partStatMom1.x     = 0.0
part_beam.partStatMom1.y     = 0.0
part_beam.partStatMom1.z     = -2.35
part_beam.partStatMom1.xp    = 0.0
part_beam.partStatMom1.yp    = 0.0
part_beam.partStatMom1.gamma = 11741.70718709478
part_beam.arStatMom2[0]      = 2.1904000000000003e-10
part_beam.arStatMom2[1]      = 0.0
part_beam.arStatMom2[2]      = 7.839999999999999e-12
part_beam.arStatMom2[3]      = 1.3690000000000002e-11
part_beam.arStatMom2[4]      = 0.0
part_beam.arStatMom2[5]      = 2.2500000000000003e-12
part_beam.arStatMom2[10]     = 1.9043999999999997e-06

magnetic_fields = []
magnetic_fields.append(SRWLMagFldH(1, 'v', 
                                   _B=0.3672543251653384, 
                                   _ph=0.0, 
                                   _s=-1, 
                                   _a=1.0))
magnetic_structure = SRWLMagFldU(_arHarm=magnetic_fields, _per=0.025, _nPer=184.0)
magnetic_field_container = SRWLMagFldC(_arMagFld=[magnetic_structure], 
                                       _arXc=array('d', [0.0]), 
                                       _arYc=array('d', [0.0]), 
                                       _arZc=array('d', [0.0]))

mesh = SRWLRadMesh(_eStart=10000.000703034077,
                   _eFin  =10000.000703034077,
                   _ne    =1,
                   _xStart=-0.001,
                   _xFin  =0.001,
                   _nx    =201,
                   _yStart=-0.001,
                   _yFin  =0.001,
                   _ny    =201,
                   _zStart=28.0)

stk = SRWLStokes()
stk.allocate(1,201,201)
stk.mesh = mesh

wfr = SRWLWfr()
wfr.allocate(mesh.ne, mesh.nx, mesh.ny)
wfr.mesh = mesh
wfr.partBeam = part_beam

initial_mesh = deepcopy(wfr.mesh)
srwl.CalcElecFieldSR(wfr, 0, magnetic_field_container, [1,0.01,0.0,0.0,50000,1,0.0])

mesh0 = deepcopy(wfr.mesh)
arI = array('f', [0]*mesh0.nx*mesh0.ny)
srwl.CalcIntFromElecField(arI, wfr, 6, 0, 3, mesh0.eStart, 0, 0)
arIx = array('f', [0]*mesh0.nx)
srwl.CalcIntFromElecField(arIx, wfr, 6, 0, 1, mesh0.eStart, 0, 0)
arIy = array('f', [0]*mesh0.ny)
srwl.CalcIntFromElecField(arIy, wfr, 6, 0, 2, mesh0.eStart, 0, 0)
#save ascii file with intensity
#srwl_uti_save_intens_ascii(arI, mesh0, <file_path>)
plotMesh0x = [1000*mesh0.xStart, 1000*mesh0.xFin, mesh0.nx]
plotMesh0y = [1000*mesh0.yStart, 1000*mesh0.yFin, mesh0.ny]
uti_plot2d1d (arI, plotMesh0x, plotMesh0y, labels=['Horizontal Position [mm]', 'Vertical Position [mm]', 'Intensity Before Propagation'])

####################################################
# BEAMLINE

srw_oe_array = []
srw_pp_array = []

oe_0=SRWLOptA(_shape='r',
               _ap_or_ob='a',
               _Dx=0.001,
               _Dy=0.001,
               _x=0.0,
               _y=0.0)

pp_oe_0 = [0,0,1.0,0,0,1.0,2.0,1.0,2.0,0,0.0,0.0]

srw_oe_array.append(oe_0)
srw_pp_array.append(pp_oe_0)

drift_after_oe_0 = SRWLOptD(1.0)
pp_drift_after_oe_0 = [0,0,1.0,1,0,1.0,1.0,1.0,1.0,0,0.0,0.0]

srw_oe_array.append(drift_after_oe_0)
srw_pp_array.append(pp_drift_after_oe_0)

acceptance_slits_oe_1=SRWLOptA(_shape='r',
               _ap_or_ob='a',
               _Dx=0.01,
               _Dy=0.0009983272956896516,
               _x=0.0,
               _y=0.0)

oe_1 = SRWLOptMirEl(_size_tang=0.4,
                     _size_sag=0.01,
                     _p=29.0,
                     _q=26.0,
                     _ang_graz=0.0024958208303519033,
                     _ap_shape='r',
                     _sim_meth=2,
                     _treat_in_out=1,
                     _nvx=0,
                     _nvy=0.9999968854408081,
                     _nvz=-0.002495818239224129,
                     _tvx=0,
                     _tvy=-0.002495818239224129,
                     _x=0.0,
                     _y=0.0)
oe_1.set_dim_sim_meth(_size_tang=0.4,
                      _size_sag=0.01,
                      _ap_shape='r',
                      _sim_meth=2,
                      _treat_in_out=1)
oe_1.set_orient(_nvx=0,
                 _nvy=0.9999968854408081,
                 _nvz=-0.002495818239224129,
                 _tvx=0,
                 _tvy=-0.002495818239224129,
                 _x=0.0,
                 _y=0.0)


pp_acceptance_slits_oe_1 = [0,0,1.0,0,0,1.0,1.0,1.0,1.0,0,0.0,0.0]
pp_oe_1 = [0,0,1.0,0,0,1.0,1.0,1.0,1.0,0,0.0,0.0]

srw_oe_array.append(acceptance_slits_oe_1)
srw_pp_array.append(pp_acceptance_slits_oe_1)

srw_oe_array.append(oe_1)
srw_pp_array.append(pp_oe_1)

drift_before_oe_2 = SRWLOptD(6.0)
pp_drift_before_oe_2 = [0,0,1.0,1,0,1.0,1.0,1.0,1.0,0,0.0,0.0]

srw_oe_array.append(drift_before_oe_2)
srw_pp_array.append(pp_drift_before_oe_2)

acceptance_slits_oe_2=SRWLOptA(_shape='r',
               _ap_or_ob='a',
               _Dx=0.0009983272956896516,
               _Dy=0.01,
               _x=0.0,
               _y=0.0)

oe_2 = SRWLOptMirEl(_size_tang=0.4,
                     _size_sag=0.01,
                     _p=35.0,
                     _q=20.0,
                     _ang_graz=0.0024958208303519033,
                     _ap_shape='r',
                     _sim_meth=2,
                     _treat_in_out=1,
                     _nvx=0.9999968854408081,
                     _nvy=0,
                     _nvz=-0.002495818239224129,
                     _tvx=-0.002495818239224129,
                     _tvy=0,
                     _x=0.0,
                     _y=0.0)
oe_2.set_dim_sim_meth(_size_tang=0.4,
                      _size_sag=0.01,
                      _ap_shape='r',
                      _sim_meth=2,
                      _treat_in_out=1)
oe_2.set_orient(_nvx=0.9999968854408081,
                 _nvy=0,
                 _nvz=-0.002495818239224129,
                 _tvx=-0.002495818239224129,
                 _tvy=0,
                 _x=0.0,
                 _y=0.0)


pp_acceptance_slits_oe_2 = [0,0,1.0,0,0,1.0,1.0,1.0,1.0,0,0.0,0.0]
pp_oe_2 = [0,0,1.0,0,0,1.0,1.0,1.0,1.0,0,0.0,0.0]

srw_oe_array.append(acceptance_slits_oe_2)
srw_pp_array.append(pp_acceptance_slits_oe_2)

srw_oe_array.append(oe_2)
srw_pp_array.append(pp_oe_2)

drift_before_oe_3 = SRWLOptD(20.0)
pp_drift_before_oe_3 = [0,0,1.0,2,0,1.0,1.0,1.0,1.0,0,0.0,0.0]

srw_oe_array.append(drift_before_oe_3)
srw_pp_array.append(pp_drift_before_oe_3)


drift_before_oe_4 = SRWLOptD(100.0)
pp_drift_before_oe_4 = [0,0,1.0,2,0,1.0,1.0,1.0,1.0,0,0.0,0.0]

srw_oe_array.append(drift_before_oe_4)
srw_pp_array.append(pp_drift_before_oe_4)



####################################################
# PROPAGATION

optBL = SRWLOptC(srw_oe_array, srw_pp_array)
srwl.PropagElecField(wfr, optBL)

mesh1 = deepcopy(wfr.mesh)
arI1 = array('f', [0]*mesh1.nx*mesh1.ny)
srwl.CalcIntFromElecField(arI1, wfr, 6, 0, 3, mesh1.eStart, 0, 0)
arI1x = array('f', [0]*mesh1.nx)
srwl.CalcIntFromElecField(arI1x, wfr, 6, 0, 1, mesh1.eStart, 0, 0)
arI1y = array('f', [0]*mesh1.ny)
srwl.CalcIntFromElecField(arI1y, wfr, 6, 0, 2, mesh1.eStart, 0, 0)
#save ascii file with intensity
#srwl_uti_save_intens_ascii(arI1, mesh1, <file_path>)
plotMesh1x = [1000*mesh1.xStart, 1000*mesh1.xFin, mesh1.nx]
plotMesh1y = [1000*mesh1.yStart, 1000*mesh1.yFin, mesh1.ny]
uti_plot2d1d(arI1, plotMesh1x, plotMesh1y, labels=['Horizontal Position [mm]', 'Vertical Position [mm]', 'Intensity After Propagation'])
uti_plot_show()
