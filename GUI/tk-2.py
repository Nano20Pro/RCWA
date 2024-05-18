import tkinter as tk
import subprocess
import numpy as np
# Implement the default Matplotlib key bindings.
from matplotlib.backend_bases import key_press_handler
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,
                                               NavigationToolbar2Tk)
from matplotlib.figure import Figure
import pandas as pd
import subprocess

def read_f3d(file):
    with open(file) as f:
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
    E1 = pd.read_csv(file, skiprows=3, names=["Re", "Im"])
    E1 = E1["Re"]+1j*E1["Im"]
    E1 = E1.values
    E1 = E1.reshape(size, order="F").T
    return X, Y, E1

def get_color(refractive):
    color_range = 4 - 0  # Calculate the range of refractive index values
    normalized_refractive = (refractive - 0) / color_range  # Normalize the refractive index value between 0 and 1
    hue = normalized_refractive * 300  # Map the normalized value to the hue range of 0-300 (red to purple)
    color = f"#{int(hue):03x}"  # Convert the hue value to a hexadecimal color code
    return color

def get_refractive(color):
    hex_value = color.lstrip("#")  # Remove the '#' from the color code
    hue = int(hex_value, 16)  # Convert the color code to an integer
    normalized_hue = hue / 300  # Normalize the hue value between 0 and 1
    refractive = normalized_hue * 4  # Map the normalized value to the refractive index range of 0-4
    return refractive
def round_coords(coord):
    global grid, canvas_dim
    new_coord = (round(coord[0]*grid[0]/canvas_dim[0])*canvas_dim[0]/grid[0], round(coord[1]*grid[1]/canvas_dim[1])*canvas_dim[1]/grid[1])
    return  new_coord
def on_mouse_press(event):
    global start_x, start_y
    start_x,start_y = round_coords([event.x,event.y])
def on_right_click(event):
    global saved_rectangles
    item = canvas.find_closest(event.x, event.y)[0]
    if item in saved_rectangles:
        canvas.delete(item)
        saved_rectangles.remove(item)

def on_mouse_drag(event):
    global start_x, start_y, draw_rectangle, refractive
    print(f"Mouse position: {event.x}, {event.y}")
    end_x,end_y = round_coords([event.x,event.y])
    print(f"Rounded position: {end_x}, {end_y}")
    if draw_rectangle:
        canvas.delete(draw_rectangle)
    draw_rectangle = canvas.create_rectangle(start_x, start_y, end_x, end_y, outline=get_color(refractive))

def on_mouse_release(event):
    global rectangles, draw_rectangle, refractive
    end_x,end_y = round_coords([event.x,event.y])
    if draw_rectangle:
        canvas.delete(draw_rectangle)
    draw_rectangle = canvas.create_rectangle(start_x, start_y, end_x, end_y, outline=get_color(refractive))
    width = abs(end_x - start_x)
    height = abs(end_y - start_y)
    area = width * height
    
    print(f"Rectangle dimensions: {width} x {height}")
    print(f"Rectangle area: {area}")

def say_hello():
    global draw_rectangle
    canvas.itemconfig(draw_rectangle, fill=get_color(refractive))
    saved_rectangles.append(draw_rectangle)
    draw_rectangle = None
    print("Hello")

# Function to parse the values and assign them to global variables

def make_run():
    with open(skeleton, 'r', encoding='utf-8') as file: 
        data = file.readlines() 
    data.insert(save_line,f"outgmodes Ex o {canvas_dim[0]} {canvas_dim[1]} mode\n")
    data.insert(save_line,f"outgmodes Ey o {canvas_dim[0]} {canvas_dim[1]} mode\n")
    bottom_left = None
    for rectangle in saved_rectangles:
        coordinates = canvas.bbox(rectangle)
        x = coordinates[0]
        y = coordinates[3]
        if bottom_left is None or (x < bottom_left[0] and y > bottom_left[1]):
            bottom_left = (x, y)

    if bottom_left is not None:
        print(f"Furthest bottom left corner: {bottom_left}")
    else:
        print("No rectangles found.")
    for rectangle in reversed(saved_rectangles):
        coordinates = canvas.bbox(rectangle)
        bl_x = coordinates[0] - bottom_left[0]
        bl_y = -coordinates[3] + bottom_left[1]
        width = abs(coordinates[2] - coordinates[0])
        height = abs(coordinates[3] - coordinates[1])
        print(f"Rectangle bottom_left: ({bl_x}, {bl_y})")
        print(f"Rectangle width: {width}")
        print(f"Rectangle height: {height}")
        color = canvas.itemcget(rectangle, "fill")
        refractive = get_refractive(color)
        print(f"Rectangle color: {color}")
        print(f"Rectangle location: {coordinates}")
        print(f"Rectangle refractive index: {refractive}")
        data.insert(insert_line, f"rectangle {refractive} 0 {width*scale} {width*scale} {bl_x*scale} {bl_y*scale}\n")
    with open(run_file, 'w', encoding='utf-8') as file: 
        file.writelines(data)
    
    #subprocess.run(["./afmm", run_file], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    #subprocess.run(["./afmm", run_file])
    
    subprocess.run(f"./afmm {run_file}")

    # Count the occurrences of the phrase "Interesting mode" in afmm.out
    count = 0
    with open("afmm.out", "r") as f:
        for line in f:
            if "Interesting mode" in line:
                count += 1

    # Print the count
    print(f"Number of occurrences of 'Interesting mode': {count}")
    file = "/Users/benwalker/Documents/afmm/mode_Ex_o_0.f3d"

    X,Y,E1 = read_f3d(file)

    fig = Figure(figsize=(5, 4), dpi=100)
    t = np.arange(0, 3, .01)
    ax = fig.add_subplot()
    ax.pcolormesh(X,Y,np.real(E1),cmap='coolwarm')
    ax.set_xlabel("time [s]")
    ax.set_ylabel("f(t)")

    #canvas = FigureCanvasTkAgg(fig, master=root)  # A tk.DrawingArea.
    #canvas.draw()

    # pack_toolbar=False will make it easier to use a layout manager later on.
    #toolbar = NavigationToolbar2Tk(canvas, root, pack_toolbar=False)
    #toolbar.update()

    #canvas.mpl_connect(
    #    "key_press_event", lambda event: print(f"you pressed {event.key}"))
    #canvas.mpl_connect("key_press_event", key_press_handler)

    

def update_grid_size(event):
    global grid
    grid_text = grid_entry.get()
    try:
        x_grid, y_grid = map(int, grid_text.split('x'))
        grid = [x_grid, y_grid]
        if x_grid <= 0 or y_grid <= 0:
            raise ValueError
    except ValueError:
        print("Invalid grid size. Please enter a positive integer.")
        return
    print(f"Grid Size: {x_grid}x{y_grid}")

def update_scale(event):
    global scale
    scale = scale_entry.get()
    try:
        scale = float(scale)
        if scale <= 0:
            raise ValueError
    except ValueError:
        print("Invalid scale. Please enter a positive float.")
        return
    print(f"scale: {scale}")

def update_refractive(event):
    global refractive
    refractive = refractive_entry.get()
    try:
        refractive = float(refractive)
        if refractive <= 0:
            raise ValueError
    except ValueError:
        print("Invalid refractive index. Please enter a positive float.")
        return
    print(f"Refractive Index: {refractive}")


canvas_dim = [800,800]
skeleton = "skeleton.fmm"
run_file = "auto.fmm"
insert_line = 12
save_line = 18
init_grid = "20x20"
init_scale = "1e-9"
init_refractive = "1"
root = tk.Tk()
root.geometry(f"{canvas_dim[0]}x{canvas_dim[1]}")

canvas = tk.Canvas(root)
canvas.pack_propagate(False)  # Prevent canvas from automatically resizing
canvas.pack(fill=tk.BOTH, expand=True)  # Fill available space in both directions

draw_rectangle = None
canvas.create_rectangle(0, 0, canvas_dim[0], canvas_dim[1], fill='gray')
canvas.bind("<ButtonPress-1>", on_mouse_press)
canvas.bind("<B1-Motion>", on_mouse_drag)
canvas.bind("<ButtonRelease-1>", on_mouse_release)
canvas.bind("<Button-2>", on_right_click)  # Bind right-click event to on_right_click function
canvas.bind("<Button-3>", on_right_click)  # Bind right-click event to on_right_click function

button1 = tk.Button(root, text="Add Region", command=say_hello)
run_button = tk.Button(root, text="Make File & Run", command=make_run)
button_quit = tk.Button(master=root, text="Quit", command=root.destroy)
button1.pack(side=tk.LEFT, anchor=tk.W)
run_button.pack(side=tk.LEFT, anchor=tk.W)

grid_label = tk.Label(root, text="Grid Size:")
grid_label.pack(side=tk.BOTTOM)
grid_entry = tk.Entry(root)
grid_entry.pack(side=tk.BOTTOM)
scale_label = tk.Label(root, text="Scale:")
scale_label.pack(side=tk.BOTTOM)
scale_entry = tk.Entry(root)
scale_entry.pack(side=tk.BOTTOM)
refractive_label = tk.Label(root, text="Refractive Index:")
refractive_label.pack(side=tk.BOTTOM)
refractive_entry = tk.Entry(root)
refractive_entry.pack(side=tk.BOTTOM)
button_quit.pack(side=tk.BOTTOM)
#toolbar = NavigationToolbar2Tk(canvas, root, pack_toolbar=False)
#toolbar.update()
#toolbar.pack(side=tk.BOTTOM, fill=tk.X)
#canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

grid_entry.bind("<KeyRelease>", update_grid_size)
scale_entry.bind("<KeyRelease>", update_scale)
refractive_entry.bind("<KeyRelease>", update_refractive)

saved_rectangles = []

grid_entry.insert(tk.END, init_grid)
scale_entry.insert(tk.END, init_scale)
refractive_entry.insert(tk.END, init_refractive)

update_grid_size(None)
update_scale(None)
update_refractive(None)

root.mainloop()