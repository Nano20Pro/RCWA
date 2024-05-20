import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

def read_f3d_fct(file_E):
    #%% Read the header of the simulation file
    # Read the size of the simulated window and the number of points
    with open(file_E) as f:
        f.readline()
        size = f.readline()
        L = f.readline()

    size = size.strip().split(" ")
    size = [int(a) for a in size if a!=""]

    L = L.strip().split(" ")
    L = [float(a) for a in L if a!=""]

    x = np.linspace(L[0], L[1], size[0])
    y = np.linspace(L[2], L[3], size[1])

    X,Y = np.meshgrid(x,y)

    #read E field Re & Im components
    E1 = pd.read_csv(file_E, skiprows=3, names=["Re", "Im"])
    E1 = E1["Re"]+1j*E1["Im"]
    E1 = E1.values
    E1 = E1.reshape(size, order="F").T

    #%% Plot the data
    fig,ax = plt.subplots()
    # fig.set_size_inches([10,5])
    # ax.set_axis_off()
    # ax.set_position([0.1,0.2,0.8,0.7])
    p = plt.pcolormesh(X,Y,np.real(E1),cmap='coolwarm')
    plt.clim([np.min(np.real(E1)),np.max(np.real(E1))])
    plt.title("$Re(E)$", fontsize=24)

    # Show the plot
    plt.show()
    
    
read_f3d_fct("input_file.f3d")
