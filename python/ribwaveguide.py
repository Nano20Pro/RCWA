
import pyAFMM as afmm

import plot2Dascii as pl

windowSizex= 10e-6
windowSizey=10e-6
coreSizex=1e-6
coreSizey=0.8e-6
layerThick=1e-6

afmm.parsescript(
"""
wants ( "propagation" )
size windowSizex windowSizey
harmonics 21 21
wavelength 1.55e-6

section 2.5e-6
                  

substrate 1+0j


matdev la 0.0

pml_transf .2e-6 .2e-6 .5-0.5j
rectangle 2.234+0j*0 coreSizex coreSizey 0
rectangle 2.234+0j*0 windowSizex layerThick 0 (coreSizey/2+layerThick/2)
rectangle 1.+0j*0 windowSizex windowSizey/2-(layerThick+coreSizey/2) 0 (windowSizey/2-(layerThick+coreSizey/2))/2+coreSizey/2+layerThick)

 """)       

# Get the refractive index distribution
struct = afmm. inpstruct (30,25, "im")
# Here we represent the structure in the text terminalè (quite crudely, but
# it gives an idea, still).
print
pl.printmap (struct)
# afmm.bend(2e-6)
afmm. order(19, 20)

# Some commands give back a return value.
neff = afmm. solve()

modelistEx = afmm. outgmodes ( "Ex", 50,21)
modelistEy = afmm. outgmodes ( "Ey", 50, 21)

