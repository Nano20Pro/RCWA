input_structure = ARG1
input_file = ARG2
output_file = ARG3
parameter = ARG4

set style data lines
unset surface
set contour base
set view 0,0
set xlabel 'x axis in {/Symbol m} m'
set ylabel 'y axis in {/Symbol m} m'
set key below
set pm3d
set palette color negative
set palette defined (0 0 0 0, 1 0 0 1, 2 0 1 0, 4 1 0 0, 6 1 1 1)
set pal maxcolor 256
set surface
unset contour
unset key
set view map

if (parameter == 1) splot input_file using ($1*1e6):($2*1e6):($3) with pm3d

set size 1.0, 0.4
set term push
set terminal postscript portrait color enhanced "Helvetica" 12
set output output_file
splot input_file using ($1*1e6):($2*1e6):($3) with pm3d
set output
set terminal pop
set size 1,1
