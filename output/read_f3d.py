import pandas as pd
import math
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
def val_sign(value, digits):
    if value == 0:
        return 0
    else:
        return round(value, digits - int(math.floor(math.log10(abs(value)))) - 1)


def count_mesh_size(df):
    first_column = df.iloc[:, 0]
    second_column = df.iloc[:, 1]
    first_column=list(first_column)
    elt=first_column.pop(0)
    size_x,size_y=first_column.index(elt)+1,first_column.count(elt)+1
    x1,x2,y1,y2 = elt,first_column[size_x-2],second_column[0],second_column[(size_y-1)*size_x]
    return size_x,size_y,x1,x2,y1,y2

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
    E1['Re'] = E1['Re'].apply(lambda x: val_sign(x, 2) if not pd.isna(x) else x)
    E1['Im'] = E1['Im'].apply(lambda x: val_sign(x, 2) if not pd.isna(x) else x)
    E1 = E1["Re"]+1j*E1["Im"]
    E1 = E1.values
    E1 = E1.reshape(size, order="F").T

    #%% Plot the data
    fig,ax = plt.subplots()
    # fig.set_size_inches([10,5])
    # ax.set_axis_off()
    # ax.set_position([0.1,0.2,0.8,0.7])
    p = plt.pcolormesh(X,Y,np.real(E1),cmap='coolwarm')
    print((np.real(E1)).size)
    plt.clim([np.min(np.real(E1)),np.max(np.real(E1))])
    plt.title("$Re(E)$", fontsize=24)

    # Show the plot
    plt.show()
    return 0

def read_structure_fct(file_E):
    with open(file_E) as f:
        header=["x","y","im.real","im.imag"]
        E1 = pd.read_csv('input_file.f3d', skiprows=1, sep='\s+', names=header)

# Print the DataFrame
    print(E1)
    #print('\n'.join([str(x) for x in list(E1["x"])[:31]]))
    size_x,size_y,x1,x2,y1,y2=count_mesh_size(E1)
    print(size_x,size_y,x1,x2,y1,y2)

    X = np.linspace(x1, x2, size_x)
    Y = np.linspace(y1, y2, size_y)

    X,Y = np.meshgrid(X,Y)


    E1 = E1["im.real"]+1j*E1["im.imag"]
    E1 = E1.values
    E1 = E1.reshape(size_x, size_y, order="F").T

    #%% Plot the data
    fig,ax = plt.subplots()
    # fig.set_size_inches([10,5])
    # ax.set_axis_off()
    # ax.set_position([0.1,0.2,0.8,0.7])
    p = plt.pcolormesh(X,Y,np.real(E1),cmap='coolwarm')
    plt.clim([np.min(np.real(E1)),np.max(np.real(E1))])
    plt.title("$structure$", fontsize=24)

    # Show the plot
    plt.show()
    return 0

def read_modes_fct(file_E):
    with open(file_E) as f:
        header=["x","y","neff.real"]
        E1 = pd.read_csv(file_E, skiprows=2, sep='\s+', names=header)
        
# Print the DataFrame
    print(E1)
    #print('\n'.join([str(x) for x in list(E1["x"])[:31]]))
    size_x,size_y,x1,x2,y1,y2=count_mesh_size(E1)
    print(size_x,size_y,x1,x2,y1,y2)

    X = np.linspace(x1, x2, size_x)
    Y = np.linspace(y1, y2, size_y)

    X,Y = np.meshgrid(X,Y)


    E1 = E1["neff.real"]
    E1 = E1.values
    E1 = E1.reshape(size_x, size_y, order="F").T

    #%% Plot the data
    fig,ax = plt.subplots()
    # fig.set_size_inches([10,5])
    # ax.set_axis_off()
    # ax.set_position([0.1,0.2,0.8,0.7])
    p = plt.pcolormesh(X,Y,np.real(E1),cmap='coolwarm')
    plt.clim([np.min(np.real(E1)),np.max(np.real(E1))])
    plt.title("$modes$", fontsize=24)

    # Show the plot
    plt.show()
    return 0

###
#read_f3d_fct("filetest_Si_o_Ex_o_1.f3d")
#read_structure_fct("filetest_Si_o_Ex_o_1.f3d")

for i in range(4):
    filename = f"filetest_Si_r_Ex_r_{i}.mode"  # Adjust the filename pattern as needed
    read_modes_fct(filename)


