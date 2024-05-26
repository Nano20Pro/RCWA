# The following line imports the AFMM module that should have
# been correctly installed on your machine:
import pyAFMM as afmm

import plot2Dascii as pl
import os
import shutil



def movefile(input_file,output_folder):
    # Specify the source file path
    source_path = f"/home/rigel/Documents/Project/RCWA/python/{input_file}"

    # Specify the destination directory
    destination_dir = f"/home/rigel/Documents/Project/RCWA/{output_folder}"

    # Construct the full destination path
    destination_path = os.path.join(destination_dir, os.path.basename(source_path))
    # Move the file
    try:
        shutil.move(source_path, destination_path)
        print(f"File moved to {destination_path}")
    except Exception as e:
        print(f"Error occurred: {e}")
    return 0


afmm.wants("propagation")
# AFMM commands are mapped directly into Python functions:
afmm.parsescript("""size 1.5e-6 1.5e-6
harmonics 21 21""")

#afmm.harmonics(21,21)
afmm.wavelength(1.55e-6)
afmm.section(2.5e-6)
afmm.substrate(1.44+0j)


# Commands that are not yet accessible via Python can be accessed
# by means of 'parsescript'. You can even process a whole AFMM
# script contained in a Python string using this technique.
afmm.parsescript("matdev la 0.0")
afmm.pml_transf(.2e-6,.2e-6,.5-0.5j)
afmm.rectangle(3.5+0j*0,500e-9,200e-9,0,0)

# Get the refractive index distribution
afmm.parsescript("inpstruct im 30 25 inputstruct.f3d")
movefile("inputstruct.f3d","output")


# Here we represent the structure in the text terminal (quite crudely, but
# it gives an idea, still).
#print
#pl.printmap(struct)

#afmm.bend(2e-6)

# afmm.order(19, 20)

# Some commands give back a return value.
#neff = afmm.solve()

#display part
#modelistEx = afmm.outgmodes("Ex",100,21)
#modelistEy = afmm.outgmodes("Ey",100,21)

#afmm.parsescript("outgmodes Ex o 21 21 filetest_Si_o")


afmm.parsescript("""
solve
select 1""")




afmm.parsescript("""
modepos
print posA
print posB
""")

afmm.parsescript("""
excitation "f" "id" 1.0 0.0 129 0
excitation "f" "id" 1.0 0.0 131 0
assemble
propagation Ex m 1.5e-6 50 50 propag.txt
""")



#k=0
#for mode in modelistEx:
#    print ("Mode: ",k,"n_eff=",neff[k]," |Ex| ")
#    pl.printmap(modelistEx[k])
#    print ("Mode: ",k,"n_eff=",neff[k]," |Ey| ")
#    pl.printmap(modelistEy[k])
#    k+=1

