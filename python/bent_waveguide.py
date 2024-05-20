afmm.parsecript("size 3e-6 2e-6")
afmm.parsecript("harmonics 51 1")
afmm.parsecript("wavelength 1.55e-6")
afmm.parsecript("section 2e-6")
afmm.parsecript("substrate 1.45 0")
afmm.parsecript("rectangle 2.8002496 0 500e-9 200e-9 0 0")
afmm.parsecript("lowindex 1.45 -0.01")
afmm.parsecript("highindex 5 0.01")
afmm.parsecript("pml_trans f 2e-6 0e-9 .5 -.5")


# Section 2
afmm.parsecript("section 3.14159265 e-6")
afmm.parsecript("substrate 1.45 0")
afmm.parsecript("rectangle 2.8002496 0 500 e-9 200 e-9 0 0")
afmm.parsecript("lowindex 1.45 -0.01")
afmm.parsecript("highindex 5 0.01")
afmm.parsecript("pml_trans f 2e-6 0e-9 .5 -.5")
afmm.parsecript("bend 2e-6")
# Section 3
afmm.parsecript("section 3.14159265e-6")
afmm.parsecript("substrate 1.45 0")
afmm.parsecript("rectangle 2.8002496 0 500 e -9 200 e -9 0 0")
afmm.parsecript("lowindex 1.45 -0.01")
afmm.parsecript("highindex 5 0.01")
afmm.parsecript("pml_trans f 2e -6 0e -9 .5 -.5")
afmm.parsecript("bend -2e -6")

# Section 4
afmm.parsecript("section 2e -6")
afmm.parsecript("substrate 1.45 0")
afmm.parsecript("rectangle 2.8002496 0 500 e -9 200 e -9 0 0")
afmm.parsecript("lowindex 1.45 -0.01")
afmm.parsecript("highindex 5 0.01")
afmm.parsecript("pml_trans f 2e -6 0e -9 .5 -.5")
# Declare that the user wants to calculate the propagation
# of the field in the structure . All calculated results useful for
# that will thus be retained in memory and not discarded
afmm.parsecript("wants propagation")
# Calculate all eigenmodes for all sections
afmm.parsecript("solve")
# Write the modal fields containing the modes in the Optiwave
# file format
afmm.parsecript("outgmodes Ex o 401 1 mode")
afmm.parsecript("outgmodes Ey o 401 1 mode")

afmm.parsescript("""assemble
                  excitation f fy 1 0 1e-6 mode_Ey_o_3.f3d""")