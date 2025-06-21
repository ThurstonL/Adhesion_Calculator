import numpy as np
import matplotlib.pyplot as plt
import matplotlib.widgets as widgets
import cv2
from matplotlib import rcParams
from HelperFunctions import *

# Tkinter (Built-in GUI Library)
# Create dialog boxes that collect user input
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox

###################1 Choose an Image to analyze ##########

image = choose_image()
if image.split('.')[1] == 'png':
    image = adapt_PNG(plt.imread(image))
else:
    image = plt.imread(image)

print(image.shape)
###################2 Crop the Photo to the area you want to analyze
# Matplotlib (for plotting user input)

fig, ax = plt.subplots(constrained_layout=True)
fig.set_size_inches(10,7)

ax.imshow(image)

clicked_pts = []
color_pts = []

def onclick1(event):
    toolbar = plt.get_current_fig_manager().toolbar
    if toolbar.mode != '':
        print(f"Ignore click - toolbar mode: {toolbar.mode}")
        return

    if event.inaxes == ax and event.button==1 and len(clicked_pts)<4:
        x, y = int(event.xdata), int(event.ydata)
        clicked_pts.append((x,y))
        print(f"Clicked: ({x}, {y})")
        ax.plot(x,y, 'rx')
        plt.draw()

def onclick2(event):
    toolbar = plt.get_current_fig_manager().toolbar
    if toolbar.mode != '':
        print(f"Ignore click - toolbar mode: {toolbar.mode}")
        return

    if event.inaxes == ax and event.button==3 and len(color_pts)<2:
        x, y = int(event.xdata), int(event.ydata)
        color_pts.append((x,y))
        print(f"Clicked: ({x}, {y})")
        ax.plot(x,y, 'bx')
        plt.draw()

def reset(event):
    clicked_pts.clear()
    color_pts.clear()
    ax.clear()
    ax.imshow(image, origin='upper')
    print("Points reset")
    plt.draw()

def confirm(event):
    root = tk.Tk()
    root.withdraw()
    if messagebox.askokcancel("Confirm Close", "Are the points you selected correct?"):
        plt.close(fig)
    root.destroy()


#Create button axes [left, bottom, width, height] in figure coords
ax_reset = fig.add_axes([0.88, 0.125, 0.1, 0.05])
ax_confirm = fig.add_axes([0.88, 0.05, 0.1, 0.05])

btn_reset = widgets.Button(ax_reset, 'Reset', color='salmon', hovercolor = 'red')
btn_confirm = widgets.Button(ax_confirm, 'Confirm', color='lightgreen', hovercolor = 'green')

btn_reset.on_clicked(reset)
btn_confirm.on_clicked(confirm)

#Connect Click event
cid1 = fig.canvas.mpl_connect('button_press_event', onclick1)
cid2 = fig.canvas.mpl_connect('button_press_event', onclick2)

fig.suptitle(
"""1. Right-click one spot of paint and one spot of substrate\n
2. Use zoom tool to focus area\n
3. (Ensure toolbar icons are not highlighted) Select 4 corners of adhesion area\n
4. Hit confirm to finalize""", 
x=0.0, ha='left', fontsize=10, fontweight='bold', color='navy')
plt.show()

########### 2.5 Cropping the Image based on clicked_pts. Changing global threshold based off color_pts ######
rect = rect_corners(clicked_pts)
corners = np.array([rect['top_left'], rect['top_right'], rect['bottom_right'], rect['bottom_left']])
mask = np.zeros(image.shape[:2], dtype = np.uint8)
cv2.fillPoly(mask, [corners], 255)
masked_image = cv2.bitwise_and(image, image, mask=mask)
masked_pixels = np.sum(mask > 0)



##########3 Turn colored image to a weighted grayscale image #############
image_wgt = np.dot(masked_image[...,:3], [0.299, 0.587, 0.114])

#4 Add code here for adaptive thresholding to turn to BW. For now global threshold
x1, y1 = color_pts[0]
gray_color1 = np.dot(image[y1,x1], [0.299, 0.587, 0.114])
x2, y2 = color_pts[1]
gray_color2 = np.dot(image[y2,x2], [0.299, 0.587, 0.114])

avg_threshold = int((gray_color1 + gray_color2) / 2)
print(avg_threshold)
image_bw = grayscale_to_BW(image_wgt, avg_threshold)

#########5 Calculate the percent area remaining ############
percent = calc_area_remaining(image_bw, masked_pixels)

#5.5 Print black and white image

fig, ax = plt.subplots()
fig.set_size_inches(10,7)

ax.imshow(image_bw, cmap='gray')

fig.suptitle(f"There is {percent}% remaining", fontsize=15, fontweight='bold', color='navy')
plt.show()



