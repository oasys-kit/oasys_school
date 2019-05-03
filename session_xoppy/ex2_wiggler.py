




print(dir(in_object_1))

print(in_object_1.get_contents("xoppy_data").shape)

eV = in_object_1.get_contents("xoppy_data")[:,0]
flux = in_object_1.get_contents("xoppy_data")[:,1]
cumulated_power = in_object_1.get_contents("xoppy_data")[:,3]

#


print("Max flux: %g at energy [eV]: %d"%(flux.max(),eV[flux.argmax()]))
print("Integrated power [W]: %4.2f  " % (cumulated_power[-1]))

#from srxraylib.plot.gol import plot
#plot(eV,flux,xlog=True,ylog=True,xtitle="Photon energy [eV]",ytitle="Flux [ph/s/0.1\%bw]")
