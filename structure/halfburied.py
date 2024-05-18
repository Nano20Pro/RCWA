# The following line imports the AFMM module that should have
# been correctly installed on your machine:
import pyAFMM as afmm

import plot2Dascii as pl

# Show the program AFMM banner and credits
afmm. banner ()

windowSizex= 5e-6
windowSizey=5e-6
coreSizex=1.6e-6
coreSizey=1.2e-6

afmm. wants ( "propagation")
# AFMM commands are mapped directly into Python functions:
afmm. size (4e-6,4e-6)
afmm. harmonics (21,21)
afmm. wavelength (800e-9)

afmm. section (2.5e-6
# Each time in an AFMM script command there is a complex number
# to specify this is done by means of the real and imaginary part.
# In the Python access, this is handled directly by means of
# complex variables, as in the following command:
afmm. substrate (1+0j)

# Commands that are not yet accessible via Python can be accessed
by means of 'parsescript'. You can even process a whole AFMM
script contained in a Python string using this technique.
#
afmm. parsescript ("matdev la 0.0")
afmm. pml_transf ( .2e-6, . 2e-6, . 5-0.5j)
afmm. rectangle (2. 2+0j*0, coreSizex, coreSizey, 0, C
afmm. rectangle (1.5+0j*0,windowSizex, (windowSizey-coreSizey)/2, 0,windowSizey/4-coreSizey/4+coreSizey/2)
afmm. rectangle(1.5+0j*0, (windowSizex-coreSizex)/2, coreSizey, coreSizex/2-coreSizey/4+windowSizex/4,0
afmm. rectangle (1.5+0j*0, (windowSizex-coreSizex)/2, coreSizey, -(coreSizex/2-coreSizey/4+windowSizex/4),0)

# Get the refractive index distribution
struct = afmm. inpstruct (30,25,"im")

# Here we represent the structure in the text terminal (quite crudely, but
# it gives an idea, still).
print
pl.printmap (struct)
# afmm.bend(2e-6)
# afmm.order(19, 20)

# Some commands give back a return value.
neff = afmm. solve()

modelistEx = afmm. outgmodes ( "Ex", 50,21)
modelistEy = afmm. outgmodes ("Ey", 50,21)

print
k=0
for mode in modelistEx:
print ("Mode: ",k, "n_eff=", neff[k], " | Ex| ")
pl. printmap (modelistEx [k])
print ("Mode: ",k, "n_eff=", neff[k], " | Ey| ")
pl.printmap (modelistEy [k] )
k+=1