
import pyAFMM as afmm

import plot2Dascii as pl

windowSizex= 10e-6
windowSizey=10e-6
coreSizex=1e-6
coreSizey=0.8e-6
layerThick=1e-6

afmm.parsescript(f"size {windowSizex} {windowSizey}")
afmm.parsescript("harmonics 21 21")
afmm.parsescript("wavelength 1.55e-6")
afmm.parsescript("section 2.5e-6")
afmm.parsescript("substrate 1 0")
afmm.parsescript("matdev la 0.0")
afmm.parsescript("pml_transf .2e-6 .2e-6 .5 -0.5")
afmm.parsescript(f"rectangle 2.234 0 {coreSizex} {coreSizey} 0")
afmm.parsescript(f"rectangle 2.234 0 {windowSizex} {layerThick} 0 ({coreSizey}/2+{layerThick}/2)")
afmm.parsescript(f"rectangle 1 0 {windowSizex} {windowSizey}/2-({layerThick}+{coreSizey}/2) 0 ({windowSizey}/2-({layerThick}+{coreSizey}/2))/2+{coreSizey}/2+{layerThick}")


# Get the refractive index distribution
afmm.parsescript("inpstruct im 30 25 input_file")
# Here we represent the structure in the text terminalè (quite crudely, but
# it gives an idea, still).

afmm. order(19, 20)

# Some commands give back a return value.
neff = afmm. solve()

modelistEx = afmm. outgmodes ( "Ex", 50,21)
modelistEy = afmm. outgmodes ( "Ey", 50, 21)

