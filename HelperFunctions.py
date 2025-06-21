import numpy as np
import matplotlib.pyplot as plt
import cv2
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox

# Converts RGBA image array to an RGB

def adapt_PNG(the_PNG):
    the_PNG = the_PNG[:,:,:3]
    the_PNG = the_PNG * 255
    the_PNG = adapt_image(the_PNG)
    return the_PNG


# Rounds floating point numbers to integers 
def adapt_image(the_img):
    return np.uint8(np.clip(the_img.round(),0,255))

# This function converts a grayscale image to black and white 
# using a global threshold.
def grayscale_to_BW(grayscale_pic, threshold):
    rows, cols = np.shape(grayscale_pic)
    BW_pic = np.zeros((rows,cols))
    for i in range(rows):
        for j in range(cols):
            BW_pic[i,j] = 0 if grayscale_pic[i,j] <= threshold else 255
    return BW_pic
    
# Helper function for calculating % area remaining. Passes in BW image and mask image
def calc_area_remaining(bw_image, masked_pixels):
    remaining = 0
    rows, cols = np.shape(bw_image)
    for i in range(rows):
        for j in range(cols):
            if bw_image[i,j] == 255:
                remaining += 1
    percent = round(remaining/(masked_pixels)*100, 2)
    #print(f'There is {percent}% remaining')
    #print(f'Remaining: {remaining} \nRemoved: {removed}')
    return percent

# GUI for selecting the jpg or png image
def choose_image():
    root = tk.Tk()
    root.withdraw()

    file_path = filedialog.askopenfilename(
        title = "Select an Image File",
        filetypes=[("Image Files", "*.png"), ("Image Files", "*.jpg"), ("Image Files", "*.jpeg")]
    )

    if file_path:
        print(f'Selected image: {file_path}')
    else:
        print("No file selected.")

    return file_path

def rect_corners(clicked_pts):
    sorted_y = sorted(clicked_pts, key=lambda x: x[1])
    top = sorted_y[:2]
    bottom = sorted_y[2:]
    top_left, top_right = sorted(top, key=lambda x: x[0])
    bottom_left, bottom_right = sorted(bottom, key=lambda x: x[0])

    return {
        'top_left': top_left,
        'top_right': top_right,
        'bottom_left': bottom_left,
        'bottom_right': bottom_right,
    }
