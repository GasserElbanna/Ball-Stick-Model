#Import NEURON and Matplotlib
from neuron import h, gui
from matplotlib import pyplot

#Create Sections
soma = h.Section(name='soma')
dend = h.Section(name='dend')

#Connect dendrite to (1) end of the soma (Topology)
dend.connect(soma(1))
h.psection(sec=dend)

#Geometry
soma.L = soma.diam = 12.6157 # Makes a soma of 500 microns squared.
dend.L = 200 # microns
dend.diam = 1 # microns
print("Surface area of soma = {}".format(soma(0.5).area()))

#Biophysics
dend.Ra = 100    # Axial resistance in Ohm * cm
dend.cm = 1      # Membrane capacitance in micro Farads / cm^2

#Insert active Hodgkin-Huxley current in the soma
soma.insert('hh')
soma.gnabar_hh = 0.12  # Sodium conductance in S/cm2
soma.gkbar_hh = 0.036  # Potassium conductance in S/cm2
soma.gl_hh = 0.0003    # Leak conductance in S/cm2
soma.el_hh = -54.3     # Reversal potential in mV

#Insert passive current in the dendrite
dend.insert('pas')
dend.g_pas = 0.001  # Passive conductance in S/cm2
dend.e_pas = -65    # Leak reversal potential mV

#Stimulation by injecting a current pulse into the distal end of the
#dendrite after 5ms from starting the simulation
stim = h.IClamp(dend(1))
stim.delay = 5 # in ms
stim.dur = 1 # in ms
stim.amp = 0.1 # in nA

#Recording Voltage and Time
voltage = h.Vector() # Membrane potential vector
time = h.Vector() # Time stamp vector
voltage.record(soma(0.5)._ref_v)
time.record(h._ref_t)
simdur = 25.0

#Run the simulation
h.tstop = simdur
h.run()

#Plotting the data
pyplot.figure(figsize=(8,4)) # Default figsize is (8,6)
pyplot.plot(time, voltage)
pyplot.xlabel('Time (ms)')
pyplot.ylabel('Voltage (mV)')
pyplot.show()
