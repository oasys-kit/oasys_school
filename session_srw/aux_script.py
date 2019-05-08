try:
    mesh = in_object_1._SRWData__srw_wavefront.mesh
    print('Propagated wavefront:')
    print('Nx = %d, Ny = %d' % (mesh.nx, mesh.ny))
    print('dx = %.4f um, dy = %.4f um' % ((mesh.xFin - mesh.xStart) * 1E6 / mesh.nx, (mesh.yFin - mesh.yStart) * 1E6 / mesh.ny))
    print('range x = %.4f um, range y = %.4f um' % ((mesh.xFin - mesh.xStart) * 1E6, (mesh.yFin - mesh.yStart) * 1E6))
except:
    pass

try:
    mesh = in_object_2._SRWData__srw_wavefront.mesh
    print('Propagated wavefront:')
    print('Nx = %d, Ny = %d' % (mesh.nx, mesh.ny))
    print('dx = %.4f um, dy = %.4f um' % ((mesh.xFin - mesh.xStart) * 1E6 / mesh.nx, (mesh.yFin - mesh.yStart) * 1E6 / mesh.ny))
    print('range x = %.4f um, range y = %.4f um' % ((mesh.xFin - mesh.xStart) * 1E6, (mesh.yFin - mesh.yStart) * 1E6))
except:
    pass
