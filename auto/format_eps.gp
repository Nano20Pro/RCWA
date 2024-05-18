
# format_ep s . gp : plot a nice image from raw data file
# useful for afmm output
# The first parameter is the input file , formatted using the afmm
# conventi on s .
# The second parameter is the output file , which should be an eps
# file .
# The third parameter is 1 if the graph should be shown in the
# current terminal .
# usage in Gnuplot :
# call " format_ep s . gp " " test . structure " " test . eps " 0

# General settings : color map view
set style data lines
unset surface ; set contour base
set view 0 ,0
# Put x and y axis labels . Note the direct use of Postcript code
# to obtain Greek characters

set xlabel ' x axis in {/ Symbol m } m '
set ylabel ' y axis in {/ Symbol m } m '
# Define the palette to be used
set key below
set pm3d
set palette color negative
set palette defined (0 0 0 0 , 1 0 0 1 , 2 0 1 0 , 4 1 0 0 , 6 1 1 1)
set pal maxcolor 256
set surface
unset contour
unset key
set view map
# Draw the color map of the file specified on the first parameter .
# Note the explicit conversion between meters and micromete r s .
if ( $2 ==1) splot '$0 ' using ( $$1 *1 e6 ):( $$2 *1 e6 ):( $$3 ) with pm3d
# Prepare an e n c a p s u l a t e d Postscript file , ready for printing
set size 1.0 , 0.4
set term push
set terminal postscript portrait color enhanced " Helvetica " 12
set output ' $1 ';
splot '$0 ' using ( $$1 *1 e6 ):( $$2 *1 e6 ):( $$3 ) with pm3d
set output
# Newer Gnuplot versions allow to use a stack for saving the
# settings of the terminal .
set terminal pop
set size 1 ,1